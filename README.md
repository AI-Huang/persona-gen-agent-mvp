# 人格提示词与OpenAI参数生成AI Agent (MVP)

核心定位：一款「输入人格需求，输出可直接复制使用」的AI工具——用户只需描述人格类型（如专业药品助手、治愈陪伴、毒舌顾问），Agent自动生成结构化人格提示词（含大五参数/MBTI）、配套OpenAI API参数，且支持一键复制，适配Dify、直接API调用等核心场景，主打"零门槛、高适配、可落地"。

## 核心功能

- **人格模板选择**：提供10个预设人格模板，涵盖专业、医疗、陪伴等多种场景
- **自然语言解析**：支持用户输入自然语言描述，自动匹配最接近的人格模板
- **提示词生成**：生成结构化的人格提示词，包含大五人格参数和行为规则
- **参数匹配**：根据人格模板匹配最佳的OpenAI API参数
- **场景适配**：支持Dify和OpenAI API两种场景
- **一键复制**：生成的提示词和参数可直接复制使用

## 项目结构

```bash
persona-agent-mvp/
├── backend/                # Python后端（FastAPI）
│   ├── agent/              # Agent核心逻辑
│   ├── config/             # 配置文件
│   ├── data/               # 静态数据
│   ├── utils/              # 工具函数
│   ├── main.py             # 入口文件
│   ├── requirements.txt    # 依赖包清单
│   └── .env                # 环境变量文件
├── frontend/               # Vue3前端
│   ├── public/             # 静态资源
│   ├── src/                # 前端核心代码
│   ├── package.json        # 依赖包清单
│   └── vite.config.js      # Vite配置文件
└── README.md               # 项目说明文档
```

### 技术栈

- 后端: Python + FastAPI + Pydantic
- 前端: Vue3 + Vite
- 依赖管理: uv（Python） + npm（前端）

## Usage

### 安装依赖

`openai>=2.31.0`

```bash
# 使用uv安装后端依赖
cd persona-agent-mvp
uv sync
```

```bash
# 安装前端依赖
cd persona-agent-mvp/frontend
npm install
```

### 1. 配置环境变量

在 `backend/.env` 文件中配置OpenAI API密钥：

```bash
# 后端基础配置
PORT=8000
HOST=0.0.0.0
RELOAD=True

# OpenAI配置（敏感信息，不提交代码）
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-3.5-turbo
```

### 2. 启动后端服务

```bash
# 启动后端服务
cd persona-agent-mvp
uv run uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

后端服务将运行在 `http://0.0.0.0:8000`

### 3. 启动前端服务

```bash
# 启动前端服务
cd persona-agent-mvp/frontend
npm run dev
```

前端服务将运行在 `http://localhost:3000/`

### 4. 使用系统

1. **访问前端界面**：打开浏览器，访问 `http://localhost:3000/`
2. **选择人格模板**：从下拉菜单中选择一个预设模板，或在文本框中描述人格需求
3. **选择使用场景**：选择Dify或OpenAI API场景
4. **点击生成按钮**：按模板生成或按描述生成
5. **复制结果**：使用一键复制功能复制生成的提示词和参数
6. **使用结果**：将复制的内容粘贴到Dify或直接用于OpenAI API调用

### 5. API端点

- `GET /api/templates` - 获取人格模板列表
- `POST /api/generate-by-template` - 按模板生成方案
- `POST /api/generate-by-nl` - 按自然语言生成方案
