#! /usr/bin/python
import os
import time

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class WatchHandler(FileSystemEventHandler):
    patterns = ["location.gpx"]

    def on_modified(self, event):
        os.system("osascript click_menu.applescript > /dev/null 2>&1")
        print("updated location..")


if __name__ == "__main__":
    event_handler = WatchHandler()
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
