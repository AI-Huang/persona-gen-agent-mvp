# 人格提示词与OpenAI参数生成AI Agent产品方案（第一阶段MVP落地版-项目结构+核心代码）

核心定位：一款「输入人格需求，输出可直接复制使用」的AI工具——用户只需描述人格类型（如专业药品助手、治愈陪伴、毒舌顾问），Agent自动生成结构化人格提示词（含大五参数/MBTI）、配套OpenAI API参数，且支持一键复制，适配Dify、直接API调用等核心场景，主打“零门槛、高适配、可落地”，聚焦第一阶段MVP核心目标快速落地。

# 一、第一阶段MVP项目结构（前后端分离，快速开发）

采用「Python后端（FastAPI，轻量高效）+ Vue3前端（简化界面，聚焦核心功能）」，无需复杂架构，降低开发成本，1-2周可完成开发部署。项目结构完整可直接复用，包含所有核心模块及配置文件，无需额外补充。

## 1.1 整体项目结构

```plain text
persona-agent-mvp/
├── backend/                # Python后端（FastAPI）
│   ├── main.py             # 入口文件，路由配置（核心）
│   ├── agent/              # Agent核心逻辑（核心目录）
│   │   ├── __init__.py     # 包初始化
│   │   ├── parser_agent.py # 需求解析Agent（核心逻辑）
│   │   ├── prompt_agent.py # 提示词生成Agent（核心逻辑）
│   │   └── parameter_agent.py # 参数匹配Agent（核心逻辑）
│   ├── config/             # 配置文件目录
│   │   ├── __init__.py     # 包初始化
│   │   └── settings.py     # 基础配置（OpenAI密钥、端口、日志等）
│   ├── data/               # 静态数据目录（核心）
│   │   ├── __init__.py     # 包初始化
│   │   └── persona_templates.py # 10+高频人格模板（核心数据）
│   ├── utils/              # 工具函数目录
│   │   ├── __init__.py     # 包初始化
│   │   └── common.py       # 通用工具（复制功能、格式转换、异常处理）
│   ├── requirements.txt    # 后端依赖包清单（可直接pip安装）
│   └── .env                # 环境变量文件（存储敏感信息，不提交代码）
├── frontend/               # Vue3前端（简化版，聚焦核心功能）
│   ├── public/             # 静态资源目录
│   │   └── index.html      # 入口HTML文件
│   ├── src/                # 前端核心代码目录
│   │   ├── components/     # 核心组件（仅保留必备）
│   │   │   ├── InputPanel.vue # 输入面板（模板选择、自然语言输入）
│   │   │   └── OutputPanel.vue # 输出面板（提示词、参数、一键复制）
│   │   ├── utils/          # 前端工具目录
│   │   │   └── request.js  # 简化请求工具（对接后端接口）
│   │   ├── App.vue         # 主页面（整合输入/输出面板）
│   │   ├── main.js         # 前端入口文件（初始化Vue）
│   │   └── style.css       # 简单样式（无需复杂美化）
│   ├── package.json        # 前端依赖包清单（可直接npm安装）
│   ├── package-lock.json   # 依赖版本锁定文件
│   └── vite.config.js      # Vite配置文件（简化配置，确保快速启动）
└── README.md               # 项目说明文档（部署步骤、使用说明）
```

## 1.2 核心目录及文件说明

- backend/agent/：核心Agent逻辑目录，对应方案中的3个核心节点（需求解析、提示词生成、参数匹配），代码极简、聚焦MVP需求，无冗余逻辑，可直接运行。

- backend/data/persona_templates.py：预设10+高频人格模板，直接定义模板名称、大五参数、行为规则，无需数据库，直接读取静态数据，快速落地。

- backend/config/settings.py + .env：分离配置与代码，敏感信息（如OpenAI密钥）存储在.env文件，避免泄露，符合开发规范。

- frontend/components/：仅保留2个核心组件，简化界面开发，聚焦“输入→输出”闭环，无需复杂交互和美化，降低前端开发成本。

- README.md：补充项目部署、启动步骤，方便开发人员快速上手，确保1-2周内完成部署上线。

# 二、第一阶段MVP核心代码（可直接复制复用，完整可运行）

所有代码均贴合MVP需求，简化逻辑、去除冗余，补充缺失的配置文件和异常处理，确保复制后可直接运行，重点实现“模板选型、自然语言解析、提示词+参数生成、一键复制”核心功能，同时符合开发规范。

## 2.1 后端核心代码（Python + FastAPI）

### 2.1.1 环境变量文件（backend/.env）

