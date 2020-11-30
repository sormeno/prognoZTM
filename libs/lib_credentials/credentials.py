from pykeepass import PyKeePass
from pykeepass import exceptions
import json
import sys
import logging
from configs.passwords_config import Titles as tt, KPpath, JSONpasspath

logger = logging.getLogger('PrognoZTM.credntials')

class KeepassDB: #class for keepass file

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


class JSONpassDB: #class for simple .json file

    def __init__(self, cred_path = JSONpasspath.PATH):
        logger.info('Loading credentials JSON')
        try:
            self.cred_path = cred_path
            with open(cred_path, 'r') as json_file:
                self.kp = json.load(json_file)
            logger.info('Credentials database fetched')
        except FileNotFoundError:
            logger.error(f'JSON file {cred_path} does not exist')
            print(f'JSON file {cred_path} does not exist')
            sys.exit()

    def get_credential(self,credential_name):
        logger.debug(f'Requesting {credential_name} credentials')
        try:
            entry = self.kp.get(tt.names[credential_name])
            logger.debug(f'{credential_name} credentials found')
            return entry.get('username'), entry.get('password')
        except KeyError:
            logger.error(f'{credential_name} not found in {self.cred_path}. Please provide correct name of entry.')
            print(f'{credential_name} not found in {self.cred_path}. Please provide correct name of entry.')
            sys.exit()