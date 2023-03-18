import os
from playwright.async_api import async_playwright, ViewportSize
from PIL import Image, ImageOps

from helpers.texttospeech import TextToSpeechGenerator
from models.title_image import TitleImage

class PostScraper:
    def __init__(self, post_list):
        self.post_list = post_list

    async def get_paragraph_screenshots_and_audio(self, folder_name):
        async with async_playwright() as p:
            browser, page = await self.initialise_page(folder_name, p)
            upvotes_path = f"{folder_name}/upvotes.png"
            header_path = f"{folder_name}/header.png"
            labels_path = f"{folder_name}/labels.png"
            title_path = f"{folder_name}/title.png"
            output_path = f"{folder_name}/paragraph_0.png"

            post = await page.query_selector('[data-test-id="post-content"]')
            title = await page.query_selector('[data-adclicklocation="title"]')
            upvotes = await post.query_selector(':nth-child(1)') 
            header = await post.query_selector(':nth-child(2) > :nth-child(1)')
            labels = await post.query_selector(':nth-child(4)') 

            await upvotes.screenshot(path=upvotes_path)
            await header.screenshot(path=header_path)
            await labels.screenshot(path=labels_path)
            await title.screenshot(path=title_path)

            title_image = TitleImage(title_path, header_path, labels_path, upvotes_path, output_path)
            title_image.save_title_image()

            await TextToSpeechGenerator.get_speech_from_post(await title.inner_text(), f"{folder_name}/0")

            #start of the post's body
            post_body = await post.query_selector(':nth-child(5) > :nth-child(1)')
            children = await post_body.query_selector_all('p')
            await self.save_screenshots_and_audio(folder_name, children)

            await browser.close()

    async def save_screenshots_and_audio(self, folder_name, children):
        file_count = 0
        for paragraph in children:
            #skip paragraph breaks from being screenshotted
            paragraph_text = await paragraph.inner_html()
            if (paragraph_text != "<br>"):
                await paragraph.screenshot(path=f"{folder_name}/paragraph_{file_count + 1}.png")
                image = Image.open(f"{folder_name}/paragraph_{file_count + 1}.png")

                    # Add padding to the image
                padded_image = ImageOps.expand(image, border=10, fill='white')

                    # Save the padded image
                padded_image.save(f"{folder_name}/paragraph_{file_count + 1}.png")
                await TextToSpeechGenerator.get_speech_from_post(paragraph_text, f"{folder_name}/{file_count + 1}")
                file_count += 1

    async def initialise_page(self, folder_name, p):
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
        url = self.post_list[0].url 
        print(url)
        await page.goto(url)
        return browser,page