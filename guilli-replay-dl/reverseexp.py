test = {
    "type" : "add",
    "add" : [
        {
            "type" : "str",
            "str" : "https://foipop.novascotia.ca/foia/views/_AttachmentDownload.jsp?attachmentRSN="
        },
        {
            "type" : "rangeINT",
            "start" : 0,
            "end" : 40
        }
    ]
}

def get_all(rexp):

    possible = []
    if rexp["type"] == "str":
        possible = [rexp["str"]]
    elif rexp["type"] == "pos":
        for pos in rexp["pos"]:
            r = get_all(pos)
            for loop in r:
                possible.append(loop)
    elif rexp["type"] == "add":
        for loop in rexp["add"]:
            r = get_all(loop)
            if len(possible) == 0:
                possible = r
            else:
                possible = split_list(possible, r)
    elif rexp["type"] == "0to9":
        possible =  ["0","1","2","3","4","5","6","7","8","9"]
    elif rexp["type"] == "rangeINT":
        for loop in range(rexp["start"], rexp["end"]+1):
            possible.append(str(loop))

    return possible

def split_list(liste1, liste2):
    rendu = []
    for loop1 in liste1:
        for loop2 in liste2:
            rendu.append(loop1+loop2)
    return rendu

t = get_all(test)
rendu = ""
for loop in t:
    rendu += loop + "\n"
print(rendu)
#print(split_list(["salut","le"],["monde"]))
