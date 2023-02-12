import requests
import json
from models.post import Post
from models.comment import Comment 
from helpers.textwriter import TextWriter
import asyncio
from helpers.texttospeech import TextToSpeechGenerator
from config import headers
from playwright.async_api import async_playwright, ViewportSize
import os
from nanoid import generate


#queries 100 posts
params = {'limit': 100}
post_list = []

def get_posts():
    try:
        with open('post_list.json') as f:
            json_data = json.load(f)
            for post_json in json_data['posts']:
                post = Post(post_json['id'], post_json['title'], post_json['url'], post_json['content'], post_json['upvotes'])
                post_list.append(post)
    except:
        res = requests.get("https://oauth.reddit.com/r/maliciouscompliance/new",
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

async def get_paragraph_screenshots(folder_name):
    async with async_playwright() as p:
        browser, page = await initialise_page(folder_name, p)
        post = await page.query_selector('[data-test-id="post-content"]')
        title = await page.query_selector('[data-adclicklocation="title"]')

        #screenshot title
        await title.screenshot(path=f"{folder_name}/title.png")

        #start of the post's body
        post_body = await post.query_selector(':nth-child(5) > :nth-child(1)')
        children = await post_body.query_selector_all('p')
        for i, paragraph in enumerate(children):
            #skip paragraph breaks from being screenshotted
            if (await paragraph.inner_html() != "<br>"):
                await paragraph.screenshot(path=f"{folder_name}/paragraph_{i+1}.png")

        await browser.close()

async def initialise_page(folder_name, p):
    #code adapted from https://github.com/elebumm/RedditVideoMakerBot/blob/master/video_creation/screenshot_downloader.py to optimise screenshot quality
    browser = await p.chromium.launch()
    os.mkdir(folder_name)
    W = 1080
    H = 1920
    dsf = (W // 600) + 1

    context = await browser.new_context(viewport=ViewportSize(width=W, height=H), device_scale_factor=dsf)
    page = await context.new_page()
    await page.set_viewport_size(ViewportSize(width=W, height=H))

        # Navigate to the reddit post and select the post element
    url = post_list[0].url 
    await page.goto(url)
    return browser,page

def get_audio(folder_name):
    TextToSpeechGenerator.get_speech_from_post(post_list[0].content, f"{folder_name}/audio.mp3")


get_posts()
folder_name = generate()
asyncio.run(get_paragraph_screenshots(folder_name))
get_audio(folder_name)






