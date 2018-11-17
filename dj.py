import youtube_scrape
import parse_emails
import artist_finder

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
loops_without_music = 0


def handle_song(title):
    video_url, duration = youtube_scrape.scrape(play_queue[0][0], play_queue[0][1])

    if not duration:
        return duration

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

    return duration


def start_song(song):
    song_file = mutagen.mp3.MP3("./Music/" + song + ".mp3")
    pygame.mixer.init(frequency=song_file.info.sample_rate)
    pygame.mixer.music.load("./Music/" + song + ".mp3")
    pygame.mixer.music.play()


while True:
    artist, song = parse_emails.readmail()
    print(play_queue)

    if artist != last_artist or song != last_song:
        loops_without_music = 0
        last_artist, last_song = artist, song

        if not play_queue:
            play_queue.append([song, artist])
            time_to_end = handle_song(song)
            if not time_to_end:
                last_artist, last_song = '', ''
                continue
            start_song(song)
            time_start = time.time()
        else:
            play_queue.append([song, artist])

    time_end = time.time()
    if time_end - time_start >= time_to_end + 3:
        can_remove = False
        while not can_remove:
            pygame.mixer.stop()
            pygame.mixer.quit()
            try:
                os.remove('./Music/'+play_queue[0][0]+'.mp3')
                can_remove = True
            except PermissionError:
                pass

        last_played_artist = play_queue[0][1]
        play_queue.pop(0)

        if play_queue:
            time_to_end = handle_song(song)
            time_start = time.time()
            if not time_to_end:
                last_artist, last_song = '', ''
                continue
            start_song(song)
        else:
            time_to_end = math.inf

    if loops_without_music > 5:
        loops_without_music = 0
        artist = artist_finder.find_similar_artist(last_played_artist)
        song = artist_finder.get_artist_song(artist)

        play_queue.append([song, artist])
        time_to_end = handle_song(song)
        if not time_to_end:
            last_artist, last_song = '', ''
            continue
        start_song(song)
        time_start = time.time()

    if not play_queue:
        loops_without_music += 1

    time.sleep(2)






