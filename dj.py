import youtube_scrape
import parse_emails
import time
import os
import sys
import subprocess

last_artist = ''
last_song = ''
play_queue = []
time_start = time.time()
time_to_end = 99


def handle_song():
    video_url, duration = youtube_scrape.scrape(play_queue[0][0], play_queue[0][1])
    duration = duration / 1000
    if sys.platform == 'win32':
        p1 = os.startfile(video_url)
    else:
        p1 = subprocess.Popen(['open', video_url])
    return duration, p1


while True:
    artist, song = parse_emails.readmail()

    if artist != last_artist or song != last_song:
        if not play_queue:
            time_start = time.time()
            play_queue.append([song, artist])
            time_to_end, process = handle_song()
        else:
            play_queue.append([song, artist])

    time_end = time.time()
    if time_end - time_start >= time_to_end + 3:
        os.close(process)
        play_queue.remove(0)
        time_to_end, process = handle_song()
        time_start = time.time()

    time.sleep(2)






