from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import RedirectResponse
import validators
import schemas

import crud
from sqlalchemy.orm import Session

import models, schemas
from database import SessionLocal, engine

import secrets

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

def get_db():
    #will create and yield new database sessions with each request
    db = SessionLocal()
    try:
        yield db
        #close db when request is finished
    finally:
        db.close()

@app.get('/')
def read_root():
    return 'Welcome to my app'

def raise_bad_request(message):
    raise HTTPException(status_code = 400, detail=message)

def raise_not_found(request):
    message = f"URL '{request.url}' doesn't exist"
    raise HTTPException(status_code=404, detail=message)

@app.get("/{url_key}")
#will be called any time a client requests a URL that matches the host and key pattern
def forward_to_target_url(
        url_key: str,
        request: Request,
        db: Session = Depends(get_db)
    ):
    #look for an active URL entry with the provided url_key in your database
    if db_url := crud.get_db_url_by_key(db=db, url_key=url_key):
        return RedirectResponse(db_url.target_url)
    else:
        raise_not_found(request)


#Make sure it responds to any post requests
@app.post('/url', response_model = schemas.URLInfo)
#establish a database session for the request and close the session when the request is finished.
def create_url(url: schemas.URLBase, db:Session=Depends(get_db)):
    #when the provided URL isn’t valid
    if not validators.url(url.target_url):
        raise_bad_request(message="Your provided URL is not valid")

    #create a database entry for your target_url.
    db_url = crud.create_db_url(db=db, url=url)
    db_url.url = db_url.key
    db_url.admin_url = db_url.secret_key

    return db_url

    return db_url