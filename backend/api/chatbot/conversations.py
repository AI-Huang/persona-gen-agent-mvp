from fastapi import APIRouter, HTTPException

from backend.api.chatbot.chat import chatbot_instances

router = APIRouter()


@router.get(
    "/conversations/{chatbot_id}",
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
