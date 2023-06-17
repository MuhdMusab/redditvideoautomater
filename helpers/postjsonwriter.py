import json

from helpers.textwriter import TextWriter
from models.post import Post

class PostJsonWriter:
    def remove_post_from_json(post_list):
        post_list.pop(0)
        with open('post_list.json') as f:
                json_data = json.load(f)
                json_data['posts'].pop(0)
                print(json_data['posts'][0])
                tw = TextWriter('post_list')
                output_json = json.dumps(json_data)
                tw.write_to_file(output_json)
    
    def append_post_to_post_list(post_list):
        with open('post_list.json') as f:
            json_data = json.load(f)
            for post_json in json_data['posts']:
                post = Post(post_json['id'], post_json['title'], post_json['url'], post_json['content'], post_json['upvotes'])
                post_list.append(post)