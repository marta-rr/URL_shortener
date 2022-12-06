from pydantic import BaseModel

class URLBase(BaseModel):
    #to store the URL that your shortened URL forwards to
    target_url: str

class URL(URLBase):
    #it allows you to deactivate shortened URLs
    is_active: bool
    #count how many times a shortened URL has been visited
    clicks: int
#Tell pydantic to work with a database model.
    class Config:
        orm_mode = True
#New class that allows to use the data in your API without storing it in your database
class URLInfo(URL):
    url: str
    admin_url: str