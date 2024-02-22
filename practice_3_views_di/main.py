from fastapi import FastAPI, Depends

app = FastAPI()


def get_data():
    db = {"data": "This is some data"}
    return db


def get_user():
    user = {"username": "Nega Bob"}
    return user


class SomeDependency:
    def __init__(self):
        self.message = "This is some dependency"

    def __call__(self):
        return self.message


@app.get("/view1")
def view1(db=Depends(get_data)):
    return {"message": "This is view 1", "db": db}


@app.get("/view2")
def view2(user=Depends(get_user)):
    return {"message": "This is view 2", "user": user}


@app.get("/view3")
def view3(some_dependency=Depends(SomeDependency())):
    return {"message": "This is view 3", "some_dependency": some_dependency}
