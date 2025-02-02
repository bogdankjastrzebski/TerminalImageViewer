#!/home/bodo/.pyenv/versions/common/bin/python
import os
import time
import argparse
import subprocess
from watchdog.observers import Observer
from watchdog.events import (
    FileSystemEventHandler,
    FileModifiedEvent,
    FileCreatedEvent,
)


def is_file(path):
    return not os.path.isdir(path)


class Watcher:
    def __init__(self, path, is_file=False):
        self.path = path
        self.observer = Observer()

    def watch(self):
        event_handler = Handler(self.path)
        self.observer.schedule(
            event_handler,
            self.path,
            recursive=True,
        )
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
        self.observer.join()


class Handler(FileSystemEventHandler):
    def __init__(self, path):
        self.path = path
        self.is_file = is_file(path)

    def on_any_event(self, event):
        #print('here')
        if event.is_directory:
            return None
        #print('there')
        if isinstance(event, (FileModifiedEvent, FileCreatedEvent)):
            path = event.src_path
            # print(f'a: {path} {self.is_file}'
            #      f' {self.path} {os.path.basename(path)}')
            if self.is_file and \
                    os.path.basename(path) != os.path.basename(self.path):
                return
            print('b')
            if path.lower().endswith(".png"):
                print('c')
                print(event.event_type)
                print(event)
                # print(f"Detected change in: {path}")
                Handler.display_image(path)

    @staticmethod
    def display_image(image_path):
        try:
            # subprocess.run(["tput", "cup", "0", "0"], check=True)
            # subprocess.run(["kitty", "icat", image_path], check=True)
            os.system(f'kitty icat {image_path}')
            print(image_path)
        except subprocess.CalledProcessError as e:
            print(f"Error displaying image: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=(
        "Monitor a directory for PNG file changes"
        "and display them with kitty icat."
    ))
    parser.add_argument("directory", help="The directory to watch")
    args = parser.parse_args()
 
    w = Watcher(args.directory)
    subprocess.run(["clear"], check=True)
    w.watch()
