from fastapi import FastAPI

def create_app() -> FastAPI:
    app = FastAPI()
    
    from api.views.v1.translate import translate_v1
    
    app.include_router(translate_v1)
    
    return app