class TextWriter:
    def __init__(self, filename):
        self.filename = filename + ".json"

    def write_to_file(self, content):
        f = open(self.filename, "w")
        f.write(content)
        f.close()