# fastapi sqlmodel uvicorn[standard]

from typing import List

import uvicorn
from fastapi import Depends, FastAPI
from sqlalchemy import func
from sqlmodel import Field, Session, SQLModel, create_engine, select

DATABASE_URL = "sqlite:///./melon-20231204.sqlite3"
engine = create_engine(DATABASE_URL, echo=True)

app = FastAPI()


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


class Song(SQLModel, table=True):
    __tablename__ = "melon_song"

    id: int = Field(default=None, primary_key=True)
    uid: str = Field(max_length=20, unique=True, index=True)
    rank: int
    album: str = Field(max_length=200)
    title: str = Field(max_length=200)
    artist: str = Field(max_length=200)
    cover_image_url: str = Field(max_length=500)
    lyrics: str
    genre: str = Field(max_length=100)
    release_date: str  # Using str for simplicity; consider using date type
    likes: int
    created_at: str  # Using str for simplicity; consider using datetime type
    updated_at: str  # Using str for simplicity; consider using datetime type


class SongListResponse(SQLModel):
    title: str
    title_length: int


# URL + method => 분기
@app.get("/melon/", response_model=List[SongListResponse])
def read_songs(*, session: Session = Depends(get_session)):
    songs = session.exec(
        select(Song.title, func.length(Song.title).label("title_length"))
    ).all()
    return songs


def main():
    # create_db_and_tables()
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
