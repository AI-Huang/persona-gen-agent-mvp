import openai
from sqlalchemy.orm import Session

from backend.config.settings import settings
from backend.database.db import ChatBot as ChatBotModel
from backend.database.db import Conversation, get_db


class ChatBot:
    def __init__(self, name: str, system_prompt: str, model: str = "gpt-3.5-turbo"):
        """
        初始化 ChatBot
        注意：system 提示词初始化后就不能修改，这是 OpenAI 官方建议的
        """
        self.name = name
        self.system_prompt = system_prompt  # 一旦初始化，不能修改
        self.model = model
        self.chatbot_id = None
        self.db: Session = None

        # 初始化 OpenAI 客户端
        openai.api_key = settings.OPENAI_API_KEY

        # 初始化数据库会话
        self._init_db()

        # 保存到数据库
        self._save_to_db()

    def _init_db(self):
        """初始化数据库会话"""
        db_generator = get_db()
        self.db = next(db_generator)

    def _save_to_db(self):
        """保存 ChatBot 到数据库"""
        chatbot = ChatBotModel(
            name=self.name, system_prompt=self.system_prompt, model=self.model
        )
        self.db.add(chatbot)
        self.db.commit()
        self.db.refresh(chatbot)
        self.chatbot_id = chatbot.id

    def chat(self, messages, params) -> str:
        """
        与 ChatBot 对话
        1. 发送用户消息到 OpenAI API
        2. 接收并返回模型响应
        3. 保存对话到数据库
        """
        try:
            # 构建消息，确保包含系统提示词
            final_messages = []
            has_system_prompt = False
            for message in messages:
                if message["role"] == "system":
                    has_system_prompt = True
                    final_messages.append(message)
            if not has_system_prompt:
                final_messages.insert(
                    0, {"role": "system", "content": self.system_prompt}
                )

            # 获取用户消息，用于保存到数据库
            user_message = ""
            for message in messages:
                if message["role"] == "user":
                    user_message = message["content"]

            # 调用 OpenAI API (OpenAI SDK v1.0+ 格式)
            from openai import OpenAI

            client = OpenAI(
                api_key=settings.OPENAI_API_KEY, base_url=settings.OPENAI_BASE_URL
            )

            response = client.chat.completions.create(
                model=params.model or self.model,
                messages=final_messages,
                temperature=params.temperature,
                top_p=params.top_p,
                n=params.n,
                stream=params.stream,
                stop=params.stop,
                max_tokens=params.max_tokens,
                frequency_penalty=params.frequency_penalty,
                presence_penalty=params.presence_penalty,
                logit_bias=params.logit_bias,
                user=params.user,
                response_format=params.response_format,
                seed=params.seed,
                tools=params.tools,
                tool_choice=params.tool_choice,
                parallel_tool_calls=params.parallel_tool_calls,
                # 新增参数
                audio=params.audio,
                function_call=params.function_call,
                functions=params.functions,
                logprobs=params.logprobs,
                max_completion_tokens=params.max_completion_tokens,
                metadata=params.metadata,
                modalities=params.modalities,
                prediction=params.prediction,
                prompt_cache_key=params.prompt_cache_key,
                prompt_cache_retention=params.prompt_cache_retention,
                reasoning_effort=params.reasoning_effort,
                safety_identifier=params.safety_identifier,
                service_tier=params.service_tier,
                store=params.store,
                stream_options=params.stream_options,
                top_logprobs=params.top_logprobs,
                verbosity=params.verbosity,
                web_search_options=params.web_search_options,
            )

            # 获取模型响应
            model_response = response.choices[0].message.content

            # 保存对话到数据库
            self._save_conversation(user_message, model_response)

            return model_response
        except Exception as e:
            print(f"对话失败: {e}")
            raise

    def _save_conversation(self, user_message: str, model_response: str):
        """保存对话到数据库"""
        conversation = Conversation(
            chatbot_id=self.chatbot_id,
            user_message=user_message,
            model_response=model_response,
        )
        self.db.add(conversation)
        self.db.commit()

    def get_conversations(self, limit: int = 10) -> list:
        """获取对话历史"""
        conversations = (
            self.db.query(Conversation)
            .filter(Conversation.chatbot_id == self.chatbot_id)
            .order_by(Conversation.created_at.desc())
            .limit(limit)
            .all()
        )

        return [
            {
                "id": conv.id,
                "user_message": conv.user_message,
                "model_response": conv.model_response,
                "created_at": conv.created_at,
            }
            for conv in conversations
        ]

    def close(self):
        """关闭数据库会话"""
        if self.db:
            self.db.close()
