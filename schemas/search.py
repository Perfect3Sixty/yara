from pydantic import BaseModel
from typing import Dict, Optional, List

class MetaUrl(BaseModel):
    scheme: str
    netloc: str
    hostname: str
    favicon: str
    path: str

class Thumbnail(BaseModel):
    src: str
    original: str
    logo: Optional[bool] = False  # Made logo optional with default False

class Profile(BaseModel):
    name: str
    url: str
    long_name: str
    img: str

class VideoResult(BaseModel):
    type: str
    url: str
    title: str
    description: str
    age: Optional[str] = None
    page_age: Optional[str] = None
    video: Dict = {}
    meta_url: MetaUrl
    thumbnail: Thumbnail

class WebResult(BaseModel):
    title: str
    url: str
    is_source_local: bool
    is_source_both: bool
    description: str
    profile: Profile
    language: str
    family_friendly: bool
    type: str
    subtype: str
    is_live: bool
    meta_url: MetaUrl
    thumbnail: Optional[Thumbnail] = None

class SearchResponse(BaseModel):
    videos: List[VideoResult]
    web: List[WebResult]