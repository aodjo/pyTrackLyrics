from providers.vibe import Vibe as Vibe_Provider

available_providers = ["vibe"]

class Lyrics:
    def __init__(self, trackName: str, artistName: str = None, providers: list = available_providers, lyricsType: str = "lrc"):
        f"""가사를 불러오는 모듈이에요.
        
            **Argument:** 
                - trackName (str, 트랙 이름)
                - artistName (str, optional, 아티스트 이름)
                - providers (list, optional, 제공 업체 리스트 ({available_providers}))
                - lyricsType (str, optional, 반환 가사 타입 (json, lrc))
        """

        self.trackName = trackName
        self.artistName = artistName
        self.providers = providers
        self.lyricsType = lyricsType

    def getSyncedLyrics(self):
        for provider in self.providers:
            match provider:
                case "vibe":
                    vibe = Vibe_Provider(self.lyricsType)
                    isTrackExist, trackid = vibe.getTrackId(f"{f'{self.artistName} - ' if self.artistName else ''}{self.trackName}")
                    if isTrackExist:
                        isLyricsExist, lyricsType, lyrics = vibe.getTrackLyrics(trackid, syncOnly=True)
                        if isLyricsExist:
                            if lyricsType == "synced":
                                return lyrics
    
    def getNormalLyrics(self):
        for provider in self.providers:
            match provider:
                case "vibe":
                    vibe = Vibe_Provider(self.lyricsType)
                    isTrackExist, trackid = vibe.getTrackId(f"{f'{self.artistName} - ' if self.artistName else ''}{self.trackName}")
                    if isTrackExist:
                        isLyricsExist, lyricsType, lyrics = vibe.getTrackLyrics(trackid, normalOnly=True)
                        if isLyricsExist:
                            if lyricsType == "normal":
                                return lyrics





if __name__ == "__main__":
    lyrics = Lyrics("청춘만화", "이무진")
    a = lyrics.getSyncedLyrics()
    print(a)
                                
