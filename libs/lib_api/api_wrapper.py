import requests
import logging

logger = logging.getLogger('PrognoZTM.api')

def call_api(endpoint, api_key_attr_name, api_key ,params=[]):
    url = f'{endpoint}?{api_key_attr_name}={api_key}'
    for param in params:
        url = f'{url}&{param[0]}={param[1]}'
        logger.debug(f'URL appended with param {param[0]}={param[1]}')
    logger.debug(f'Following URL has been generated: {url}')
    logger.debug(f'Requesting data with generated URL')
    try:
        data = requests.get(url).json()
        logger.debug(f'Successful data fetch from: {url}')
    except Exception as e:
        logger.error(f'Error {e} appeared when requesting data. No data retrieved.', exc_info=True)
        data = {}
    return data