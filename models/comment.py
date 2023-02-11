class Comment:
    def __init__(self, id, url, content, replies_json):
        self.id = id
        self.url = url
        self.content = content
        self.replies_json = replies_json
        self.__top_level_replies = []
        self.number_of_top_level_replies = 0

    def get_top_level_replies(self):
        if self.__top_level_replies:
            return self.__top_level_replies
        else:
            replies_list = []
            if self.replies_json:
                for reply_json in self.replies_json['data']['children']:
                    url = f"https://reddit.com{reply_json['data']['permalink']}"
                    reply = Comment(reply_json['data']['id'], url, reply_json['data']['body'], reply_json['data']['replies'])
                    replies_list.append(reply)
            self.__top_level_replies = replies_list
            return replies_list