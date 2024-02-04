import string
import random
from fastapi import FastAPI, Depends, HTTPException, Query, Header
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

user_data = {}
music_data = {}
music_counter = 1


class UserAccount(BaseModel):
    name: str
    age: int


class UserAccountID(BaseModel):
    token: str


class track(BaseModel):
    name: str
    artist: str
    year: Optional[int] = None
    genres: Optional[list[str]] = []


class ResponseModel(BaseModel):
    track_id: int


class trackInfo(BaseModel):
    artist: str
    name: str


class SearchResponse(BaseModel):
    track_ids: Optional[list[int]] = []


def check_token(x_token: str = Header(None)) -> Optional[str]:
    if not x_token:
        raise HTTPException(status_code=401, detail="Missing token")
    if x_token not in user_data:
        raise HTTPException(status_code=401, detail="Incorrect token")
    return x_token


@app.post("/api/v1/registration/register_user", response_model=UserAccountID)
async def register_user(user: UserAccount) -> UserAccountID:
    token = ''.join(random.choices(string.ascii_letters + string.digits, k=40))
    user_data[token] = user
    return UserAccountID(token=token)


@app.post("/api/v1/tracks/add_track", response_model=ResponseModel, dependencies=[Depends(check_token)],
          status_code=201)
async def add_track(track: track) -> ResponseModel:
    global music_counter
    music_data[music_counter] = track
    track_id = music_counter
    music_counter += 1
    return ResponseModel(track_id=track_id)


@app.delete("/api/v1/tracks/{track_id}", dependencies=[Depends(check_token)])
async def delete_track(track_id: int) -> Optional[dict[str, str]]:
    if track_id not in music_data:
        raise HTTPException(status_code=404, detail="Invalid track_id")
    del music_data[track_id]
    return {"status": "track removed"}


@app.get("/api/v1/tracks/all", response_model=list[track], dependencies=[Depends(check_token)], status_code=200)
async def get_all_tracks() -> list[track]:
    return [track for track in music_data.values()]


@app.get("/api/v1/tracks/search", dependencies=[Depends(check_token)], response_model=SearchResponse)
async def search_tracks(name: Optional[str] = Query(None), artist: Optional[str] = Query(None)) -> SearchResponse:
    if (not name) and (not artist):
        raise HTTPException(status_code=422, detail="You should specify at least one search argument")
    search_name = False
    search_artist = False
    search_both = False
    track_ids = []
    if name and not artist:
        search_name = True
    elif not name and artist:
        search_artist = True
    elif name and artist:
        search_both = True
    for track_id, track in music_data.items():
        if search_name and name == track.name:
            track_ids.append(track_id)
        elif search_artist and artist == track.artist:
            track_ids.append(track_id)
        elif search_both and name == track.name and artist == track.artist:
            track_ids.append(track_id)
    return SearchResponse(track_ids=track_ids)


@app.get("/api/v1/tracks/{track_id}", response_model=trackInfo, dependencies=[Depends(check_token)], status_code=200)
async def get_track(track_id: int) -> trackInfo:
    if track_id not in music_data:
        raise HTTPException(status_code=404, detail="Invalid track_id")
    return trackInfo(name=music_data[track_id].name, artist=music_data[track_id].artist)
