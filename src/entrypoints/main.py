from src.api.auth.routes import router as auth_router
from src.api.result.routes import router as result_router
from src.bootstrap import Bootstrap

bootstraped = Bootstrap()()
api = bootstraped.fast_api
api.include_router(auth_router)
api.include_router(result_router)
