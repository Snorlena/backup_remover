"""Script to remove old backups"""
import os
import configparser
import sys
from datetime import datetime, timedelta


def remove_backups(path, days_since_mod, minimum_size, file_extension):
    """Remove old backups from path"""
    treshold = datetime.now() - (timedelta(days=days_since_mod))

    try:
        entries = os.listdir(path)
    except FileNotFoundError:
        print("The path:", path, "could not be found")
        sys.exit(1)

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
        try:
            data = dict(config.items(section))
        except KeyError:
            print("No sections in the config file")
            sys.exit(1)

        try:
            filepath = data["path"]
            last_modified = data["last_modified"]
            min_size = data["size"]
            file_ext = data["file_extensions"].replace(" ","").split(",")
        except KeyError as key:
            print(key, "could not be found in the", section, "section of the config.")
            sys.exit(1)

        remove_backups(filepath, int(last_modified), int(min_size), file_ext)
