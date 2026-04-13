from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.agent.chatbot_agent import ChatBot
from backend.database.db import ChatBot as ChatBotModel
from backend.database.db import get_db

router = APIRouter()

# 存储活跃的 ChatBot 实例
chatbot_instances = {}


class ChatBotCreateInput(BaseModel):
    name: str
    system_prompt: str
    model: str = "gpt-5"


class ChatBotUpdateInput(BaseModel):
    name: str
    system_prompt: str
    model: str


class OpenAICompletionCreateParams(BaseModel):
    """Copy from openai.types.chat.CompletionCreateParams"""

    # 必需参数
    messages: list
    """A list of messages comprising the conversation so far.
    
    Depending on the model you use, different message types (modalities) are supported, like text, images, and audio.
    """

    model: str
    """Model ID used to generate the response, like `gpt-4o` or `o3`.
    
    OpenAI offers a wide range of models with different capabilities, performance characteristics, and price points.
    """

    # 可选参数
    audio: dict = None
    """Parameters for audio output.
    
    Required when audio output is requested with `modalities: ["audio"]`.
    """

    frequency_penalty: float = 0.0
    """Number between -2.0 and 2.0.
    
    Positive values penalize new tokens based on their existing frequency in the text so far, decreasing the model's likelihood to repeat the same line verbatim.
    """

    function_call: dict = None
    """Deprecated in favor of `tool_choice`.
    
    Controls which (if any) function is called by the model.
    """

    functions: list = None
    """Deprecated in favor of `tools`.
    
    A list of functions the model may generate JSON inputs for.
    """

    logit_bias: dict = None
    """Modify the likelihood of specified tokens appearing in the completion.
    
    Accepts a JSON object that maps tokens (specified by their token ID in the tokenizer) to an associated bias value from -100 to 100.
    """

    logprobs: bool = None
    """Whether to return log probabilities of the output tokens or not.
    
    If true, returns the log probabilities of each output token returned in the `content` of `message`.
    """

    max_completion_tokens: int = None
    """
    An upper bound for the number of tokens that can be generated for a completion,
    including visible output tokens and reasoning tokens.
    """

    max_tokens: int = None
    """
    The maximum number of tokens that can be generated in the chat completion. This value can be used to control costs for text generated via API.
    
    This value is now deprecated in favor of `max_completion_tokens`.
    """

    metadata: dict = None
    """Set of 16 key-value pairs that can be attached to an object.
    
    This can be useful for storing additional information about the object in a structured format, and querying for objects via API or the dashboard.
    """

    modalities: list = None
    """
    Output types that you would like the model to generate. Most models are capable
    of generating text, which is the default: `["text"]`
    
    The `gpt-4o-audio-preview` model can also be used to generate audio.
    """

    n: int = 1
    """How many chat completion choices to generate for each input message.
    
    Note that you will be charged based on the number of generated tokens across all of the choices. Keep `n` as `1` to minimize costs.
    """

    parallel_tool_calls: bool = True
    """
    Whether to enable parallel function calling during tool use.
    """

    prediction: dict = None
    """
    Static predicted output content, such as the content of a text file that is
    being regenerated.
    """

    presence_penalty: float = 0.0
    """Number between -2.0 and 2.0.
    
    Positive values penalize new tokens based on whether they appear in the text so far, increasing the model's likelihood to talk about new topics.
    """

    prompt_cache_key: str = None
    """
    Used by OpenAI to cache responses for similar requests to optimize your cache
    hit rates. Replaces the `user` field.
    """

    prompt_cache_retention: str = None
    """The retention policy for the prompt cache.
    
    Set to `24h` to enable extended prompt caching, which keeps cached prefixes active for longer, up to a maximum of 24 hours.
    """

    reasoning_effort: str = None
    """
    Constrains effort on reasoning for reasoning models. Currently
    supported values are `none`, `minimal`, `low`, `medium`, `high`, and `xhigh`.
    """

    response_format: dict = None
    """An object specifying the format that the model must output.
    
    Setting to `{ "type": "json_schema", "json_schema": {...} }` enables Structured Outputs which ensures the model will match your supplied JSON schema.
    """

    safety_identifier: str = None
    """
    A stable identifier used to help detect users of your application that may be
    violating OpenAI's usage policies.
    """

    seed: int = None
    """
    This feature is in Beta. If specified, our system will make a best effort to
    sample deterministically, such that repeated requests with the same `seed` and
    parameters should return the same result.
    """

    service_tier: str = None
    """Specifies the processing type used for serving the request.
    
    - If set to 'auto', then the request will be processed with the service tier configured in the Project settings.
    - If set to 'default', then the request will be processed with the standard pricing and performance for the selected model.
    - If set to 'flex' or 'priority', then the request will be processed with the corresponding service tier.
    """

    stop: list = None
    """Not supported with latest reasoning models `o3` and `o4-mini`.
    
    Up to 4 sequences where the API will stop generating further tokens. The returned text will not contain the stop sequence.
    """

    store: bool = None
    """
    Whether or not to store the output of this chat completion request for use in
    our model distillation or evals products.
    """

    stream_options: dict = None
    """Options for streaming response. Only set this when you set `stream: true`."""

    temperature: float = 0.7
    """What sampling temperature to use, between 0 and 2.
    
    Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. We generally recommend altering this or `top_p` but not both.
    """

    tool_choice: dict = None
    """
    Controls which (if any) tool is called by the model. `none` means the model will
    not call any tool and instead generates a message. `auto` means the model can
    pick between generating a message or calling one or more tools. `required` means
    the model must call one or more tools.
    """

    tools: list = None
    """A list of tools the model may call.
    
    You can provide either custom tools or function tools.
    """

    top_logprobs: int = None
    """
    An integer between 0 and 20 specifying the number of most likely tokens to
    return at each token position, each with an associated log probability.
    `logprobs` must be set to `true` if this parameter is used.
    """

    top_p: float = 1.0
    """
    An alternative to sampling with temperature, called nucleus sampling, where the
    model considers the results of the tokens with top_p probability mass. So 0.1
    means only the tokens comprising the top 10% probability mass are considered.
    
    We generally recommend altering this or `temperature` but not both.
    """

    user: str = None
    """This field is being replaced by `safety_identifier` and `prompt_cache_key`.
    
    Use `prompt_cache_key` instead to maintain caching optimizations. A stable identifier for your end-users.
    """

    verbosity: str = None
    """Constrains the verbosity of the model's response.
    
    Lower values will result in more concise responses, while higher values will result in more verbose responses. Currently supported values are `low`, `medium`, and `high`.
    """

    web_search_options: dict = None
    """
    This tool searches the web for relevant results to use in a response. Learn more
    about the web search tool.
    """


