import sys
import subprocess

def main():
    subprocess.run(["python", "manage.py", "runserver"])

def collectstatic():
    subprocess.run(["python", "manage.py", "collectstatic"])