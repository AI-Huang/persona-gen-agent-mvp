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
                "model": settings.OPENAI_MODEL,  # 关联配置文件
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
                {"role": "user", "content": "请输入你的问题"},
            ],
        }
