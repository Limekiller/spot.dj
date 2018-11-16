import youtube_scrape
import parse_emails
import time
import math
import playsound
import pytube

last_artist = ''
last_song = ''
play_queue = []
time_start = time.time()
time_to_end = 99


def handle_song(title):
    video_url, duration = youtube_scrape.scrape(play_queue[0][0], play_queue[0][1])
    duration = duration / 1000
    yt = pytube.YouTube(video_url)
    stream = yt.streams.filter(only_audio=True, file_extension='mp3').first()
    download_start = time.time()

    print(download_start)
    stream.download('./Music', title)
    download_end = time.time()
    print(download_end)
    return duration


while True:
    artist, song = parse_emails.readmail()

    if artist != last_artist or song != last_song:
        last_artist, last_song = artist, song
        if not play_queue:
            time_start = time.time()
            play_queue.append([song, artist])
            time_to_end = handle_song(song)
            playsound.playsound('/Music/'+song+'.mp3')
        else:
            play_queue.append([song, artist])

    time_end = time.time()
    if time_end - time_start >= time_to_end + 3:

        play_queue.pop(0)
        if play_queue:
            time_to_end = handle_song(song)
            time_start = time.time()
            playsound.playsound('/Music/'+song+'.mp3')
        else:
            time_to_end = math.inf
    time.sleep(2)






