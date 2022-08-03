"""Script to remove old backups"""
import os
import configparser
import json
from datetime import datetime, timedelta


def remove_backups(path, days_since_mod, minimum_size, file_extension):
    """Remove old backups from path"""
    treshold = datetime.now() - (timedelta(days=days_since_mod))
    entries = os.listdir(path)

    for file in entries:
        # Get modification time from file
        mod_time = datetime.fromtimestamp(os.stat(os.path.join(path, file)).st_mtime)
        # Get filesize of file
        file_size = os.stat(os.path.join(path, file)).st_size
        for extension in file_extension:
            # Check if file has extension to be removed.
            if os.path.join(path, file).endswith(extension):
                if mod_time < treshold and file_size > minimum_size:
                    os.remove(os.path.join(path, file))
                    print(file, "has been removed")


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("config.ini")

    for section in config.sections():
        data = dict(config.items(section))
        filepath = data["path"]
        last_modified = data["last_modified"]
        min_size = data["size"]
        file_ext = json.loads(data["file_extensions"])
        remove_backups(filepath, int(last_modified), int(min_size), file_ext)
