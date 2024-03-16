from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from utils.repository import AbcRepository
from utils.schemes import CreatePost, Post
import utils.models as db


class PostRepository(AbcRepository):

    def __init__(self, session: Session):
        self.session = session

    def create(self, post: CreatePost) -> str:
        self.session.add(db.Post(**post.model_dump()))
        self.session.commit()
        return "post created"

    def list(self):
        db_posts = self.session.execute(select(db.Post)).scalars().all()
        posts = [Post.model_validate(db_post) for db_post in db_posts]
        return posts

    def retrieve(self, id: int) -> Post:
        post = self.session.get(db.Post, id)
        return Post.model_validate(post)

    def delete(self, id: int):
        self.session.execute(delete(db.Post).where(db.Post.id == id))
        self.session.commit()
        return "post deleted"

