from fastapi import FastAPI, status
from starlette.responses import JSONResponse

from src.apps.shared.serialize import SerializationFilter
from src.apps.viacep.viacep import ViaCepClass
from src.log import get_logger

logger = get_logger(__name__)
app = FastAPI()

@app.get('/')
def read_root():
    return {'hello': 'world'}

@app.get('/cep/{cep}')
async def get_address_by_cep(cep: int):
    try:
        get_cep = await ViaCepClass.get(cep=cep)
        if get_cep['status'] == 'success':
            logger.info('CEP found with success')
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    'status': 'success',
                    'message': 'get cep finished with success',
                    'data': SerializationFilter.response(get_cep['data'])
                }
            )
        logger.warning('Cep not found.')
        return JSONResponse(
            status_code=status.HTTP_302_FOUND,
            content={
                'status': 'failure',
                'message': 'not get location by cep'
            }
        )

    except Exception as err:
        pass