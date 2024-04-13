# Simulating a database with a list
fake_database = []


def insert_to_db(data):
    fake_database.append(data)


def get_from_db(coin):
    return [record for record in fake_database if record['coin'] == coin]
