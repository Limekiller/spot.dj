import youtube_scrape
import parse_emails

import time
import os
import math
import youtube_dl
import pygame
import mutagen.mp3

last_artist = ''
last_song = ''
play_queue = []
time_start = time.time()
time_to_end = math.inf


def handle_song(title):
    video_url, duration = youtube_scrape.scrape(play_queue[0][0], play_queue[0][1])
    duration = duration / 1000

    options = {
        'format': 'bestaudio/best',
        'outtmpl': './Music/'+title+".%(ext)s",
        'postprocessors': [{
            'key':'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }]
    }
    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download([video_url])

    # os.rename('./Music/'+title+'.mp4', './Music/'+title+'.mp3')
    return duration


while True:
    artist, song = parse_emails.readmail()
    print(play_queue)

    if artist != last_artist or song != last_song:
        last_artist, last_song = artist, song
        if not play_queue:
            play_queue.append([song, artist])
            time_to_end = handle_song(song)

            if not time_to_end:
                last_artist, last_song = '', ''
                continue

            mp3 = mutagen.mp3.MP3("./Music/"+song+".mp3")
            pygame.mixer.init(frequency=mp3.info.sample_rate)
            pygame.mixer.music.load("./Music/"+song+".mp3")
            pygame.mixer.music.play()

            time_start = time.time()

        else:
            play_queue.append([song, artist])

    time_end = time.time()
    if time_end - time_start >= time_to_end + 3:

        os.remove('./Music/'+play_queue[0][0]+'.mp3')
        play_queue.pop(0)
        if play_queue:
            time_to_end = handle_song(song)
            time_start = time.time()

            mp3 = mutagen.mp3.MP3("./Music/" + song + ".mp3")
            pygame.mixer.init(frequency=mp3.info.sample_rate)
            pygame.mixer.music.load("./Music/" + song + ".mp3")
            pygame.mixer.music.play()
        else:
            time_to_end = math.inf
    time.sleep(2)






