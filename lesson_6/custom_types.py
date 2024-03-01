from typing import Union, List

import schemas

CreateType = Union[schemas.CreateUser, schemas.CreatePost, schemas.CreateComment, schemas.CreateLike]
ReturnType = Union[schemas.User, schemas.Post, schemas.Comment, schemas.Like]
ListReturnType = Union[List[schemas.User], List[schemas.Post], List[schemas.Comment], List[schemas.Like]]
