import requests
import xmltodict
import json
from bs4 import BeautifulSoup
from urllib.parse import quote


class Vibe:
    def __init__(self, returnType):
        if returnType in ["json", "lrc"]:
            self.returnType = returnType
        else:
            raise ValueError("올바르지 않는 반환 타입입니다. json과 lrc 중 선택하세요.")

    def formatLyrics(self, lyrics_json, lyricsType=None):
        """
            주어진 가사 json을 특정 형식으로 변환합니다.

        **Arguments:** lyrics_json (dict, 가사 json), lyricsType (str, optional, 반환 타입)

        **Return:** 포멧된 가사 (str)
        """

        if lyricsType in ["json", "lrc", None]:
            returnType = None
            if lyricsType:
                returnType = lyricsType
            elif self.returnType:
                returnType = self.returnType
            else:
                returnType = "lrc"


            start_times = lyrics_json['startTimeIndex']['startTimeIndex']
            lyrics = None
            
            if type(lyrics_json["contents"]["contents"]) == dict:
                lyrics = lyrics_json['contents']['contents']['text']['text']
            else:
                lyrics = lyrics_json['contents']['contents'][0]['text']['text']

            if returnType == "json":

                formatted_list = []
                for start_time_str, text in zip(start_times, lyrics):
                    start_time_float = float(start_time_str)

                    minutes = int(start_time_float // 60)
                    seconds = int(start_time_float % 60)
                    hundredths = int((start_time_float - int(start_time_float)) * 100)

                    formatted_time = f"{minutes:01}:{seconds:02}.{hundredths:02}"
                    
                    formatted_list.append({"start": formatted_time, "text": text})

                return json.dumps(formatted_list, ensure_ascii=False)
            elif returnType == "lrc":
                if len(start_times) != len(lyrics):
                    raise ValueError("시작 시간과 가사 라인의 개수가 일치하지 않습니다.")

                lrc_lines = []
                for i in range(len(start_times)):
                    start_time_str = start_times[i]
                    lyric_text = lyrics[i]
                    
                    total_seconds = float(start_time_str)
                    minutes = int(total_seconds // 60)
                    seconds = int(total_seconds % 60)
                    milliseconds = int((total_seconds - int(total_seconds)) * 100)
                    
                    lrc_line = f"[{minutes:01d}:{seconds:02d}.{milliseconds:02d}] {lyric_text}"
                    lrc_lines.append(lrc_line)
                    
                return "\n".join(lrc_lines)
            
        else:
            raise ValueError("올바르지 않는 반환 타입입니다. json과 lrc 중 선택하세요.")

    def getTrackId(self, query):
        """트랙의 ID를 가져오는 함수입니다.

            **Argument:** query (str)

            **Return:** ID 존재 여부 (Boolen), 트랙 ID (int | None)
        """

        requestURL = f"https://apis.naver.com/vibeWeb/musicapiweb/v4/searchall?query={quote(query)}&sort=RELEVANCE"
        response = requests.get(requestURL)
        xmlData = response.text
        soup = BeautifulSoup(xmlData, "xml") 

        json_data = xmltodict.parse(soup.prettify())

        popularResult = json_data["response"]["result"]["popularResult"]
        resultType = int(popularResult["searchType"]) # 1 -> 성공 / -1 -> 실패

        if resultType == 1:
            popularTrackId = popularResult["track"]["trackId"]
            return True, popularTrackId

        elif resultType == -1:
            return False, None
    
    def getTrackLyrics(self, trackId, syncOnly=None, normalOnly=None):
        """트랙의 가사를 가져오는 함수입니다.
            가사의 우선순위는 synced를 우선으로 반환합니다.
        
            **Argument:** trackId (int), syncOnly (Boolen, Optional), normalOnly (Boolen, Optional)

            **Return:** 가사 존재 여부 (boolen), 가사 타입 (str | None, "normal"/"synced" | None), 가사 (str | None)
        """
        requestURL = f"https://apis.naver.com/vibeWeb/musicapiweb/vibe/v4/lyric/{trackId}"
        response = requests.get(requestURL)
        xmlData = response.text
        soup = BeautifulSoup(xmlData, "xml") 

        json_data = xmltodict.parse(soup.prettify())

        lyricsValue = json_data["response"]["result"]["lyric"]
        hasNormalLyric = True if lyricsValue["hasNormalLyric"] == "true" else False 
        hasSyncLyric = True if lyricsValue["hasSyncLyric"] == "true" else False 

        if syncOnly and normalOnly:
            raise ValueError("syncOnly와 normalOnly는 함께 사용할 수 없습니다.")

        elif not syncOnly and not normalOnly:
            if hasSyncLyric:
                lyrics = self.formatLyrics(lyricsValue["syncLyric"])
                return True, "synced", lyrics
            elif hasNormalLyric:
                lyrics = lyricsValue["normalLyric"]["text"]
                return True, "normal", lyrics
            else:
                return False, None, None
        elif syncOnly:
            if hasSyncLyric:
                lyrics = self.formatLyrics(lyricsValue["syncLyric"])
                return True, "synced", lyrics
            else:
                return False, None, None
        elif normalOnly:
            if hasNormalLyric:
                lyrics = lyricsValue["normalLyric"]["text"]
                return True, "normal", lyrics
            else:
                return False, None, None

if __name__ == "__main__":
    vibe = Vibe("lrc")

    success, result = vibe.getTrackId("이무진 청춘만화")
    print(vibe.getTrackLyrics(result))

