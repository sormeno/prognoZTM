import logging
import json
import sys
import libs.lib_api.api_wrapper as api_wrap

logger = logging.getLogger('PrognoZTM.ZTM')

class LiveDataClient:

    def __init__ (self,keepassDB,keepassEntry,api_config):

        logger.info(f'Creating API client for {keepassEntry}')
        self.endpoint, self.api_key = keepassDB.get_credential(keepassEntry)
        self.api_atrributes  = api_config.API_ATTRIBUTES
        logger.info(f'API client for {keepassEntry} created with endpoint {self.endpoint} and apikey={self.api_key}')

        logger.info(f'Testing API client {keepassEntry} with {self.endpoint} and apikey={self.api_key}')
        test_api = api_wrap.call_api(
                self.endpoint,
                self.api_atrributes['API_ATTR_NAME'],
                self.api_key
            )
        try:
            if test_api[api_config.INVALID_API_KEY_CHECK['label']] == api_config.INVALID_API_KEY_CHECK['result']:
                logger.error(f'API access to {self.endpoint} with apikey={self.api_key} denied. Please check {type(api_config).__name__} API KEY')
                print(f'API access to {self.endpoint} with apikey={self.api_key} denied. Please check {type(api_config).__name__} API KEY')
                sys.exit()
            else:
                logger.info(f'Connected to API {self.endpoint} with provided apikey!')
                print(f'Connected to API {self.endpoint} with provided apikey!')
        except KeyError:
            print(f'Service {self.endpoint} is not available')
            sys.exit()



    def get_data(self, params=[]):
        logger.debug(f'Passing params {params} to URL builder.')
        try:
            data = api_wrap.call_api(
                self.endpoint,
                self.api_atrributes['API_ATTR_NAME'],
                self.api_key,
                params
            )
            logger.debug(f'Data fetched from URL builder. Data type is {data.__class__}')
        except KeyError:
            data = json.loads({'No data found or error occured'})
            logger.error('No data found or error occured')
        return data

