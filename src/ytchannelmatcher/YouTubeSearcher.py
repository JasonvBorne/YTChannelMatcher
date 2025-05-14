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
    # keywords = [
	# "Smartphone Photography Tricks","Portrait Photography Techniques","Landscape Photography Tips","Street Photography Guide",
	# "Lighting for Photography","Camera Settings for Beginners","Photography Composition Tips"]
    # keywords = ["Street Photography Guide","Lighting for Photography",
    #             "Camera Settings for Beginners", "Photography Composition Tips"]
    # max_results = 500
    # for keyword in keywords:
    #     output_file = f"../../result/{keyword.replace(' ', '_')}_results.csv"
    #     youtube.write_to_csv(keyword, max_results, output_file)

    video_id = "5x3Hy7zie94"
    video_meta = youtube.get_video_metadata(video_id)
    '''
    {'kind': 'youtube#video', 'etag': 'ZVnhO9jlHYLXddU0SMG59b4urv0', 'id': '5x3Hy7zie94', 'snippet': {'publishedAt': '2020-10-18T18:07:00Z', 'channelId': 'UCpsHnULJAkwwckxzdmspKDw', 'title': 'Lightroom Tutorial BASICS | Photo Editing Masterclass', 'description': "Learn How To Make Six Figures With Your Camera! - https://www.skool.com/full-timecreator/about\nThe Most Advanced Lightroom Presets Ever Created! - https://bit.ly/leicalook2\nToday we tackle our Lightroom Tutorial Basics Masterclass! Everything you need to know to learn how to professionally edit photos in adobe lightroom! #Lightroom #Editing #Tutorial\nDownload & Edit This Photo Along With Me! https://bit.ly/37iBg0k\nJoin Our Editing & Photography Discord - https://discord.gg/BRxefa75Sy\n-Download the FILM FRAMES App for free on IOS! https://bit.ly/filmframes\n\nThe R5 & All My Favorite Gear: https://bit.ly/2SWka3kbodies\n-Subscribe for New Videos every Week! http://bit.ly/ZMLOuV\n-Best MUSIC For Youtubers: https://goo.gl/G5hfFs - Royalty Free!\n\nChapters--\n00:00 - 01:59 Intro\n02:00 - 04:50 Basics\n05:00 - 07:50 Tone Curve\n08:00 - 10:30 HSL/Color\n10:31 - 12:00 Calibration\n12:30 - 13:00 Detail\n13:01 - 13:30 Lens Correction\n13:31 - 14:00 Effects\n14:01 - 14:31 Crop Tool\n14:32 - 16:50 Adjustment Brushes\n\n--- My Instagram is @sawyerhartman\nShot on a Canon EOS R5\nIf You've read this far just comment something nice, and have an awesome day  xx\n\nBRAND INQUIRY : \nfor business related emails contact Business@Sawyerhartman.com\nCategory", 'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/5x3Hy7zie94/default.jpg', 'width': 120, 'height': 90}, 'medium': {'url': 'https://i.ytimg.com/vi/5x3Hy7zie94/mqdefault.jpg', 'width': 320, 'height': 180}, 'high': {'url': 'https://i.ytimg.com/vi/5x3Hy7zie94/hqdefault.jpg', 'width': 480, 'height': 360}, 'standard': {'url': 'https://i.ytimg.com/vi/5x3Hy7zie94/sddefault.jpg', 'width': 640, 'height': 480}, 'maxres': {'url': 'https://i.ytimg.com/vi/5x3Hy7zie94/maxresdefault.jpg', 'width': 1280, 'height': 720}}, 'channelTitle': 'sawyerhartman', 'tags': ['Lightroom', 'lightroom editing', 'lightroom photo editing', 'lightroom mobile tutorial', 'lightroom presets tutorial', 'lightroom editing tutorial', 'adobe lightroom', 'lightroom cc', 'lightroom tips', 'how to edit photos', 'how to use lightroom', 'lightroom tutorials for beginners', 'lightroom tips and tricks', 'how to edit in lightroom', 'lightroom tutorials', 'lightroom cc tutorial', 'Lightroom tutorial', 'lightroom tutorial for beginners', 'lightroom tutorial 2020', 'lightroom color grading', 'lightroom 2021'], 'categoryId': '1', 'liveBroadcastContent': 'none', 'localized': {'title': 'Lightroom Tutorial BASICS | Photo Editing Masterclass', 'description': "Learn How To Make Six Figures With Your Camera! - https://www.skool.com/full-timecreator/about\nThe Most Advanced Lightroom Presets Ever Created! - https://bit.ly/leicalook2\nToday we tackle our Lightroom Tutorial Basics Masterclass! Everything you need to know to learn how to professionally edit photos in adobe lightroom! #Lightroom #Editing #Tutorial\nDownload & Edit This Photo Along With Me! https://bit.ly/37iBg0k\nJoin Our Editing & Photography Discord - https://discord.gg/BRxefa75Sy\n-Download the FILM FRAMES App for free on IOS! https://bit.ly/filmframes\n\nThe R5 & All My Favorite Gear: https://bit.ly/2SWka3kbodies\n-Subscribe for New Videos every Week! http://bit.ly/ZMLOuV\n-Best MUSIC For Youtubers: https://goo.gl/G5hfFs - Royalty Free!\n\nChapters--\n00:00 - 01:59 Intro\n02:00 - 04:50 Basics\n05:00 - 07:50 Tone Curve\n08:00 - 10:30 HSL/Color\n10:31 - 12:00 Calibration\n12:30 - 13:00 Detail\n13:01 - 13:30 Lens Correction\n13:31 - 14:00 Effects\n14:01 - 14:31 Crop Tool\n14:32 - 16:50 Adjustment Brushes\n\n--- My Instagram is @sawyerhartman\nShot on a Canon EOS R5\nIf You've read this far just comment something nice, and have an awesome day  xx\n\nBRAND INQUIRY : \nfor business related emails contact Business@Sawyerhartman.com\nCategory"}, 'defaultAudioLanguage': 'es'}, 'contentDetails': {'duration': 'PT17M54S', 'dimension': '2d', 'definition': 'hd', 'caption': 'true', 'licensedContent': True, 'contentRating': {}, 'projection': 'rectangular'}, 'statistics': {'viewCount': '2661950', 'likeCount': '94486', 'favoriteCount': '0', 'commentCount': '2134'}}
    '''
    print(video_meta["snippet"]["title"])


    channel_id = "UCHIRBiAd-PtmNxAcLnGfwog"
    channel_meta = youtube.get_channel_metadata(channel_id)
    '''
    {'kind': 'youtube#channel', 'etag': 'LUcODZhd3-6-N2uXkRBW5Mahsak', 'id': 'UCHIRBiAd-PtmNxAcLnGfwog', 'snippet': {'title': 'B&H Photo Video Pro Audio', 'description': 'We love what we do. We are both professional and avid photographers, filmmakers, and audio professionals. We enjoy getting out to explore the world as creators and teachers. On our channel, you’ll see videos, podcasts, and tutorials showing this passion for craft, as well as other artists that love what they do as much as we do.\n \nWant to see more of something you love doing, or want to do better? Drop us a line at askbh@bhphoto.com\n\nHead to our B&H Event Space YouTube channel for more seminars! https://bhpho.to/BHEventSpaceYT\n', 'customUrl': '@bandh', 'publishedAt': '2007-05-28T22:09:20Z', 'thumbnails': {'default': {'url': 'https://yt3.ggpht.com/he4HLOuSK_9wQGEHQq-SLqv_deXV7LUQvSC_ZFQec_-i1FBF4SI_git1SbcevBQ0DglNI_rn7iA=s88-c-k-c0x00ffffff-no-rj', 'width': 88, 'height': 88}, 'medium': {'url': 'https://yt3.ggpht.com/he4HLOuSK_9wQGEHQq-SLqv_deXV7LUQvSC_ZFQec_-i1FBF4SI_git1SbcevBQ0DglNI_rn7iA=s240-c-k-c0x00ffffff-no-rj', 'width': 240, 'height': 240}, 'high': {'url': 'https://yt3.ggpht.com/he4HLOuSK_9wQGEHQq-SLqv_deXV7LUQvSC_ZFQec_-i1FBF4SI_git1SbcevBQ0DglNI_rn7iA=s800-c-k-c0x00ffffff-no-rj', 'width': 800, 'height': 800}}, 'localized': {'title': 'B&H Photo Video Pro Audio', 'description': 'We love what we do. We are both professional and avid photographers, filmmakers, and audio professionals. We enjoy getting out to explore the world as creators and teachers. On our channel, you’ll see videos, podcasts, and tutorials showing this passion for craft, as well as other artists that love what they do as much as we do.\n \nWant to see more of something you love doing, or want to do better? Drop us a line at askbh@bhphoto.com\n\nHead to our B&H Event Space YouTube channel for more seminars! https://bhpho.to/BHEventSpaceYT\n'}, 'country': 'US'}, 'statistics': {'viewCount': '436253505', 'subscriberCount': '987000', 'hiddenSubscriberCount': False, 'videoCount': '5074'}, 'brandingSettings': {'channel': {'title': 'B&H Photo Video Pro Audio', 'description': 'We love what we do. We are both professional and avid photographers, filmmakers, and audio professionals. We enjoy getting out to explore the world as creators and teachers. On our channel, you’ll see videos, podcasts, and tutorials showing this passion for craft, as well as other artists that love what they do as much as we do.\n \nWant to see more of something you love doing, or want to do better? Drop us a line at askbh@bhphoto.com\n\nHead to our B&H Event Space YouTube channel for more seminars! https://bhpho.to/BHEventSpaceYT\n', 'keywords': 'photography photo mirrorless camera DSLR camcorders lens lenses flash megapixel aperture shutter speed eos bh and h” howto speedlite lighting filmmaking film video videos micro four thirds Mac PC Windows MacOS iMac Macbook superstore how to shoot Jeff Cable Lindsay Adler lightroom photoshop lecture workshop tutorial Peter Hurley wedding reviews tim grey', 'trackingAnalyticsAccountId': 'UA-48894505-5', 'unsubscribedTrailer': 'EdyImCbC0Yg', 'country': 'US'}, 'image': {'bannerExternalUrl': 'https://yt3.googleusercontent.com/AOq9aaRCcm47Kn1EIfXgIe8Zc1yfz--Yre0gGYt3BFDKhDpmaGASZsNVxXkb562rq3RV_xkVv8M'}}}
    '''
    print(channel_meta["snippet"]["title"])