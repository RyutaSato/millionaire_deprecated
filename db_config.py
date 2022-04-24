import os

from postgresql_connect import PostgreConnect
def db_config():
    pg = PostgreConnect(password=os.environ.get('SECURITY_KEY'))
    print(f'connected {pg.get_table_list()}')

