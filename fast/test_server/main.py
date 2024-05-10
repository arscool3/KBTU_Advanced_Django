import random
import time

from fastapi import FastAPI
#PG-13: Some Material May Be Inappropriate For Children Under 13
app = FastAPI()

def test(name: str):
    print("hallo")
    return not name == "Arslan"

def test_pg13(name: str):
    non_kid_friendly_genres = [
        "Horror",
        "Erotica",
        "Thriller",
        "Crime",
        "Psychological thriller",
        "Suspense",
        "Dark Fantasy",
        "Noir",
        "Gothic",
        "Urban Fantasy",
        "Erotic Thriller",
        "Absurdist Fiction"
    ]
    print("test_pg13")
    return name in non_kid_friendly_genres

@app.get("/pg13")
def pg13_endpoint(name: str):
    print("pg13_endpoint")
    #returning true means the book is not kid friendly
    return  test_pg13(name)


@app.get("/drug")
def drug_endpoint(name: str):
    time.sleep(5)
    return test(name)


@app.get("/psycho")
def psycho_endpoint(name: str):
    time.sleep(5)
    return test(name)


@app.get("/crime")
def crime_endpoint(name: str):
    time.sleep(5)
    return test(name)