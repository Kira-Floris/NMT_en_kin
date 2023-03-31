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
    src, trg, text = request.src, request.trg, request.text
    if src=="en" and trg=="kin":
        response = shell_translate(text, "models/onmt_v1/en_kin_model_step_20000.pt")
    elif src=="kin" and trg=="en":
        response = shell_translate(text, "models/onmt_v1/kin_en_model_step_20000.pt")
    else:
        response = ""
    
    return TranslateTextResponseSchema(translation=response)