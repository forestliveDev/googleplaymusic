import os


def main():
    upload("../assets/path/")

def upload(path):

    for root, dirs, files in os.walk(path):
        for file_ in files:
            filePath = os.path.join(root, file_)
            print( "upload : " + file_ )
            print(file_)
            os.system('python3 music_download.py https://www.youtube.com/watch?v=' + file_)
            os.remove(filePath)

if __name__ == "__main__":
    main()