```plain text
# 后端基础配置
PORT=8000
HOST=0.0.0.0
RELOAD=True

# OpenAI配置（敏感信息，不提交代码）
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-3.5-turbo
```

### 2.1.2 配置文件（backend/config/settings.py）

```python
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

# 加载.env环境变量
load_dotenv()

class Settings(BaseSettings):
    # 后端服务配置
    PORT: int = int(os.getenv("PORT", 8000))
    HOST: str = os.getenv("HOST", "0.0.0.0")
    RELOAD: bool = os.getenv("RELOAD", "True").lower() == "true"
    
    # OpenAI配置
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

# 实例化配置对象，供其他模块调用
settings = Settings()
```

### 2.1.3 依赖包（backend/requirements.txt）

```plain text
fastapi==0.103.1          # 轻量高效的后端框架
uvicorn==0.23.2           # 运行FastAPI的ASGI服务器
pydantic==2.4.2           # 数据校验
pydantic-settings==2.0.3  # 配置文件管理
python-dotenv==1.0.0      # 加载.env环境变量
openai==1.3.5             # OpenAI API调用（可选，辅助解析）
python-multipart==0.0.6   # 处理表单数据（备用）
```

### 2.1.4 通用工具函数（backend/utils/common.py）

```python
def copy_to_clipboard(text: str) -> bool:
    """
    复制文本到剪贴板（后端备用，主要依赖前端复制功能）
    :param text: 要复制的文本
    :return: 复制成功返回True，失败返回False
    """
    try:
        import pyperclip
        pyperclip.copy(text)
        return True
    except ImportError:
        return False

def format_params(params: dict) -> str:
    """
    格式化参数为JSON字符串，便于前端展示和复制
    :param params: 参数字典
    :return: 格式化后的JSON字符串
    """
    import json
    return json.dumps(params, ensure_ascii=False, indent=2)
```

### 2.1.5 高频人格模板（backend/data/persona_templates.py）

