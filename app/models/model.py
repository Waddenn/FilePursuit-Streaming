class FileDatabase:
    def __init__(self):
        # Simulons une base de données de fichiers avec une simple liste
        self.files = ["document1.txt", "photo1.jpg", "music1.mp3", "document2.txt"]

    def search_files(self, query):
        # Retourner tous les fichiers qui contiennent la requête
        return [file for file in self.files if query in file]
