import libs.lib_credentials.credentials as cred
import db_backup.db_backup_config as cfg
import os
import logging
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%d-%m-%Y %H:%M:%S',
    level=logging.INFO,
    filename='C:\\Users\\filip\\OneDrive\\Dokumenty\\Programowanie\\Python Projects\\PrognoZTM\\db_backup\\logs.txt'
    )
dbdump_logger = logging.getLogger('DBdump')
dbdump_logger.info('Started DBdump!')


dbdump_logger.info(f'{cfg.mysqldump_path} will be used for dump')
dbdump_logger.info(f'{cfg.schemas_for_backup} will be dumped')
dbdump_logger.info(f'DDLs will be saved to {cfg.target_dir}')

kp = cred.JSONpassDB(cred_path = cfg.creds)
user, pwd = kp.get_credential('MYSQL_DUMP')

cmds = [
    f'{cfg.mysqldump_path} -d -u {user} -p{pwd} -h localhost -B {cfg.schemas_for_backup} > {cfg.DDL_path}',
    f'{cfg.mysqldump_path} --no-create-info -d -u {user} -p{pwd} -h localhost -B mysql --tables db user columns_priv tables_priv procs_priv > {cfg.users_path}',

]

for cmd in cmds:
    try:
        dbdump_logger.info(f'Running {cmd}')
        os.system(cmd)
        dbdump_logger.info(f'Command has run successfully')
    except:
        dbdump_logger.error(f'Cannot run command {cmd}',  exc_info= True)
        dbdump_logger.error(f'Command execution skipped')
        raise



