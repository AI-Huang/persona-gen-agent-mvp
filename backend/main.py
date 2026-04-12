from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware  # 解决跨域问题
from pydantic import BaseModel

from backend.agent.parameter_agent import ParameterAgent
from backend.agent.parser_agent import ParserAgent
from backend.agent.prompt_agent import PromptAgent
from backend.config.settings import settings
from backend.data.persona_templates import PERSONA_TEMPLATES
from backend.utils.common import format_params

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


# 启动服务（关联配置文件中的端口、主机）
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app", host=settings.HOST, port=settings.PORT, reload=settings.RELOAD
    )
