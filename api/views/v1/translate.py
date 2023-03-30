from fastapi import APIRouter, HTTPException, status

# schema
from api.schemas.v1.translate import (
    TranslateTextRequestSchema,
    TranslateTextResponseSchema
)

from utils.onmt.v1.parse import translate as shell_translate

translate_v1 = APIRouter(prefix="/api/v1/translate")

DEVDEBUG = True

@translate_v1.post("")
async def translate(
    request: TranslateTextRequestSchema
):
    response = shell_translate("trying", "models/onmt_v1/en_kin_model_step_20000.pt")
    return TranslateTextResponseSchema(translation=response)