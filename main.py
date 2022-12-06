from fastapi import FastAPI, HTTPException
import validators
import schemas

app = FastAPI()

@app.get('/')
def read_root():
    return 'Welcome to my app'

def raise_bad_request(message):
    raise HTTPException(status_code = 400, detail=message)

@app.post('/url')
def create_url(url: schemas.URLBase):
    #when the provided URL isn’t valid
    if not validators.url(url.target_url):
        raise_bad_request(message="Your provided URL is not valid")
    return f"TODO: Create database entry for: {url.target_url}"    