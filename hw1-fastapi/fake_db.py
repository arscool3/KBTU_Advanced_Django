from datetime import datetime

from films.schemas import Film


films = [
    Film(id=1, name="HZ", description="djsfjsdfkjs", rating=2, release_date=datetime.now()),
    Film(id=2, name="HZ1", description="djsfjsdfkjs", rating=4, release_date=datetime.now()),
    Film(id=3, name="HZ2", description="djsfjsdfkjs", rating=4, release_date=datetime.now()),
    Film(id=4, name="HZ3", description="djsfjsdfkjs", rating=9, release_date=datetime.now()),
    Film(id=5, name="HZ4", description="djsfjsdfkjs", rating=5, release_date=datetime.now()),
]
