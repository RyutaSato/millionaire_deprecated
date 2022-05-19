import configparser


def w_config():
    config = configparser.ConfigParser()
    config['DEFAULT'] = {
        'debug': True
    }
    config['db_server'] = {
        'dialect': 'postgresql',
        'host': 'localhost',
        'port': 5432,
        'charset': 'utf8',
        'db_name': 'postgresql'
    }

    config['millionaire'] = {
        'number': 4

    }

    with open('config.ini', 'w') as config_file:
        config.write(config_file)


def r_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    print(config['db_server']['host'])

if __name__ == '__main__':
    w_config()
    r_config()
