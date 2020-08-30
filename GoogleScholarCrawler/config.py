import configparser

config = configparser.ConfigParser()
config.read('config.ini', 'utf8')


def get_mysql():
    conn_params = {
        'host': config['MySQL']['host'],
        'port': int(config['MySQL'].get('port', '3306')),
        'user': config['MySQL']['user'],
        'password': config['MySQL']['password'],
        'database': config['MySQL']['database'],
        'charset': config['MySQL'].get('charset', 'utf8')
    }
    table = config['MySQL']['table']
    return conn_params, table


def get_proxy():
    return {
        'host': config['Proxy']['host'],
        'port': int(config['Proxy']['port'])
    }
