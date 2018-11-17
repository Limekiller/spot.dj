import requests
import random
from bs4 import BeautifulSoup


def find_similar_artist(artist_name):
    artist_name = artist_name.replace(" ", "+")
    header = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}

    try:
        response = requests.get("http://www.similar-artist.info/similarto/artist/"+artist_name, headers=header)
    except requests.exceptions.ConnectionError:
        return None

    content = response.content
    soup = BeautifulSoup(content, "html.parser")
    similar_artists = []
    all_title_tags = soup.find_all("div", attrs={"class": "discounted-item"})

    for div in all_title_tags[1:]:
        similar_artists.append(div.find('h1').contents[0].lower())

    final_artist = random.choice(similar_artists)
    return final_artist


def get_artist_song(final_artist):
    header = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}

    try:
        response = requests.get("http://www.top50songs.info/artist.php?artist="+final_artist, headers=header)
    except requests.exceptions.ConnectionError:
        return None

    content = response.content
    soup = BeautifulSoup(content, "html.parser")
    songs = []
    all_title_tags = soup.find_all("li")

    for li in all_title_tags:
        songs.append(li.find("a")['title'].lower())

    final_song = random.choice(songs)
    return final_song