from pykeepass import PyKeePass
from pykeepass import exceptions
import sys
import logging
from configs.KeePass_config import Titles as tt, KPpath

logger = logging.getLogger('PrognoZTM.credntials')

class PassDB:

    def __init__(self, masterpass):
        logger.info('Requesting KeePass database data')
        try:
            self.kp = PyKeePass(KPpath.PATH, password=masterpass)
            logger.info('Credentials database fetched')
        except FileNotFoundError:
            logger.error(f'KDBX file {KPpath.PATH} does not exist')
            print(f'KDBX file {KPpath.PATH} does not exist')
            sys.exit()
        except exceptions.CredentialsIntegrityError:
            logger.error(f'Unauthorized access to {KPpath.PATH} attempt!')
            print('Wrong password - try again')
            sys.exit()

    def get_credential(self,credential_name):
        logger.debug(f'Requesting {credential_name} credentials')
        try:
            entry = self.kp.find_entries(title= tt.names[credential_name], first=True)
            logger.debug(f'{credential_name} credentials found')
            return entry.username, entry.password
        except KeyError:
            logger.error(f'{credential_name} not found in {KPpath.PATH}. Please provide correct name of entry.')
            print(f'{credential_name} not found in {KPpath.PATH}. Please provide correct name of entry.')
            sys.exit()
