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

    def search_videos(self, keyword: str, max_results: int = 100):
        import time
        start_time = time.time()
        videos = []
        next_page_token = None

        while len(videos) < max_results:
            req = self.yt.search().list(
                part="id,snippet",
                q=keyword,
                type="video",
                maxResults=min(50, max_results - len(videos)),  # 每次最多取50条
                order="relevance",
                pageToken=next_page_token
            )
            res = req.execute()

            for item in res.get("items", []):
                if "videoId" in item["id"]:
                    videos.append({
                        "videoId": item["id"]["videoId"],
                        "title": item["snippet"]["title"],
                        "channelId": item["snippet"]["channelId"],
                        "channelTitle": item["snippet"]["channelTitle"],
                        "description": item["snippet"]["description"],
                        "publishTime": item["snippet"]["publishedAt"],
                    })

            next_page_token = res.get("nextPageToken")
            if not next_page_token:
                break

        print(f"✅ 搜索完成，共获取 {len(videos)} 条视频，用时 {time.time() - start_time:.2f} 秒")
        return videos

    def write_to_csv(self, keyword: str, max_results: int, output_file: str):
        import time
        start_time = time.time()
        videos = self.search_videos(keyword, max_results)
        with open(output_file, "w", newline='', encoding="utf-8") as csvfile:
            print(f"📄 开始写入 {len(videos)} 条视频数据到 {output_file} CSV 文件...")
            fieldnames = ["videoId", "title", "channelId", "channelTitle", "description", "publishTime","statistics"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(videos)
            print(f"✅ 写入完成，用时 {time.time() - start_time:.2f} 秒")


    def get_channel_metadata(self, channel_id: str):
        request = self.yt.channels().list(
            part="snippet,statistics,brandingSettings",
            id=channel_id
        )
        response = request.execute()
        if response["items"]:
            return response["items"][0]
        return None

    def get_video_metadata(self, video_id: str):
        request = self.yt.videos().list(
            part="snippet,statistics,contentDetails",
            id=video_id
        )
        response = request.execute()
        if response["items"]:
            return response["items"][0]
        return None


if __name__ == '__main__':
    #api-key1 AIzaSyBx-8EFvRjOaQT3uecCtrqJFkaM2jpHvGM
    #api-key2 AIzaSyBCQwls2Lz7YuD0JaDjb-sdxEUPi5ZcUiw
    # AIzaSyDwQtpdrdsmuRsawPAAWYa6zZ21KaH39pY
    #AIzaSyAKfY0kf6VkLg_XbmZaeCcPPwR9lpzKQeM
    youtube = YouTubeSearcher(api_key='AIzaSyDwQtpdrdsmuRsawPAAWYa6zZ21KaH39pY',proxy_url='http://127.0.0.1:1080')
    #"Photography Tutorials","Photo Editing Tutorials", "Beginner Photography Tips","DSLR Photography Tutorials"
    keywords = [
	"Smartphone Photography Tricks","Portrait Photography Techniques","Landscape Photography Tips","Street Photography Guide",
	"Lighting for Photography","Camera Settings for Beginners","Photography Composition Tips"]
    # keywords = ["Street Photography Guide","Lighting for Photography",
    #             "Camera Settings for Beginners", "Photography Composition Tips"]
    max_results = 500
    for keyword in keywords:
        output_file = f"../../result/{keyword.replace(' ', '_')}_results.csv"
        youtube.write_to_csv(keyword, max_results, output_file)