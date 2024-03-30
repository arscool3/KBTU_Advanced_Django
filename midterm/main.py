from fastapi import FastAPI, Depends

import models as db
import punq
from database import session
from schemas import User, CreateUser, Course, CreateCourse, Video, CreateVideo, Review, CreateReview, Purchase, \
    CreatePurchase, Progress, CreateProgress, BaseUser
from repository import UserRepository, CourseRepository, VideoRepository, ReviewRepository, PurchaseRepository, ProgressRepository, AbcRepository

app = FastAPI()

class Dependency:
    def __init__(self, repo: AbcRepository):
        self.repo = repo

    def __call__(self, id: int) -> User | Course | Video | Review | Purchase | Progress:
        return self.repo.get_by_id(id)

def get_container(repository: type[AbcRepository]) -> punq.Container:
    container = punq.Container()
    container.register(AbcRepository, repository, instance=repository(session=session))
    container.register(Dependency)
    return container

@app.post("/users")
def add_user(user: CreateUser) -> str:
    session.add(db.User(**user.dict()))
    session.commit()
    session.close()
    return "User added"

@app.post("/courses")
def add_course(course: CreateCourse) -> str:
    session.add(db.Course(**course.dict()))
    session.commit()
    session.close()
    return "Course added"

@app.post("/videos")
def add_video(video: CreateVideo) -> str:
    session.add(db.Video(**video.dict()))
    session.commit()
    session.close()
    return "Video added"

@app.post("/reviews")
def add_review(review: CreateReview) -> str:
    session.add(db.Review(**review.dict()))
    session.commit()
    session.close()
    return "Review added"

@app.post("/purchases")
def add_purchase(purchase: CreatePurchase) -> str:
    session.add(db.Purchase(**purchase.dict()))
    user = session.get(db.User, purchase.user_id)
    course = session.get(db.Course, purchase.course_id)
    if user and course:
        user.courses.append(course)

    session.commit()
    session.close()
    return "Purchase added and course associated with user"


@app.post("/progress")
def add_progress(progress: CreateProgress) -> str:
    session.add(db.Progress(**progress.dict()))
    session.commit()
    session.close()
    return "Progress added"

def get_user_courses_dependency(user_id: int):
    user = session.get(db.User, user_id)
    return user.courses if user else []

def get_course_users_dependency(course_id: int):
    course = session.get(db.Course, course_id)
    return [BaseUser(name=user.name, email=user.email) for user in course.users] if course else []

def get_all_courses_dependency():
    return session.query(db.Course).all()

def get_all_users_dependency():
    return session.query(db.User).all()

@app.get("/users/{user_id}/courses")
def get_user_courses(user_id: int, courses: list[Course] = Depends(get_user_courses_dependency)):
    return courses

@app.get("/courses/{course_id}/users")
def get_course_users(course_id: int, users: list[BaseUser] = Depends(get_course_users_dependency)):
    return users

@app.get("/all_courses")
def get_all_courses(courses: list[Course] = Depends(get_all_courses_dependency)):
    return courses

@app.get("/all_users")
def get_all_users(users: list[User] = Depends(get_all_users_dependency)):
    return users


@app.get("/users/{user_id}/courses")
def get_user_courses(user_id: int):
    user = session.get(db.User, user_id)
    if user:
        return user.courses
    return "No such user!"

@app.get("/courses/{course_id}/users")
def get_course_users(course_id: int):
    course = session.get(db.Course, course_id)
    if course:
        return [BaseUser(name=user.name, email=user.email) for user in course.users]
    return "No such course!"

@app.get("/all_courses")
def get_all_courses():
    courses = session.query(db.Course).all()
    return courses

@app.get("/all_users")
def get_all_users():
    users = session.query(db.User).all()
    return users

app.add_api_route("/users", get_container(UserRepository).resolve(Dependency), methods=["GET"])
app.add_api_route("/courses", get_container(CourseRepository).resolve(Dependency), methods=["GET"])
app.add_api_route("/videos", get_container(VideoRepository).resolve(Dependency), methods=["GET"])
app.add_api_route("/reviews", get_container(ReviewRepository).resolve(Dependency), methods=["GET"])
app.add_api_route("/purchases", get_container(PurchaseRepository).resolve(Dependency), methods=["GET"])
app.add_api_route("/progresses", get_container(ProgressRepository).resolve(Dependency), methods=["GET"])

@app.put("/users/{user_id}")
def update_user(user_id: int, updated_user: User):
    user = session.get(db.User, user_id)
    if user:
        user.name = updated_user.name
        user.email = updated_user.email
        session.commit()
        return "User updated successfully"
    return "User not found"

@app.delete("/courses/{course_id}")
def delete_course(course_id: int):
    course = session.get(db.Course, course_id)
    if course:
        session.delete(course)
        session.commit()
        return "Course deleted successfully"
    return "Course not found"


