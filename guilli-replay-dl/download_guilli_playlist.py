import requests
from lxml import etree
url = "https://replay.gulli.fr/dessins-animes/Pokemon113"

def get_guilli_playlist(playlistURL):
    r = requests.get(playlistURL)
    if r.status_code == 200:
        html = r.text
    else:
        raise

    a = open("temp.html","w")
    a.write(html)
    a.close()

    obtained = []

    data = etree.parse("temp.html", etree.HTMLParser())
    for div in data.iter("div"):
        if "class" in div.attrib:
            if div.attrib["class"] == "all-videos":# all-videos here
                liste = div.find("ul")
                for movie in liste.findall("li"):
                    actual = {}
                    link = movie.find("a")
                    actual["url"] = link.attrib["href"]
                    actual["thumb"] = link.find("img").attrib["src"]
                    # TODO: find the movie title
                    obtained.append(actual)
    return obtained

if __name__ == '__main__':
    listURL = get_guilli_playlist(url)

    ext = "mp4"
    from download_guilli import download_guilli
    for toDL in listURL:
        toDL = download_guilli(toDL["url"])
        if toDL != False:
            name = toDL["serie"]+":S"+toDL["saison"]+"E"+toDL["episode"]+ " :" + toDL["title"]
            # check name for special character
            name2 = ""
            for loop in name:
                if loop == "\"":
                    loop = "\\\""
                name2 += loop
            name = name2
            command = "youtube-dl " + toDL["file"][0] + " -o \"" + name+"."+ext+"\""
            print(command)
