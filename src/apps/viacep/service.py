from src.apps.core.models.viacep_model import ViaCEPBase
from src.log import get_logger
import requests

logger = get_logger(__name__)

class ViaCEPService:
    """
    Class responsible for a viaCEp Service
    """
    @staticmethod
    def get(cep: int):
        """
        method responsible for a get location by cep
        :return: dictionary content information
        """
        try:
            url = f'https://viacep.com.br/ws/{cep}/json/'

            response = requests.get(url=url)

            if response.status_code == 200:
                logger.warning(response.json())
                return {
                    'status': 'success',
                    'message': 'location found with success',
                    'data': response.json()
                }
            return {
                'status': 'failure',
                'message': 'cep not found',
            }
        except Exception as err:
            return {
                'status': 'failure',
                'message': f'An error occurred: {str(err)}'
            }

    @staticmethod
    def parse_data(data: dict) -> ViaCEPBase:
        """
        Method responsible for parsing ViaCEP API data to ViaCEPBase model
        :param data: Raw data from ViaCEP API
        :return: ViaCEPBase model instance
        """
        return ViaCEPBase(
            cep=data.get('cep'),
            street=data.get('logradouro'),
            supplement=data.get('complemento'),
            unit=data.get('unidade'),
            neighborhood=data.get('bairro'),
            location=data.get('localidade'),
            uf=data.get('uf'),
            state=data.get('estado'),
            region=data.get('regiao'),
            ibge=data.get('ibge'),
            gia=data.get('gia'),
            ddd=data.get('ddd'),
            siafi=data.get('siafi')
        )