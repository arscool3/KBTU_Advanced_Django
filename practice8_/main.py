from fastapi import FastAPI
app=FastAPI()

students=[
    'aruka',
    'oli',
    'alisa'
]
@app.get('/students')
def get_students()->list:
    return students