```python
# 10+高频人格模板（MVP重点覆盖专业/医疗场景，完整补充至10个）
PERSONA_TEMPLATES = [
    {
        "id": 1,
        "name": "药品查询专用型",
        "traits": "专业、严谨、不胡编、照本宣科、情绪稳定",
        "big_five": {"O": 20, "C": 95, "E": 10, "A": 70, "N": 0},
        "behavior_rules": "只依据提供的药品说明书回答，不做医疗诊断、不推荐用药、不联想、不推断、不胡编乱造",
        "openai_params": {
            "temperature": 0.1,
            "top_p": 0.1,
            "frequency_penalty": 0.0,
            "presence_penalty": 0.0,
            "max_tokens": 1024
        }
    },
    {
        "id": 2,
        "name": "专业严谨咨询型",
        "traits": "理性、严谨、靠谱、不发散、客观",
        "big_five": {"O": 25, "C": 90, "E": 15, "A": 75, "N": 0},
        "behavior_rules": "仅基于用户提供的信息回答，不编造、不扩展、不情绪化，保持专业距离",
        "openai_params": {
            "temperature": 0.2,
            "top_p": 0.2,
            "frequency_penalty": 0.0,
            "presence_penalty": 0.0,
            "max_tokens": 1024
        }
    },
    {
        "id": 3,
        "name": "治愈陪伴型",
        "traits": "温柔、共情、耐心、安静、情绪稳定",
        "big_five": {"O": 55, "C": 60, "E": 35, "A": 95, "N": 5},
        "behavior_rules": "倾听用户情绪，共情安慰，不评判、不说教，语气柔和，每轮回复1-3句话",
        "openai_params": {
            "temperature": 0.4,
            "top_p": 0.5,
            "frequency_penalty": 0.1,
            "presence_penalty": 0.1,
            "max_tokens": 512
        }
    },
    {
        "id": 4,
        "name": "活泼聊天搭子",
        "traits": "热情、话多、脑洞大、活泼、随性",
        "big_five": {"O": 85, "C": 45, "E": 80, "A": 75, "N": 10},
        "behavior_rules": "语气活泼，话多不啰嗦，带点俏皮，主动回应，不冷场",
        "openai_params": {
            "temperature": 0.8,
            "top_p": 0.8,
            "frequency_penalty": 0.2,
            "presence_penalty": 0.2,
            "max_tokens": 512
        }
    },
    {
        "id": 5,
        "name": "客服专用型",
        "traits": "耐心、礼貌、高效、严谨、不情绪化",
        "big_five": {"O": 30, "C": 85, "E": 40, "A": 90, "N": 0},
        "behavior_rules": "快速响应用户问题，礼貌用语，精准解答，不闲聊、不推诿",
        "openai_params": {
            "temperature": 0.2,
            "top_p": 0.3,
            "frequency_penalty": 0.0,
            "presence_penalty": 0.0,
            "max_tokens": 800
        }
    },
    {
        "id": 6,
        "name": "毒舌顾问型",
        "traits": "犀利、毒舌、直白、理性、不绕弯",
        "big_five": {"O": 60, "C": 70, "E": 65, "A": 40, "N": 20},
        "behavior_rules": "直言不讳，指出问题核心，不委婉、不讨好，语气犀利但不人身攻击",
        "openai_params": {
            "temperature": 0.6,
            "top_p": 0.7,
            "frequency_penalty": 0.1,
            "presence_penalty": 0.1,
            "max_tokens": 600
        }
    },
    {
        "id": 7,
        "name": "游戏NPC型",
        "traits": "代入感强、贴合角色、不跳戏、有互动感",
        "big_five": {"O": 75, "C": 50, "E": 55, "A": 60, "N": 15},
        "behavior_rules": "严格贴合游戏角色设定，语气、措辞符合角色身份，主动引导互动，不泄露游戏外信息",
        "openai_params": {
            "temperature": 0.7,
            "top_p": 0.7,
            "frequency_penalty": 0.2,
            "presence_penalty": 0.2,
            "max_tokens": 700
        }
    },
    {
        "id": 8,
        "name": "法律咨询型",
        "traits": "专业、严谨、合规、客观、不误导",
        "big_five": {"O": 20, "C": 90, "E": 25, "A": 70, "N": 0},
        "behavior_rules": "仅提供基础法律常识，不提供具体法律意见，提示用户咨询专业律师，不编造法律条款",
        "openai_params": {
            "temperature": 0.2,
            "top_p": 0.2,
            "frequency_penalty": 0.0,
            "presence_penalty": 0.0,
            "max_tokens": 1024
        }
    },
    {
        "id": 9,
        "name": "创意文案型",
        "traits": "脑洞大、有创意、语言生动、灵活",
        "big_five": {"O": 90, "C": 55, "E": 70, "A": 80, "N": 10},
        "behavior_rules": "产出有创意、有感染力的文案，贴合需求，不生硬，可灵活调整风格",
        "openai_params": {
            "temperature": 0.8,
            "top_p": 0.9,
            "frequency_penalty": 0.3,
            "presence_penalty": 0.2,
            "max_tokens": 800
        }
    },
    {
        "id": 10,
        "name": "极简回复型",
        "traits": "简洁、高效、不啰嗦、直击重点",
        "big_five": {"O": 15, "C": 80, "E": 10, "A": 60, "N": 0},
        "behavior_rules": "仅回复核心信息，不添加多余内容，每轮回复不超过1句话，直击问题重点",
        "openai_params": {
            "temperature": 0.3,
            "top_p": 0.4,
            "frequency_penalty": 0.0,
            "presence_penalty": 0.0,
            "max_tokens": 200
        }
    }
]
```

### 2.1.6 需求解析Agent（backend/agent/parser_agent.py）

```python
from backend.data.persona_templates import PERSONA_TEMPLATES

class ParserAgent:
    @staticmethod
    def parse_template(template_id: int):
        """解析用户选择的人格模板，返回模板信息，处理模板不存在的异常"""
        for template in PERSONA_TEMPLATES:
            if template["id"] == template_id:
                return template
        return None
    
    @staticmethod
    def parse_natural_language(prompt: str):
        """解析用户自然语言输入，匹配最接近的人格模板（简化逻辑，MVP够用，增加容错）"""
        if not prompt or prompt.strip() == "":
            # 输入为空时，默认返回专业严谨型
            return PERSONA_TEMPLATES[1]
        # 核心关键词匹配，无需复杂NLP，快速落地
        prompt = prompt.lower().strip()
        if "药品" in prompt or "医疗" in prompt:
            return PERSONA_TEMPLATES[0]  # 药品查询专用型
        elif "专业" in prompt or "严谨" in prompt:
            return PERSONA_TEMPLATES[1]  # 专业严谨咨询型
        elif "陪伴" in prompt or "温柔" in prompt or "共情" in prompt:
            return PERSONA_TEMPLATES[2]  # 治愈陪伴型
        elif "活泼" in prompt or "聊天" in prompt or "俏皮" in prompt:
            return PERSONA_TEMPLATES[3]  # 活泼聊天搭子
        elif "客服" in prompt or "咨询" in prompt:
            return PERSONA_TEMPLATES[4]  # 客服专用型
        elif "毒舌" in prompt or "犀利" in prompt:
            return PERSONA_TEMPLATES[5]  # 毒舌顾问型
        elif "游戏" in prompt or "npc" in prompt:
            return PERSONA_TEMPLATES[6]  # 游戏NPC型
        elif "法律" in prompt:
            return PERSONA_TEMPLATES[7]  # 法律咨询型
        elif "文案" in prompt or "创意" in prompt:
            return PERSONA_TEMPLATES[8]  # 创意文案型
        elif "简洁" in prompt or "极简" in prompt:
            return PERSONA_TEMPLATES[9]  # 极简回复型
        else:
            # 默认返回专业严谨型，避免解析失败
            return PERSONA_TEMPLATES[1]
```

