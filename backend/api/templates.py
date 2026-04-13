from fastapi import APIRouter

from backend.data.persona_templates import PERSONA_TEMPLATES

router = APIRouter()


@router.get(
    "/templates",
    summary="获取所有人格模板",
    description="返回10+高频人格模板，供前端下拉选择",
)
async def get_templates():
    return {"code": 200, "message": "success", "data": PERSONA_TEMPLATES}
