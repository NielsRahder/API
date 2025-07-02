from .. import models, schema, utils, oauth2
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import session
from ..database import engine, get_db
from ..schema import PostBase, PostCreate, PostResponse, UserCreate, UserOut, PostOut
from typing import List, Optional
from jose import JWTError
from sqlalchemy import func

router = APIRouter(
    prefix = "/posts", 
    tags = ['Posts']
)

@router.get("/", response_model= List[PostOut])
def get_post(db: session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
            limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # cursor.execute('SELECT * FROM posts')
    # posts = cursor.fetchall()
    
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    

    return posts


@router.post("/", status_code = status.HTTP_201_CREATED, response_model= PostResponse)
def create_post(post: PostCreate, db: session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute('INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *', 
    #                (post.title, post.content, post.published)) #use %s instead of an fstring to prevent SQL injection
    # new_post = cursor.fetchone()

    # connection.commit() #push the changes out

    # new_post = models.Post(title = post.title, 
    #            content = post.content, 
    #            published = post.published)
    
    new_post = models.Post(owner_id = current_user.id, **post.model_dump())
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}", response_model= PostOut)
def get_post(id: int, db: session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute('SELECT * FROM posts WHERE id = %s', (str(id)))            
    # post = cursor.fetchone()

    #post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f"post with ID {id} not found") 
    
    return post


@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # cursor.execute('DELETE FROM posts WHERE id = %s RETURNING *', str(id))
    # deleted_post = cursor.fetchone()
    # connection.commit()

    deleted_post = db.query(models.Post).filter(models.Post.id == id).first()

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail = f"post with id:{id} does not exist")
    
    if deleted_post.owner_id != current_user.id:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                            detail = f"That is not your post m8")
    
    db.delete(deleted_post)
    db.commit()
    
    return Response(status_code= status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=PostResponse)
def update_post(id: int, post: PostBase, db: session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # cursor.execute('UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *',
    #                (post.title, post.content, post.published, str(id))) 
    
    # updated_post = cursor.fetchone()
    # connection.commit()

    updated_post_query = db.query(models.Post).filter(models.Post.id == id)
    
    updated_post = updated_post_query.first()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail = f"post with id:{id} does not exist")
    
    if updated_post.owner_id != current_user.id:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                        detail = f"That is not your post m8")


    updated_post_query.update(post.model_dump(), synchronize_session = False)
    
    db.commit()

    return updated_post_query.first()