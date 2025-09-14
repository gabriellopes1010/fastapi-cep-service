from fastapi import APIRouter,status
from starlette.responses import JSONResponse

from src.apps.shared.serialize import SerializationFilter
from src.apps.viacep.facade import ViaCepFacade
from src.log import get_logger

logger = get_logger(__name__)

router = APIRouter(
    prefix='/v1',
    tags=['viaCEP']
)

@router.get('/cep/{cep}')
async def get_address_by_cep(cep: int):
    """
    Method responsible for a get address by cep
    :param cep: cep number
    :return: dict content data
    """
    logger.info('Resource: Starting get address by cep')

    get_address_data = await ViaCepFacade.get_address_by_cep(cep=cep)
    if get_address_data['status'] == 'success':
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                'status': 'success',
                'message': 'Get address successful',
                'data': SerializationFilter.response(get_address_data['data'])
            }
        )
    logger.error("Resource:get address failed")
    return JSONResponse(
        status_code=status.HTTP_302_FOUND,
        content={
            "status": "failure",
            "message": "get address failed"
        }
    )