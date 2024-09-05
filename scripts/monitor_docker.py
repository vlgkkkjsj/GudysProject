import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class DockerEventHandler(FileSystemEventHandler):
    def __init__(self, build_and_up_command, prune_command):
        self.build_and_up_command = build_and_up_command
        self.prune_command = prune_command
        super().__init__()

    def on_any_event(self, event):
        print(f'Change detected: {event.event_type} on {event.src_path}')
        self.run_prune_and_build()

    def run_prune_and_build(self):
        try:
            print("Pruning unused Docker objects...")
            subprocess.run(self.prune_command, check=True)
            print("Building and starting containers...")
            subprocess.run(self.build_and_up_command, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error occurred: {e}")

if __name__ == "__main__":
    path = '.'  # Monitorar o diretório atual
    build_and_up_command = ['docker-compose', 'up', '--build', '-d']
    prune_command = ['docker', 'system', 'prune', '-a', '-f']
    
    event_handler = DockerEventHandler(build_and_up_command, prune_command)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    print("Monitoring started. Press Ctrl+C to stop.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("Monitoring stopped.")

    observer.join()
