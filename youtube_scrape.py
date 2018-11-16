from bs4 import BeautifulSoup
import requests
import re


def rank_results(result_list, search_title, search_artist):

    scores = []

    for title in result_list:
        score = 0
        if search_title in title:
            score += 1
        if search_artist in title:
            score += 1
        if search_title in title and search_artist in title:
            score += 1
        if title == search_title:
            score = 100
        scores.append(score)

    return scores.index(max(scores))


def get_video_time(url):
    header = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}

    try:
        response = requests.get(url, headers=header)
    except requests.exceptions.ConnectionError:
        return None

    content = response.content
    soup = BeautifulSoup(content, "html.parser")
    string_to_search = soup(text=re.compile('approxDurationMs'))[0]
    slice_beginning = string_to_search.index('approxDurationMs')+len("approxDurationMs")
    slice_end = string_to_search.index('audioSampleRate')
    unrefined_time = string_to_search[slice_beginning:slice_end]
    refined_time = ''.join(c for c in unrefined_time if c.isdigit())

    return int(refined_time)


def scrape(search_title, search_artist):
    search_artist = search_artist.replace(" ", "+")
    search_title = search_title.replace(" ", "+")

    search_query = search_title + "+" + search_artist
    youtube_url = "https://www.youtube.com/results?search_query=" + search_query
    header = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}

    try:
        response = requests.get(youtube_url, headers=header)
    except requests.exceptions.ConnectionError:
        return None

    content = response.content
    soup = BeautifulSoup(content, "html.parser")
    title = []
    ref = []
    all_title_tags = soup.find_all("h3", attrs={"class": "yt-lockup-title"})

    for h3 in all_title_tags:
        title.append(h3.find('a').contents[0])
        ref.append(h3.find('a')['href'])

    best_title = rank_results(title, search_title, search_artist)
    print("Best result is: '"+str(title[best_title])+"' at index "+str(best_title))
    final_url = 'https://www.youtube.com'+ref[best_title]

    video_length = get_video_time(final_url)
    print("Video length is "+str(video_length)+' ms long')
    return final_url, video_length
