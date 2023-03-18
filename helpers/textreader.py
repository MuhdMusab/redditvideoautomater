class TextReader:
    def __init__(self, filename):
        self.filename = filename + ".txt"

    def read_from_file(self):
        try:
            f = open(self.filename, "r")
            content = f.readlines()
            f.close()
            return content
        except Exception as e:
            print(e)
            return None