import sys
import time
import logging
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MarconaServerRestart(FileSystemEventHandler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print('init event handler')
        self.start_process()
    
    def on_any_event(self, event):
        print('file change happened')
        self.stop_process()
        self.start_process()

    def start_process(self):
        self.process = subprocess.Popen(['python', 'marcona_server.py'])

    def stop_process(self):
        self.process.kill()


path = sys.argv[1] if len(sys.argv) > 1 else '.'
event_handler = MarconaServerRestart()
observer = Observer()
observer.schedule(event_handler, path, recursive=True)
observer.start()
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()