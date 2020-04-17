import requests
import logging
import sys

logger = logging.getLogger('PrognoZTM.api')

def call_api(endpoint, api_key_attr_name, api_key, attributes = None ,params=[]):
    url = f'{endpoint}?{api_key_attr_name}={api_key}'
    for param in params:
        try:
            url = f'{url}&{attributes[param[0]]}={param[1]}'
            logger.debug(f'URL appended with param {attributes[param[0]]}={param[1]}')
        except KeyError:
            logger.error(f'Attribute name \'{param[0]}\' not found in api_config attributes list')
            sys.exit()

    logger.debug(f'Following URL has been generated: {url}')
    logger.debug(f'Requesting data with generated URL')

    try:
        data = requests.get(url).json()
        logger.debug(f'Successful data fetch from: {url}')
    except Exception as e:
        logger.error(f'Error {e} appeared when requesting data. No data retrieved.', exc_info=True)
        data = {}
    return data