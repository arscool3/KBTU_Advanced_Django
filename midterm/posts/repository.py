from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from utils.repository import AbcRepository
from utils.schemes import CreatePost, Post, Comment, Like, Complaint
import utils.models as db


class PostRepository(AbcRepository):

    def __init__(self, session: Session = None):
        self.session = session

    def create(self, post: CreatePost) -> str:
        self.session.add(db.Post(**post.model_dump()))
        self.session.commit()
        return "post created"

    def list(self):
        db_posts = self.session.query(db.Post).all()
        posts = [Post.model_validate(db_post) for db_post in db_posts]
        return posts

    def retrieve(self, id: int) -> Post:
        post = self.session.get(db.Post, id)
        return Post.model_validate(post)

    def delete(self, id: int):
        self.session.execute(delete(db.Post).where(db.Post.id == id))
        self.session.commit()
        return "post deleted"

    def get_comments(self, post_id: int):
        db_comments = self.session.query(db.Comment).where(db.Comment.post_id == post_id).all()
        comments = [Comment.model_validate(db_comment) for db_comment in db_comments]
        return comments

    def get_complaints(self, post_id: int):
        db_complaints = self.session.query(db.Complaint).where(db.Complaint.post_id == post_id).all()
        complaints = [Complaint.model_validate(db_complaint) for db_complaint in db_complaints]
        return complaints

    def get_likes(self, post_id: int):
        db_likes = self.session.query(db.Like).where(db.Like.post_id == post_id).all()
        comments = [Like.model_validate(db_like) for db_like in db_likes]
        return comments

