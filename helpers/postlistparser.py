from helpers.textreader import TextReader 

class PostListParser:
    @staticmethod
    def parse_post_list(filename):
        tr = TextReader(filename)
        content = tr.read_from_file()
        return content