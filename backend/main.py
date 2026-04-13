from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware  # 解决跨域问题
from pydantic import BaseModel

from backend.agent.chatbot_agent import ChatBot
from backend.agent.parameter_agent import ParameterAgent
from backend.agent.parser_agent import ParserAgent
from backend.agent.prompt_agent import PromptAgent
from backend.config.settings import settings
from backend.data.persona_templates import PERSONA_TEMPLATES
from backend.database.db import create_tables
from backend.utils.common import format_params

# 初始化数据库表
create_tables()

# 初始化FastAPI应用
app = FastAPI(title="Persona Prompt & OpenAI Parameter Agent (MVP)", version="1.0.0")

# 解决跨域问题（前端对接后端必备）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 开发环境允许所有来源，生产环境可修改为指定域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 输入模型（简化，MVP够用，增加数据校验）
class NaturalLanguageInput(BaseModel):
    prompt: str
    scene: str = "dify"


class TemplateInput(BaseModel):
    template_id: int
    scene: str = "dify"


# ChatBot 相关输入模型
class ChatBotCreateInput(BaseModel):
    name: str
    system_prompt: str
    model: str = "gpt-3.5-turbo"


class ChatBotInput(BaseModel):
    chatbot_id: str
    model: str
    messages: list
    temperature: float = 0.7
    top_p: float = 1.0
    n: int = 1
    stream: bool = False
    stop: list = None
    max_tokens: int = None
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0
    logit_bias: dict = None
    user: str = None
    response_format: dict = None
    seed: int = None
    tools: list = None
    tool_choice: str = None
    parallel_tool_calls: bool = True


# 路由：获取所有人格模板（供前端下拉选择）
@app.get(
    "/api/templates",
    summary="获取所有人格模板",
    description="返回10+高频人格模板，供前端下拉选择",
)
async def get_templates():
    return {"code": 200, "message": "success", "data": PERSONA_TEMPLATES}


# 路由：通过模板生成方案（核心路由）
@app.post(
    "/api/generate-by-template",
    summary="按模板生成方案",
    description="选择模板后，生成对应的提示词和OpenAI参数",
)
async def generate_by_template(input: TemplateInput):
    # 1. 解析模板
    template = ParserAgent.parse_template(input.template_id)
    if not template:
        raise HTTPException(
            status_code=400, detail="模板不存在，请选择有效的模板ID（1-10）"
        )
    # 2. 生成提示词
    prompt = PromptAgent.generate_prompt(template, input.scene)
    # 3. 匹配参数
    params = ParameterAgent.match_parameters(template, input.scene)
    # 4. 生成Python API调用示例（仅API场景）
    api_example = ""
    if input.scene == "api":
        api_example = f"""import openai
from backend.config.settings import settings  # 若后端调用，可直接导入配置

# 初始化OpenAI客户端
openai.api_key = settings.OPENAI_API_KEY

# 调用OpenAI API
response = openai.ChatCompletion.create(
    model="{settings.OPENAI_MODEL}",
    temperature={params['temperature']},
    top_p={params['top_p']},
    frequency_penalty={params['frequency_penalty']},
    presence_penalty={params['presence_penalty']},
    max_tokens={params['max_tokens']},
    messages={format_params(params['messages'])}
)

# 输出结果
print("AI回复：", response.choices[0].message.content)"""

    return {
        "code": 200,
        "message": "生成成功",
        "data": {
            "prompt": prompt,
            "params": params,
            "api_example": api_example,
            "matched_template": template["name"],
        },
    }


