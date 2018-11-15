from bs4 import BeautifulSoup
import requests

title = "Riptide"
artist = "Vance Joy"

def scrape(search_title, search_artist):
    artist = search_artist.replace(" ","+")
    search_query = search_title + "+" + artist
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

    sequence = ["S.No", "Title"]
    t = PrettyTable(sequence)
    sz = len(title)
    print("Results found = " + str(sz))
    sys.setrecursionlimit(100000)
    for i in range(sz):
        t.add_row([i + 1, title[i]])
    if len(title) != 0:
        print(color.BOLD + color.CYAN + "\nResults : " + color.END)
        print(t)

        choice = input(color.CYAN + color.BOLD + "\nEnter your choice (numerical) : " + color.END)
        if 1 <= int(choice) <= len(title):
            filename = title[int(choice) - 1]
            video_url = "https://www.youtube.com" + str(ref[int(choice) - 1])
            return filename, video_url
        else:
            print("Invalid entry.")
            sys.exit()
    else:
print(color.BOLD + color.CYAN + "Sorry, no results found." + color.END)


