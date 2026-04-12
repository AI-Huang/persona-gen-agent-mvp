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
