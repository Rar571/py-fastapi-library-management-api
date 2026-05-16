from sqlalchemy.orm import Session

from fastapi import FastAPI, Depends, HTTPException

import crud
import schemas
from database import base, engine, SessionLocal

app = FastAPI()


base.metadata.create_all(bind=engine)


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/authors/", response_model=list[schemas.AuthorList])
def authors_list(db: Session = Depends(get_db)):
    return crud.get_all_authors(db)


@app.get("/authors/{author_id}/", response_model=schemas.AuthorList)
def author_detail(
    author_id: int,
    db: Session = Depends(get_db)
    ):
    author = crud.get_author(db=db, author_id=author_id)

    if author is None:
        raise HTTPException(status_code=404, detail="Author with this id is not found")

    return author


@app.post("/authors/", response_model=schemas.AuthorList)
def author_create(
    author: schemas.AuthorCreate,
    db: Session = Depends(get_db)
):
    return crud.create_author(db=db, author=author)
