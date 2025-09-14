from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from src.apps.viacep import resource as viacep
from .log import get_logger, set_context

logger = get_logger(__name__)
app = FastAPI(
    title='Get address Via cep',
    version='1.0.0',
    docs_url='/documentation',
    redoc_url=None
)

origins = [
    "http://0.0.0.0:8000",
    "http://localhost:8000",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """
    Event that will be executed when the application starts
    :return:
    """
    app.include_router(viacep.router)


async def add_request_id_header(request: Request):
    """
    Add X-Request-ID to each response, from FastAPI
    :param request:
    :param call_next:
    :return: X-Request-ID
    """
    x_request = request.headers.get('X-Request-ID', "development")
    set_context(x_request)


@app.exception_handler(Exception)
def global_exception_handler(exc: Exception):
    """
    log your exception here
    you can also request details by using request object
    """
    logger.error("Erro interno: %s",exc )

    return JSONResponse(content={"message":"Um erro interno ocorreu!"},
    status_code=500)
