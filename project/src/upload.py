from gmusicapi import Mobileclient
from gmusicapi import Musicmanager
import os

def main():
    upload("../assets/mp3/")

def upload(path):
    mm = Musicmanager()
    mm.login()

    for root, dirs, files in os.walk(path):
        for file_ in files:
            mp3FilePath = os.path.join(root, file_)
            print( "upload : " + file_ )
            mm.upload(mp3FilePath)
            os.remove(mp3FilePath)

if __name__ == "__main__":
    main()
