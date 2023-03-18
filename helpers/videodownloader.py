from pytube import YouTube

class VideoDownloader:
    @staticmethod
    def download_video(url, filename):
        yt = YouTube(url)
        # Select the highest resolution stream
        stream = yt.streams.filter(res="1080p").first()
        # Download the video to the specified file path
        stream.download(filename=filename)

