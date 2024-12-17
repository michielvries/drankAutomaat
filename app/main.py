import sys
import time
import subprocess


def install_poetry_dependencies():
    try:
        subprocess.run(["poetry", "install", "--sync"], check=True)
    except subprocess.CalledProcessError:
        print("Failed to install poetry dependencies, trying to resolve issues..")
        subprocess.run(["poetry", "lock", "--no-update"], check=True)
        print("Fixed poetry lock file, restart main.py to start the environment")
        time.sleep(5)
        return False
    return True

if __name__ == "__main__":
    if not install_poetry_dependencies():
        sys.exit(1)

    print("Poetry dependencies installed successfully!")
    print("Starting the app...")