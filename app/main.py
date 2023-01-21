from fastapi import FastAPI
from fastapi import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange


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

@app.get('/posts/{id}')
def get_posts(id: int):
    print(id)
    return {
        "data":f'post id is {id}'
    }