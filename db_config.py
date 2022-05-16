import os

from postgresql_connect import PostgreConnect

SECURITY_KEY = os.environ.get('SECURITY_KEY')
DIALECT = 'postgresql'
HOST = 'localhost'
PORT = '5432'
CHARSET_TYPE = 'utf8mb4'
db_name = 'postgresql'
def db_config():
    pg = PostgreConnect()
    print(f'connected {pg.get_table_list()}')


from sqlalchemy import create_engine
db_engine = create_engine(f"{DIALECT}://rsato:{SECURITY_KEY}@{HOST}:{PORT}/{db_name}?charset={CHARSET_TYPE}")
