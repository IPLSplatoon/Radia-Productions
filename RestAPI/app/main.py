from fastapi import Request, FastAPI
from fastapi.openapi.utils import get_openapi
import os
import logging
from app.database import DBConnector
from app.routers import commentators, live, organisation, mocking
# import uvicorn

debug = os.getenv("DEBUG")

# Initialize logging
logging.basicConfig(
    level=(
        logging.DEBUG if debug else logging.INFO
    ),
    format='\033[31m%(levelname)s\033[0m \033[90min\033[0m \033[33m%(filename)s\033[0m \033[90mon\033[0m %(asctime)s\033[90m:\033[0m %(message)s',
    datefmt='\033[32m%m/%d/%Y\033[0m \033[90mat\033[0m \033[32m%H:%M:%S\033[0m'
)
logging.getLogger("fastapi").setLevel(logging.ERROR)
logging.getLogger("uvicorn").setLevel(logging.WARNING)
logging.getLogger("asyncio").setLevel(logging.WARNING)
logging.getLogger("motor").setLevel(logging.ERROR)

logging.getLogger(__name__)

if debug:
    logging.info("static.env - 'DEBUG' key found. Running in debug mode, do not use in production.")


# Optionally initialize sentry
def initialize_sentry(sentry_env):
    import sentry_sdk

    sentry_sdk.init(
        dsn="https://e62712051c0141f3a8442b4eea1166a9@o83253.ingest.sentry.io/5768573",
        environment=sentry_env
    )


if sentry_env := os.getenv("SENTRY"):
    initialize_sentry(sentry_env)
    logging.info("static.env - 'SENTRY' key found. Initializing Sentry")
else:
    logging.info("static.env - 'SENTRY' key not found. Skipping Sentry.")

# Load Database
if not (mongo_uri := os.getenv("MONGODBURI")):
    logging.error("static.env - 'MONGODBURI' key not found. Cannot start bot.")
    raise EnvironmentError


def create_app():
    database = DBConnector(mongo_uri, "radiaTwitch")

    app = FastAPI(
        title="Radia Production API",
        description="Inkling Performance Labs Production API Service",
        version="1.1.0",
        docs_url=None,
        redoc_url="/docs"
    )

    app.add_event_handler("startup", database.connect_db)
    app.add_event_handler("shutdown", database.close_mongo_connection)

    app.include_router(
        commentators.router,
        prefix="/commentators",
        tags=["commentators"]
    )

    app.include_router(
        live.router,
        prefix="/live",
        tags=['live']
    )

    app.include_router(
        organisation.router,
        prefix="/organisation",
        tags=['organisation']
    )

    app.include_router(
        mocking.router,
        prefix="/mock",
        tags=['mocking']
    )

    @app.middleware("http")
    async def db_session_middleware(request: Request, call_next):
        request.state.db = database
        response = await call_next(request)
        return response

    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema
        openapi_schema = get_openapi(
            title="Radia Production API",
            description="Inkling Performance Labs Production API Service. <br>"
                        "URL: https://github.com/IPLSplatoon/Radia-Productions | Documentation Licence: CC-BY 4.0",
            version="1.1.0",
            routes=app.routes,
            tags=[
                {
                    "name": "commentators",
                    "description": "Retrieve and set details on commentators"
                },
                {
                    "name": "live",
                    "description": "Retrieve on commentators currently live in a Discord Guild/Twitch Channel"
                },
                {
                    "name": "organisation",
                    "description": "Retrieve information about a Discord Guild/Twitch Channel settings"
                },
                {
                    "name": "mocking",
                    "description": "Used for mocking other endpoints in testing scenario"
                }
            ]
        )
        security = openapi_schema["components"]["securitySchemes"]
        security["APIKeyHeader"]["description"] = "An API Authorization token must be provided to be able to use an " \
                                                  "endpoint. <br> To do this set you HEADER can be set as like the " \
                                                  "following. `Authorization: Your_Authorization_Key` " \
                                                  "<br> A Key can be issued by IPL Production Team."
        openapi_schema["info"]["x-logo"] = {
            "url": "https://store.iplabs.work/production.png",
            "href": "https://iplabs.work",
            "altText": "Inkling Performance Labs Productions"
        }
        app.openapi_schema = openapi_schema
        return app.openapi_schema

    app.openapi = custom_openapi
    return app


app = create_app()

# if __name__ == "__main__":
#     uvicorn.run(app, host="localhost", port=2000)
