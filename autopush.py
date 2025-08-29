import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess

# Path to your Git repository
repo_path = "C:/Users/owyya/OneDrive/Documents/todo"

class GitCommitPushHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return

        # Check if the event is a file modification (not deletion)
        if event.event_type == 'modified':
            print(f"File {event.src_path} modified. Checking for changes...")

            # Check if there are uncommitted changes before committing
            if self.has_uncommitted_changes():
                print(f"Uncommitted changes found. Committing and pushing changes...")
                self.git_commit_push()
            else:
                print("No changes to commit.")

    def has_uncommitted_changes(self):
        # Check for uncommitted changes using `git status --porcelain`
        result = subprocess.run(['git', 'status', '--porcelain'], cwd=repo_path, text=True, capture_output=True)

        # If the result is non-empty, there are uncommitted changes
        return len(result.stdout.strip()) > 0

    def git_commit_push(self):
        # Navigate to the repo directory (in case we're not already there)
        os.chdir(repo_path)

        # Stage all changes
        subprocess.run(['git', 'add', '.'])

        # Commit changes if there are changes to commit
        commit_message = "Auto commit and push"
        subprocess.run(['git', 'commit', '-m', commit_message])

        # Push to the remote repo
        subprocess.run(['git', 'push'])

if __name__ == "__main__":
    # Create the event handler and observer
    event_handler = GitCommitPushHandler()
    observer = Observer()
    observer.schedule(event_handler, path=repo_path, recursive=True)

    # Start observing the repository
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()