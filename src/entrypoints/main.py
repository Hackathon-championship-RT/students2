from src.api import routers
from src.bootstrap import Bootstrap

bootstraped = Bootstrap()()
api = bootstraped.fast_api
api.include_router(routers.auth)
