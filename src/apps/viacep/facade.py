from src.apps.shared.response import CustomResponse
from src.apps.viacep.service import ViaCEPService
from src.log import get_logger

logger = get_logger(__name__)

class ViaCepFacade:
    """
    class responsible for a viaCEP Facade
    """
    @staticmethod
    async def get_address_by_cep(cep: int)-> CustomResponse:
        """
        Class responsible for a get address by cep
        :param cep: cep
        :return: custom response
        """
        try:
            logger.info('Facade: Initializing get_address_by_cep')

            get_cep_data = ViaCEPService.get(cep=cep)


            if get_cep_data['status'] == 'success':
                parse_response = ViaCEPService.parse_data(get_cep_data['data'])
                logger.info('Get address by cep success')
                return CustomResponse.success(
                    message=get_cep_data['message'],
                    data=parse_response
                )
            logger.warning('Error in locate address via cep')
            return CustomResponse.failure(message=get_cep_data['message'])
        except Exception as err:
            logger.error("Error find address by cep: %s", err)
            return CustomResponse.failure(message=f"Error find address by cep: {str(err)}")