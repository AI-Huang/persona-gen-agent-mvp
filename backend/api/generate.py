from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.agent.parameter_agent import ParameterAgent
from backend.agent.parser_agent import ParserAgent
from backend.agent.prompt_agent import PromptAgent
from backend.config.settings import settings
from backend.utils.common import format_params

router = APIRouter()


# 输入模型（简化，MVP够用，增加数据校验）
class NaturalLanguageInput(BaseModel):
    prompt: str
    scene: str = "dify"


class TemplateInput(BaseModel):
    template_id: int
    scene: str = "dify"


@router.post(
    "/generate-by-template",
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


@router.post(
    "/generate-by-nl",
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
