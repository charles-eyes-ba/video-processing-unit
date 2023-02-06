class VideoFeed:
    
    @property
    def id(self) -> str:
        return self._id
    
    @property
    def url(self) -> str:
        return self._url
    
    def __init__(self, id: str, url: str):
        self._id = id
        self._url = url