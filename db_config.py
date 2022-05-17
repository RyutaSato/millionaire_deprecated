import os

# from postgresql_connect import PostgreConnect

SECURITY_KEY = os.environ.get('SECURITY_KEY')
DIALECT = 'postgresql'
HOST = 'localhost'
PORT = '5432'
CHARSET_TYPE = 'utf8mb4'
db_name = 'postgresql'

# This code is DEPLICATED
# def db_config():
#     pg = PostgreConnect()
#     print(f'connected {pg.get_table_list()}')


from sqlalchemy import create_engine
def db_config():
    return create_engine(f"{DIALECT}://rsato:{SECURITY_KEY}@{HOST}:{PORT}/{db_name}?charset={CHARSET_TYPE}")
