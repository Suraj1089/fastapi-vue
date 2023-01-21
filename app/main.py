from typing import Optional
from fastapi import FastAPI
from fastapi import Body
from pydantic import BaseModel
from random import randrange
from fastapi import Response
from fastapi import status 
from fastapi import HTTPException

app = FastAPI()

# post
class Post(BaseModel):
    title: str 
    content: str 
    published: bool = True
    rating: Optional[int] = None

my_posts = [
    {
        "id":1,
        "title":"first post",
        "cotent":"second post"
    } ,
    {
        "id":2,
        "title":"favourite posts",
        "cotent":"I like pizza"
    }
]

def find_post(id):
    for post in my_posts:
        if post['id'] == id:
            return post
    return None

@app.get('/',tags=['home'])
async def home():
    return {
        'page':'HomePage',
        'name':'suraj',
        'email':'surajpisal113@gmail.com'
    }


@app.get('/posts')
def get_posts():
    return {
        "data":my_posts
    }

# title: str , content: str
@app.post('/posts')
def create_posts(post: Post):
    # pydantic to dict
    post_dict = post.dict()
    post_dict['id'] = randrange(0,10000)
    my_posts.append(post_dict)
    return {
        "data":post_dict
    }

@app.get('/posts/{id}',status_code=status.HTTP_200_OK)
def get_posts(id: int,response: Response):
    post = find_post(id)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'post with {id} not found'
        )

def get_post_index(id):
    print(f"id is {id}")
    ct=-1
    for post in my_posts:
        ct+=1
        if post['id'] == id:
            return ct 
    return ct
@app.delete('/posts/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id:int):
    index = get_post_index(id)
    if index!=-1:
        my_posts.pop(index)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'{id} post not found'
    )

@app.put('/posts/{id}')
def update_posts(id: int,post: Post):
    index = get_post_index(id)
    print(index)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'post {id} not found')
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {
        'data':post_dict
    }
    