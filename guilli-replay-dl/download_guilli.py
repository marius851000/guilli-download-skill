import requests
from lxml import etree

url = "https://replay.gulli.fr/dessins-animes/Pokemon113/VOD68824145382000"
url = "https://replay.gulli.fr/dessins-animes/Ben-10/VOD68908592105000"
#like http://gulli-replay-transmux.scdn.arkena.com/68861986788000/68861986788000_Ipad.smil/68861986788000_Ipad-audio=64000-video=750000.m3u8

def download_guilli(url):
    id = url.split("/")[len(url.split("/"))-1]
    if len(id.split("VOD"))>1:
        id = id.split("VOD")[1]
    else:
        return False
    audios = ["64000"]
    videos = ["64000","200000","350000","750000"]
    possibility = []
    for audio in audios:
        for video in videos:
            possibility.append("http://gulli-replay-transmux.scdn.arkena.com/"+id+"/"+id+"_Ipad.smil/"+id+"_Ipad-audio="+audio+"-video="+video+".m3u8")

    r = requests.get(url)
    if r.status_code == 200:
        html = r.text
    else:
        raise

    a = open("temp.html","w")
    a.write(html)
    a.close()

    obtained = []

    got = {}
    data = etree.parse("temp.html", etree.HTMLParser())
    for section in data.iter("section"):
        if "id" in section.attrib:
            if section.attrib["id"] == "main":
                container = section.find("div")
                #get the serie name
                serie = container.find("h2").find("span")
                serieSTR = serie.text
                # TODO: fix

                serieSTR2 = []
                for loop in serieSTR.split(" "):
                    if loop != "" and loop != "\n":
                        serieSTR2.append(loop)
                serieSTR = serieSTR2[0:len(serieSTR2)-2]
                serieSTR2 = ""
                for loop in serieSTR:
                    serieSTR2 += loop + " "
                serieSTR = serieSTR2[0:len(serieSTR2)-1]
                if serieSTR == "":
                    for titre_top in container.find("h2"):
                        theString = str(etree.tostring(titre_top))
                        theString = theString.split("/>\\n")[1]
                        theString = theString.split("\\n")[0]
                        serieSTR2 = []
                        for loop in theString.split(" "):
                            if loop != "":
                                serieSTR2.append(loop)
                        serieSTR = ""
                        for loop in serieSTR2:
                            serieSTR += loop + " "
                        serieSTR = serieSTR.split("en streaming")[0]
                        
                got["serie"] = serieSTR


                for title in container.iter("h1"):
                    if "id" in title.attrib:
                        if title.attrib["id"] == "myEpisodeTitle":
                            titleSTR = title.text
                            titleSTR = titleSTR.split(" ")
                            titleSTR2 = []
                            for loop in titleSTR:
                                if loop != "" and loop != "\n":
                                    titleSTR2.append(loop)
                            titleSTR = ""
                            for loop in titleSTR2:
                                titleSTR += loop + " "
                            titleSTR = titleSTR[0:len(titleSTR)-2]
                            titleSTR2 = titleSTR.split(":")
                            previous = titleSTR2[0]
                            after = titleSTR2[1:len(titleSTR2)]
                            after2 = ""
                            for loop in after:
                                after2 += loop
                            after = after2

                            previousSplited = previous.split(",")
                            saisonNB = previousSplited[0].split(" ")[1]
                            got["saison"] = saisonNB
                            epiNB = previousSplited[1].split(" ")[2]
                            got["episode"] = epiNB
                            got["title"] = after

    got["file"] = possibility
    return got

if __name__ == '__main__':
    print(download_guilli(url))
