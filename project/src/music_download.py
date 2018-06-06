# coding: utf-8

import youtube_dl
import sys
import os
import glob
import shutil
import magic
import eyed3
from eyed3.id3.frames import ImageFrame
from pytube import YouTube
import re

from mutagen.id3 import ID3, TIT2, TALB, TPE1, TRCK, APIC, TDRC, TCON
from mutagen.mp3 import MP3
import mutagen.id3

regex = re.compile(r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?(?P<id>[A-Za-z0-9\-=_]{11})')

def dl(URL):
	options = {
		'format': 'bestaudio[ext=mp3]/bestaudio[ext=m4a]/bestaudio',
		'outtmpl': '%(title)s.%(ext)s',
	}
	with youtube_dl.YoutubeDL(options) as ydl:
		ydl.download([URL])

def thumbnail(youtube_url, title):
	match = regex.match(youtube_url)
	if not match:
		print('no match')
	print(match.group('id'))
	os.system("wget http://i.ytimg.com/vi/'%s'/default.jpg -O '%s'.jpg" % (match.group('id'), title))


def mp4to3(filename, thumbnailName):
	root, ext = os.path.splitext(filename)
	if ext not in ['.m4a', '.mp4']: return
	newname = '%s.mp3' % root

	# video to mp3
	cmd = 'ffmpeg -i "%s" -ab 256k "%s"' % (filename, newname)
	os.system(cmd)
	os.remove(filename)


	# サムネイル画像をmp3ファイルに埋め込む
	f = eyed3.load(newname)
	print(f)
	print(f.tag)
	if f.tag is None:
		f.initTag()
	with open(thumbnailName, 'rb') as dest_png:
		f.tag.images.set(
			ImageFrame.FRONT_COVER,
			dest_png.read(),
			'image/jpeg'
		)
	f.tag.save(encoding='utf-8')

	print(newname)
	audio = MP3(newname, ID3=ID3)
    # ジャケット画像
	audio['TALB'] = TALB(encoding=3, text="うま娘")
	audio['APIC'] = APIC(
			encoding=0,        # 3 is for utf-8
			mime='image/jpeg', # image/jpeg or image/png
			type=3,            # 3 is for the cover image
			desc=u'Cover',
			data=open(thumbnailName, encoding='ISO-8859-1').read().encode()
		)
		
	audio.save(v2_version=3)	
	os.remove(thumbnailName)

	# ファイル移動
	shutil.move('./' + newname, '../assets/mp3/')


def main():
	if len(sys.argv) > 1:
		URL = sys.argv[1]
		dl(URL)
	# タイトル取得
	yt = YouTube(URL)
	title = yt.title
	thumbnail(URL, "thumbnail")

	filenames = glob.glob('./*.m4a')
	for filename in filenames:
		mp4to3(filename, "thumbnail.jpg")

	os.system("python3 ./upload.py")

main()