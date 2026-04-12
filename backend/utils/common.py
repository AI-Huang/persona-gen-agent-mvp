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
