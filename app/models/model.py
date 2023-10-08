class FileDatabase:
    def __init__(self):
        # Simulating a file database with a simple list
        self.files = ["document1.txt", "photo1.jpg", "music1.mp3", "document2.txt"]

    def search_files(self, query):
        # Return all files that contain the query
        return [file for file in self.files if query in file]
