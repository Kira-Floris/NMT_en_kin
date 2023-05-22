from fastapi import APIRouter, HTTPException, status

# schema
from api.schemas.v1.translate import (
    TranslateTextRequestSchema,
    TranslateTextResponseSchema
)

from utils.onmt.v1.parse import translate as shell_translate

translate_v1 = APIRouter(prefix="/api/v1/translate")

DEVDEBUG = True

en_rw_model = "models/onmt_other/transformer/en_kin_model_step_12000.pt"
rw_en_model = "models/onmt_other/transformer/rw_en_model_step_5000.pt"

@translate_v1.post("")
async def translate(
    request: TranslateTextRequestSchema
):
    src, trg, text = request.src, request.trg, request.text
    if src=="en" and trg=="kin":
        response = shell_translate(text, "models/onmt_other/transformer/en_kin_model_step_12000.pt", onmt_version='v1')
    elif src=="kin" and trg=="en":
        response = shell_translate(text, "models/onmt_v1/kin_en_model_step_20000.pt", onmt_version='v1')
    else:
        response = ""
    
    return TranslateTextResponseSchema(translation=response)