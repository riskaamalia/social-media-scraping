import youtube_dl

ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s%(ext)s'})

with ydl:
    result = ydl.extract_info(
        'https://www.facebook.com/BeritagarID/videos/10154922854401078/',
        download=False # We just want to extract the info
    )

if 'entries' in result:
    # Can be a playlist or a list of videos
    video = result['entries'][0]
else:
    # Just a video
    video = result

video_urls = video['formats']
previous_video = ''
longest_url = ''
for video_url in video_urls :
    longest_url = video_url['url']
    if previous_video > longest_url :
        longest_url = previous_video

    previous_video = video_url['url']

print longest_url
    # di read kalo content lengthnya panjang baru, kalo pendek berarti invalid url , update
    # ambil url terpanjang

# import os
# os.system('youtube-dl https://www.facebook.com/BeritagarID/videos/10154922854401078/')