from datetime import timedelta
from auth import create_access_token


def access_token_generate_handler(data):
    access_token = create_access_token(str(data['email']), str(data['id']), timedelta(minutes=20))
    return {
        'access_token': access_token,
        'token_type': 'bearer'
    }
