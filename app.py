import requests
import json
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

def get_video_length(folder_name):
    mp3_files = glob.glob(f"{folder_name}/*.mp3")
    num_of_mp3_files = len(mp3_files)
    video_length = 0
    print(num_of_mp3_files)
    for i in range(num_of_mp3_files - 1):
        video_length += MP3(f"{folder_name}/{i}.mp3").info.length
    return video_length

async def get_posts(subreddit):
    try:
        with open('post_list.json') as f:
            json_data = json.load(f)
            for post_json in json_data['posts']:
                post = Post(post_json['id'], post_json['title'], post_json['url'], post_json['content'], post_json['upvotes'])
                post_list.append(post)
    except:
        res = requests.get(f"https://oauth.reddit.com/r/{subreddit}/new",
                        headers=headers, params=params)
        for index, post_json in enumerate(res.json()['data']['children']):
            post = Post.get_post_from_json(post_json, index)
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

def remove_post_from_json(post_list):
    post_list.pop(0)
    with open('post_list.json') as f:
            json_data = json.load(f)
            json_data['posts'].pop(0)
            print(json_data['posts'][0])
            tw = TextWriter('post_list')
            output_json = json.dumps(json_data)
            tw.write_to_file(output_json)
def run():
    print('Enter the name of a subreddit:', end=' ')
    subreddit = input()
    print('How many videos would you like?:', end=' ')
    number_of_videos = int(input())
    asyncio.run(get_posts(subreddit))
    for _ in range(number_of_videos):
        folder_name = generate()
        asyncio.run(PostScraper(post_list).get_paragraph_screenshots_and_audio(folder_name))
        video_length = get_video_length(folder_name)
        mp3_files = glob.glob(f"{folder_name}/*.mp3")
        num_of_mp3_files = len(mp3_files)
        if not os.path.exists("vid.mp4"):
            VideoDownloader.download_video("https://www.youtube.com/watch?v=n_Dv4JMiwK8", "vid.mp4")
        try:
            VideoCreator.create_video(num_of_mp3_files, folder_name)
        except Exception as e:
            print(e)
            remove_post_from_json(post_list)
            continue
        remove_post_from_json(post_list)

run()