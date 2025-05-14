class YouTubeMetaFetcher:
    def __init__(self, yt_service):
        self.yt = yt_service

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
    fetcher = YouTubeMetaFetcher()
    # print(fetcher.get_channel_metadata("UCX6OQ3DkcsbYNE6H8uQQuVA"))
    # print(fetcher.get_video_metadata("dQw4w9WgXcQ"))