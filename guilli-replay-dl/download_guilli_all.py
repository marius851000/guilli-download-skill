import requests
from lxml import etree
import download_guilli_playlist as dlp
import download_guilli as dlg

def download_guilli_all():
    url = "https://replay.gulli.fr/all"
    r = requests.get(url)
    if r.status_code == 200:
        html = r.text
    else:
        raise

    a = open("temp.html","w")
    a.write(html)
    a.close()

    obtained = []

    data = etree.parse("temp.html", etree.HTMLParser())
    for program in data.iter("div"):
        if "class" in program.attrib:
            if program.attrib["class"] == "wrap-img program":
                lien = program.find("a")
                obtained.append(lien.attrib["href"])

    final = []
    count = 0
    for program in obtained:
        count += 1
        td = dlp.get_guilli_playlist(program)
        for loop in td:
            if loop != False:
                final.append(dlg.download_guilli(loop["url"]))

    return final

if __name__ == '__main__':
    listURL = download_guilli_all()

    ext = "mp4"
    for toDL in listURL:
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
