import requests


class ViaCepClass:

    @staticmethod
    async def get(cep: int):
        """
        method responsible for a get location by cep
        :return: dictionary content information
        """
        try:
            url = f'https://viacep.com.br/ws/{cep}/json/'

            response = requests.get(url=url)

            if response.status_code == 200:
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




