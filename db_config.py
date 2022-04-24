from postgresql_connect import PostgreConnect
def db_config():
    pg = PostgreConnect(password='Q2w3oert192837', )
    print(f'connected {pg.get_table_list()}')

