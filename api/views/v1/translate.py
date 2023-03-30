from fastapi import APIRouter, HTTPException, status

# schema
from NMT_en_kin.api.schemas.v1.translate import (
    TranslateTextRequestSchema,
    TranslateTextResponseSchema
)

translate_v1 = APIRouter(prefix="/api/v1/translate")

DEVDEBUG = True

@translate_v1.post("")
async def translate(
    request: TranslateTextRequestSchema
):
    response = ""
    return TranslateTextResponseSchema(translation=response)