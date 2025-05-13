from googleapiclient.discovery import build
import csv

class YouTubeSearcher:
    def __init__(self, api_key: str, proxy_url: str = None, timeout_secs: int = 30):
        import httplib2
        import os
        if proxy_url:
            proxy_info = httplib2.ProxyInfo(
                proxy_type=httplib2.socks.PROXY_TYPE_HTTP,
                proxy_host=proxy_url.split("://")[-1].split(":")[0],
                proxy_port=int(proxy_url.split(":")[-1]),
            )
            http_obj = httplib2.Http(proxy_info=proxy_info, timeout=timeout_secs)
        else:
            for var in ("https_proxy", "HTTPS_PROXY"):
                os.environ.pop(var, None)
            http_obj = httplib2.Http(timeout=timeout_secs)
        self.yt = build("youtube", "v3", developerKey=api_key,
                        cache_discovery=False, http=http_obj)

    def search_videos(self, keyword: str, max_results: int = 25):
        req = self.yt.search().list(
            part="id,snippet",
            q=keyword,
            type="video",
            maxResults=max_results,
            order="relevance"
        )
        res = req.execute()
        return [
            {
                "videoId": item["id"]["videoId"],
                "title": item["snippet"]["title"],
                "channelId": item["snippet"]["channelId"],
                "channelTitle": item["snippet"]["channelTitle"],
                "description": item["snippet"]["description"],
                "publishTime": item["snippet"]["publishedAt"]
            }
            for item in res["items"]
        ]

    def write_to_csv(self, keyword: str, max_results: int, output_file: str):
        videos = self.search_videos(keyword, max_results)
        with open(output_file, "w", newline='', encoding="utf-8") as csvfile:
            fieldnames = ["videoId", "title", "channelId", "channelTitle", "description", "publishTime"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(videos)

if __name__ == '__main__':
    youtube = YouTubeSearcher(api_key='AIzaSyBx-8EFvRjOaQT3uecCtrqJFkaM2jpHvGM',proxy_url='http://127.0.0.1:1080')
    keyword = "Photography Tutorials"
    max_results = 100
    output_file = "../../result/youtube_search_results.csv"
    youtube.write_to_csv(keyword, max_results, output_file)