# 路由：通过自然语言生成方案（核心路由）
@app.post(
    "/api/generate-by-nl",
    summary="按自然语言生成方案",
    description="输入人格描述，自动匹配模板并生成方案",
)
async def generate_by_nl(input: NaturalLanguageInput):
    # 1. 解析自然语言，匹配模板
    template = ParserAgent.parse_natural_language(input.prompt)
    # 2. 生成提示词
    prompt = PromptAgent.generate_prompt(template, input.scene)
    # 3. 匹配参数
    params = ParameterAgent.match_parameters(template, input.scene)
    # 4. 生成Python API调用示例（仅API场景）
    api_example = ""
    if input.scene == "api":
        api_example = f"""import openai
from backend.config.settings import settings  # 若后端调用，可直接导入配置

# 初始化OpenAI客户端
openai.api_key = settings.OPENAI_API_KEY

# 调用OpenAI API
response = openai.ChatCompletion.create(
    model="{settings.OPENAI_MODEL}",
    temperature={params['temperature']},
    top_p={params['top_p']},
    frequency_penalty={params['frequency_penalty']},
    presence_penalty={params['presence_penalty']},
    max_tokens={params['max_tokens']},
    messages={format_params(params['messages'])}
)

# 输出结果
print("AI回复：", response.choices[0].message.content)"""

    return {
        "code": 200,
        "message": "生成成功",
        "data": {
            "prompt": prompt,
            "params": params,
            "api_example": api_example,
            "matched_template": template["name"],  # 告知用户匹配的模板，提升体验
        },
    }


# ChatBot 相关路由
# 存储活跃的 ChatBot 实例
chatbot_instances = {}


# 路由：创建 ChatBot
@app.post(
    "/api/chatbot/create",
    summary="创建 ChatBot",
    description="创建一个新的 ChatBot 实例，初始化 system 提示词",
)
async def create_chatbot(input: ChatBotCreateInput):
    try:
        # 创建 ChatBot 实例
        chatbot = ChatBot(
            name=input.name, system_prompt=input.system_prompt, model=input.model
        )

        # 存储实例
        chatbot_instances[chatbot.chatbot_id] = chatbot

        return {
            "code": 200,
            "message": "创建成功",
            "data": {
                "chatbot_id": chatbot.chatbot_id,
                "name": chatbot.name,
                "system_prompt": chatbot.system_prompt,
                "model": chatbot.model,
            },
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建 ChatBot 失败: {str(e)}")


# 路由：与 ChatBot 对话
@app.post(
    "/api/chatbot/chat",
    summary="与 ChatBot 对话",
    description="向指定的 ChatBot 发送消息并获取响应，支持 OpenAI Chat Completions API 的完整参数",
)
async def chat_with_chatbot(input: ChatBotInput):
    try:
        # 获取 ChatBot 实例
        chatbot = chatbot_instances.get(input.chatbot_id)
        if not chatbot:
            raise HTTPException(
                status_code=404, detail=f"ChatBot {input.chatbot_id} 不存在"
            )

        # 进行对话
        response = chatbot.chat(
            messages=input.messages,
            model=input.model,
            temperature=input.temperature,
            top_p=input.top_p,
            n=input.n,
            stream=input.stream,
            stop=input.stop,
            max_tokens=input.max_tokens,
            frequency_penalty=input.frequency_penalty,
            presence_penalty=input.presence_penalty,
            logit_bias=input.logit_bias,
            user=input.user,
            response_format=input.response_format,
            seed=input.seed,
            tools=input.tools,
            tool_choice=input.tool_choice,
            parallel_tool_calls=input.parallel_tool_calls,
        )

        return {"code": 200, "message": "对话成功", "data": {"response": response}}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"对话失败: {str(e)}")


# 路由：获取 ChatBot 对话历史
@app.get(
    "/api/chatbot/conversations/{chatbot_id}",
    summary="获取 ChatBot 对话历史",
    description="获取指定 ChatBot 的对话历史",
)
async def get_chatbot_conversations(chatbot_id: str, limit: int = 10):
    try:
        # 获取 ChatBot 实例
        chatbot = chatbot_instances.get(chatbot_id)
        if not chatbot:
            raise HTTPException(status_code=404, detail="ChatBot 不存在")

        # 获取对话历史
        conversations = chatbot.get_conversations(limit)

        return {"code": 200, "message": "获取成功", "data": conversations}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取对话历史失败: {str(e)}")


# 启动服务（关联配置文件中的端口、主机）
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app", host=settings.HOST, port=settings.PORT, reload=settings.RELOAD
    )