### 2.1.7 提示词生成Agent（backend/agent/prompt_agent.py）

```python
class PromptAgent:
    @staticmethod
    def generate_prompt(template: dict, scene: str = "dify"):
        """
        生成结构化人格提示词，适配Dify/API调用场景，增加异常处理
        :param template: 人格模板信息
        :param scene: 场景（dify / api）
        :return: 结构化提示词
        """
        if not template:
            return "请先选择或描述有效的人格需求"
        big_five = template["big_five"]
        # 基础提示词模板（固定结构，适配MVP需求，强化合规约束）
        base_prompt = f"""你是{template['name']}，核心特质：{template['traits']}。
你的大五人格参数：
开放性 O={big_five['O']}%，尽责性 C={big_five['C']}%，外向性 E={big_five['E']}%，宜人性 A={big_five['A']}%，神经质 N={big_five['N']}%。

行为规则：
{template['behavior_rules']}

强约束要求：
1.  严格按照上述人格参数和行为规则回复，绝对不OOC（出戏）；
2.  每轮回复前，先检查是否符合人格要求，不符合则重写；
3.  不添加任何额外信息，不发散、不联想、不编造；
4.  若涉及医疗、法律等敏感领域，需明确提示“仅提供基础信息，不构成专业建议”。"""
        
        # 场景适配：Dify场景无需额外修改，API场景整合到system格式，处理特殊字符转义
        if scene == "api":
            return f"""{{"role": "system", "content": "{base_prompt.replace('"', '\\"').replace('\n', '\\n')}"}}"""
        return base_prompt
```

### 2.1.8 参数匹配Agent（backend/agent/parameter_agent.py）

```python
from backend.config.settings import settings

class ParameterAgent:
    @staticmethod
    def match_parameters(template: dict, scene: str = "dify"):
        """
        匹配OpenAI参数，适配Dify/API调用场景，结合配置文件，增加异常处理
        :param template: 人格模板信息
        :param scene: 场景（dify / api）
        :return: 格式化后的参数
        """
        if not template:
            return {"error": "请先选择或描述有效的人格需求"}
        params = template["openai_params"]
        # 场景适配：Dify返回简化版（仅核心参数），API返回完整JSON，关联配置文件中的模型
        if scene == "dify":
            return {
                "temperature": params["temperature"],
                "top_p": params["top_p"],
                "frequency_penalty": params["frequency_penalty"],
                "presence_penalty": params["presence_penalty"],
                "max_tokens": params["max_tokens"],
                "model": settings.OPENAI_MODEL  # 关联配置文件
            }
        # API场景返回完整请求体JSON（含提示词占位符），便于用户直接复制调用
        return {
            "model": settings.OPENAI_MODEL,
            "temperature": params["temperature"],
            "top_p": params["top_p"],
            "frequency_penalty": params["frequency_penalty"],
            "presence_penalty": params["presence_penalty"],
            "max_tokens": params["max_tokens"],
            "messages": [
                {"role": "system", "content": ""},  # 提示词后续替换
                {"role": "user", "content": "请输入你的问题"}
            ]
        }
```

### 2.1.9 后端入口文件（backend/main.py）

```python
from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware  # 解决跨域问题
from backend.agent.parser_agent import ParserAgent
from backend.agent.prompt_agent import PromptAgent
from backend.agent.parameter_agent import ParameterAgent
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
    scene: str = Query(default="dify", enum=["dify", "api"])

class TemplateInput(BaseModel):
    template_id: int = Query(ge=1, le=10, description="人格模板ID（1-10）")
    scene: str = Query(default="dify", enum=["dify", "api"])

# 路由：获取所有人格模板（供前端下拉选择）
@app.get("/api/templates", summary="获取所有人格模板", description="返回10+高频人格模板，供前端下拉选择")
async def get_templates():
    return {"code": 200, "message": "success", "data": PERSONA_TEMPLATES}

# 路由：通过模板生成方案（核心路由）
@app.post("/api/generate-by-template", summary="按模板生成方案", description="选择模板后，生成对应的提示词和OpenAI参数")
async def generate_by_template(input: TemplateInput):
    # 1. 解析模板
    template = ParserAgent.parse_template(input.template_id)
    if not template:
        raise HTTPException(status_code=400, detail="模板不存在，请选择有效的模板ID（1-10）")
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
            "matched_template": template["name"]
        }
    }

# 路由：通过自然语言生成方案（核心路由）
@app.post("/api/generate-by-nl", summary="按自然语言生成方案", description="输入人格描述，自动匹配模板并生成方案")
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
            "matched_template": template["name"]  # 告知用户匹配的模板，提升体验
        }
    }

# 启动服务（关联配置文件中的端口、主机）
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD
    )
```