class ChatBotInput(BaseModel):
    chatbot_id: str
    params: OpenAICompletionCreateParams


@router.get(
    "/list",
    summary="获取 ChatBot 列表",
    description="获取所有 ChatBot 实例",
)
async def get_chatbots():
    try:
        # 获取数据库会话
        db_generator = get_db()
        db = next(db_generator)
        
        # 查询所有 ChatBot
        chatbots = db.query(ChatBotModel).all()
        
        # 转换为响应格式
        chatbot_list = []
        for chatbot in chatbots:
            chatbot_list.append({
                "id": chatbot.id,
                "name": chatbot.name,
                "systemPrompt": chatbot.system_prompt,
                "model": chatbot.model
            })
        
        return {
            "code": 200,
            "message": "获取成功",
            "data": chatbot_list
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取 ChatBot 列表失败: {str(e)}")


@router.put(
    "/update/{chatbot_id}",
    summary="更新 ChatBot",
    description="更新指定 ChatBot 的信息",
)
async def update_chatbot(chatbot_id: str, input: ChatBotUpdateInput):
    try:
        # 获取数据库会话
        db_generator = get_db()
        db = next(db_generator)
        
        # 查询 ChatBot
        chatbot = db.query(ChatBotModel).filter(ChatBotModel.id == chatbot_id).first()
        if not chatbot:
            raise HTTPException(status_code=404, detail=f"ChatBot {chatbot_id} 不存在")
        
        # 更新 ChatBot 信息
        chatbot.name = input.name
        chatbot.system_prompt = input.system_prompt
        chatbot.model = input.model
        
        # 保存到数据库
        db.commit()
        db.refresh(chatbot)
        
        # 更新内存中的实例
        if chatbot_id in chatbot_instances:
            del chatbot_instances[chatbot_id]
        
        return {
            "code": 200,
            "message": "更新成功",
            "data": {
                "id": chatbot.id,
                "name": chatbot.name,
                "system_prompt": chatbot.system_prompt,
                "model": chatbot.model
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新 ChatBot 失败: {str(e)}")


@router.delete(
    "/delete/{chatbot_id}",
    summary="删除 ChatBot",
    description="删除指定的 ChatBot 实例",
)
async def delete_chatbot(chatbot_id: str):
    try:
        # 获取数据库会话
        db_generator = get_db()
        db = next(db_generator)
        
        # 查询 ChatBot
        chatbot = db.query(ChatBotModel).filter(ChatBotModel.id == chatbot_id).first()
        if not chatbot:
            raise HTTPException(status_code=404, detail=f"ChatBot {chatbot_id} 不存在")
        
        # 删除 ChatBot
        db.delete(chatbot)
        db.commit()
        
        # 从内存中删除实例
        if chatbot_id in chatbot_instances:
            del chatbot_instances[chatbot_id]
        
        return {
            "code": 200,
            "message": "删除成功"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除 ChatBot 失败: {str(e)}")


@router.post(
    "/create",
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


@router.post(
    "/chat",
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
        response = chatbot.chat(messages=input.params.messages, params=input.params)

        return {"code": 200, "message": "对话成功", "data": {"response": response}}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"对话失败: {str(e)}")        raise HTTPException(status_code=500, detail=f"对话失败: {str(e)}")