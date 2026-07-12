import json
import os


class DocumentMetadataStore:
    def __init__(self, file_path="metadata.json"):
        self.file_path = file_path
        if os.path.exists(self.file_path):
            with open(self.file_path) as f:
                self.data = json.load(f)
        else:
            self.data = {}

            
