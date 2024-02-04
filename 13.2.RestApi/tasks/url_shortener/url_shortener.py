from fastapi import FastAPI, HTTPException
import hashlib
from fastapi.responses import RedirectResponse
from pydantic import BaseModel as base

app = FastAPI()
url_storage = {}


class Shorted(base):
    url: str
    key: str


class Change(base):
    title: str


class ToShort(base):
    url: str


def generate_hash(url: bytes) -> str:
    return hashlib.sha256(url).hexdigest()[:8]


@app.post("/shorten", response_model=Shorted, status_code=201, summary="Short Url")
async def short_url(url_req: ToShort) -> Shorted:
    url_storage[generate_hash(url_req.url.encode())] = url_req.url
    return Shorted(url=url_req.url, key=generate_hash(url_req.url.encode()))


@app.get('/go/{key}', status_code=307, responses={
    307: {
        'description': 'Successful Response',
        'content': {
            'application/json': {
                'schema': Change(title='Response Redirect To Url Go  Key  Get')
            }
        }
    }
})
async def redirect_to_url(key: str) -> RedirectResponse:
    if url_storage.get(key):
        return RedirectResponse(url=url_storage[key])
    else:
        raise HTTPException(status_code=404, detail='Url not found')
