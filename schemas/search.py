from typing import List, Optional, Dict
from pydantic import BaseModel

class MetaUrl(BaseModel):
    scheme: Optional[str] = None
    netloc: Optional[str] = None
    hostname: Optional[str] = None
    favicon: Optional[str] = None
    path: Optional[str] = None

class Thumbnail(BaseModel):
    src: Optional[str] = None
    original: Optional[str] = None
    logo: Optional[bool] = False

class Profile(BaseModel):
    name: Optional[str] = None
    url: Optional[str] = None
    long_name: Optional[str] = None
    img: Optional[str] = None

class WebResult(BaseModel):
    title: str
    url: str
    description: Optional[str] = None
    profile: Optional[Profile] = None
    type: Optional[str] = None
    subtype: Optional[str] = None
    language: Optional[str] = None
    thumbnail: Optional[Thumbnail] = None
    meta_url: Optional[MetaUrl] = None

class VideoResult(BaseModel):
    type: str = "video_result"
    url: str
    title: str
    description: Optional[str] = None
    age: Optional[str] = None
    page_age: Optional[str] = None
    thumbnail: Optional[Thumbnail] = None
    meta_url: Optional[MetaUrl] = None

class SearchResponse(BaseModel):
    web: List[WebResult] = []
    videos: List[VideoResult] = []