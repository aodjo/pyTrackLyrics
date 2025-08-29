class Lyrics:
    def __init__(self, trackName: str, artistName: str = "", providers: list = ["vibe"], lyricsType: str = "lrc"):
        """가사를 불러오는 모듈이에요.
        
            **Argument:** 
                - trackName (str, 트랙 이름)
                - artistName (str, optional, 아티스트 이름)
                - providers (list, optional, 제공 업체 리스트)
                - lyricsType (str, optional, 반환 가사 타입 (json, lrc))
        """

        self.trackName = trackName
        self.artistName = artistName
        self.providers = providers
        self.lyricsType = lyricsType

    
    