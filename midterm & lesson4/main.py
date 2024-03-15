from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
import database as db

app = FastAPI()

class Book(BaseModel):
    id: int
    title: str
    author_id: int
    category_id: int

    class Config:
        orm_mode = True

class Author(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class Category(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

def get_session():
    session = db.SessionLocal()
    try:
        yield session
    finally:
        session.close()

@app.post('/book')
def create_book(book: Book, session: db.Session = Depends(get_session)):
    session.add(db.Book(**book.dict()))
    session.commit()
    return f"Book {book.title} created successfully"

@app.get('/books')
def get_books(session: db.Session = Depends(get_session)):
    books = session.execute(select(db.Book)).scalars().all()
    return books

@app.get('/book/{book_id}')
def get_book(book_id: int, session: db.Session = Depends(get_session)):
    book = session.query(db.Book).filter(db.Book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.post('/author')
def create_author(author_name: str, session: db.Session = Depends(get_session)):
    author = db.Author(name=author_name)
    session.add(author)
    session.commit()
    return f"Author {author_name} created successfully"

@app.get('/authors')
def get_authors(session: db.Session = Depends(get_session)):
    authors = session.execute(select(db.Author)).scalars().all()
    return authors

@app.post('/category')
def create_category(category_name: str, session: db.Session = Depends(get_session)):
    category = db.Category(name=category_name)
    session.add(category)
    session.commit()
    return f"Category {category_name} created successfully"

@app.get('/categories')
def get_categories(session: db.Session = Depends(get_session)):
    categories = session.execute(select(db.Category)).scalars().all()
    return categories


# from fastapi import FastAPI, Depends
# from pydantic import BaseModel
# from sqlalchemy import select

# import database as db

# app = FastAPI()

# class Teacher(BaseModel):
#     id: int
#     name: str
#     yoe: int

#     class Config:
#         from_attributes = True

# class Student(BaseModel):
#     id: int
#     name: str
#     age: int

#     class Config:
#         from_attributes = True


# def get_session():
#     session = db.session
#     yield session
#     session.commit()
#     session.close()


# @app.post('/student')
# def student(student: Student, session: db.Session = Depends(get_session)):
#     session.add(db.Student(**student.model_dump()))
#     return f"{student.name} was added"

# @app.get('/student')
# def student() -> list[Student]:
#     db_students = db.session.execute(select(db.Student)).scalars().all()
#     students = []
#     for db_student in db_students:
#         students.append(Student.model_validate(db_student)) 
    
#     return students

# def nested_dependency(teacher_with_lesson: TeacherWithLesson):
#     lesson = teacher_with_lesson.lesson
#     teacher = teacher_with_lesson.teacher
#     return f"You have joined to {lesson}, and your teacher is {teacher.name} with {teacher.yoe} years of experience " 


# def dependency(nested_dep_func: str = Depends(nested_dependency)) -> str:
#     print("Handling Nested Dependency")
#     return nested_dep_func

