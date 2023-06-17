import requests
import json
from helpers.postjsonwriter import PostJsonWriter
from helpers.postscraper import PostScraper
from models.post import Post
from helpers.textwriter import TextWriter
from helpers.videocreator import VideoCreator 
import asyncio
from realconfig import headers
import os
from nanoid import generate
from helpers.videodownloader import VideoDownloader
from moviepy.editor import *
from mutagen.mp3 import MP3
import glob

#queries 100 posts
params = {'limit': 100}
post_list = []
os.environ["IMAGEIO_FFMPEG_EXE"] = <filepath to ffmpeg>

async def get_posts(subreddit, post_json_writer):
    try:
        post_json_writer.append_post_to_post_list(post_list)
    except:
        res = requests.get(f"https://oauth.reddit.com/r/{subreddit}/new",
                        headers=headers, params=params)
        for index, post_json in enumerate(res.json()['data']['children']):
            post = Post.get_post_from_json(post_json, index)
            #retrieve "popular" posts with upvotes greater than 4000
            if post.upvotes >= 4000:
                post_list.append(post)
                params['after'] = post.full_id
        posts_dicts = map(lambda x: x.to_dict() ,post_list)
        output_json = json.dumps({
            "posts": list(posts_dicts)
        })
        tw = TextWriter('post_list')
        tw.write_to_file(output_json)
            
        #found a post with >= 4000 upvotes
        if params['after']:
            tw = TextWriter('a')
            tw.write_to_file(params['after'])

def run():
    print('Enter the name of a subreddit:', end=' ')
    subreddit = input()
    print('How many videos would you like?:', end=' ')
    number_of_videos = int(input())
    post_json_writer = PostJsonWriter()
    asyncio.run(get_posts(subreddit, post_json_writer))
    for _ in range(number_of_videos):
        folder_name = generate()
        asyncio.run(PostScraper(post_list).get_paragraph_screenshots_and_audio(folder_name))
        mp3_files = glob.glob(f"{folder_name}/*.mp3")
        num_of_mp3_files = len(mp3_files)
        if not os.path.exists("vid.mp4"):
            VideoDownloader.download_video("https://www.youtube.com/watch?v=n_Dv4JMiwK8", "vid.mp4")
        try:
            VideoCreator.create_video(num_of_mp3_files, folder_name)
        except Exception as e:
            print(e)
            post_json_writer.remove_post_from_json(post_list)
            continue
        post_json_writer.remove_post_from_json(post_list)

run()