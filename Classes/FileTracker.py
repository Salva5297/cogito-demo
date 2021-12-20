

class FileTracker:

    def __init__(self, id):
        self.file_id = id


    def store_file(self, file_path, file_type):
        """
        Store file in the "file storage" / "relational database"
        """
        # file.name = file_id + file_type
        return