## 2.2 前端核心代码（Vue3 + Vite，简化版，完整可运行）

### 2.2.1 前端依赖配置（frontend/package.json）

```json
{
  "name": "persona-agent-frontend",
  "private": true,
  "version": "0.1.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "vue": "^3.4.15"
  },
  "devDependencies": {
    "@vitejs/plugin-vue": "^5.0.3",
    "vite": "^5.0.11"
  }
}
```

### 2.2.2 Vite配置文件（frontend/vite.config.js）

```javascript
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    port: 3000,  // 前端端口，与后端端口区分
    proxy: {
      // 代理后端接口，解决跨域问题（开发环境必备）
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '/api')
      }
    }
  }
})
```

### 2.2.3 前端请求工具（frontend/src/utils/request.js）

```javascript
// 简化请求工具，MVP够用，处理请求异常，适配前端对接
export const request = async (url, method = 'GET', data = {}) => {
  const options = {
    method,
    headers: {
      'Content-Type': 'application/json'
    }
  };
  // POST请求添加请求体
  if (method === 'POST') {
    options.body = JSON.stringify(data);
  }
  try {
    const response = await fetch(url, options);
    const res = await response.json();
    // 处理后端返回的错误
    if (res.code !== 200) {
      alert(`请求失败：${res.message || '未知错误'}`);
      return null;
    }
    return res;
  } catch (error) {
    console.error('请求失败：', error);
    alert('请求失败，请检查后端服务是否启动');
    return null;
  }
};
```

### 2.2.4 输入面板组件（frontend/src/components/InputPanel.vue）

```vue
请选择或描述人格需求<!-- 模板选择 -->
    <select v-model="selectedTemplateId" @<!-- 自然语言输入 -->
    <!-- 场景选择 -->
    <!-- 生成按钮 -->
<button @" :disabled="!selectedTemplateId">按模板生成<button @按描述生成
```

### 2.2.5 输出面板组件（frontend/src/components/OutputPanel.vue）

```vue
生成结果（可直接复制使用）<!-- 匹配的模板提示 -->
    匹配人格模板：{{ result.matched_template }}<!-- 提示词输出 -->
    {{ result.prompt }}<button @一键复制<!-- 参数输出 -->
    {{ JSON.stringify(result.params, null, 2) }}<button @, null, 2))">一键复制<!-- API调用示例（仅API场景显示） -->
    {{ result.api_example }}<button @一键复制
    请选择模板或输入人格描述，点击生成按钮获取结果

```

### 2.2.6 主页面组件（frontend/src/App.vue）

```vue
人格提示词与OpenAI参数生成工具（MVP版）<InputPanel @generate-result="handleGenerateResult" />
    <OutputPanel :result="result" />
  
```

### 2.2.7 前端入口文件（frontend/src/main.js）

```javascript
import { createApp } from 'vue'
import './style.css'
import App from './App.vue'

createApp(App).mount('#app')
```

### 2.2.8 前端样式文件（frontend/src/style.css）

```css
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  background: #f8f9fa;
  font-size: 14px;
  color: #333;
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 20px;
}
```

### 2.2.9 前端入口HTML（frontend/public/index.html）

```html
<!DOCTYPE html>
人格提示词与OpenAI参数生成工具
```

# 三、补充说明

1. 代码使用说明：所有代码可直接复制到对应目录，后端安装依赖（pip install -r requirements.txt）、前端安装依赖（npm install）后，分别启动后端（python backend/main.py）和前端（npm run dev），即可正常运行。

2. 敏感信息处理：.env文件需自行填写OpenAI密钥，该文件不提交到代码仓库，避免密钥泄露。

3. 场景适配：代码已适配Dify和OpenAI API两大高频场景，生成的提示词和参数可直接复制使用，无需二次修改。

> （注：文档部分内容可能由 AI 生成）
