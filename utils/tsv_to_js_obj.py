import requests, zipfile, io
from bs4 import BeautifulSoup

def get_item_names(parts):
    partnames = []
    partnos = [part.strip("\"\n \'") for part in parts.split(',')]
    print(partnos);
    for partno in partnos:
        if partno == '':
            continue

        if partno.startswith('bb'):
            typ = 'G'
        else:
            typ = 'P'
        r = requests.get("https://www.bricklink.com/v2/catalog/catalogitem.page?" + typ + "=" + partno, headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
        if r.status_code != 200:
            print("Error retrieving bl page for part: ", partno)
            exit(-1)

        span = BeautifulSoup(r.text).find("span", {"id": "item-name-title"})

        try:
            partname = span.text
            partnames.append(partname) 
        except:
            continue
    return partnames
        
def main():
    sheetzip = requests.get("https://docs.google.com/spreadsheets/d/1TP0Rwawa3ELegEJ63vOX-B8gjMhH20R_usnD1WiaUow/export?format=zip", headers= {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
    if sheetzip.status_code != 200:
        print("Error retrieving zip")
    z = zipfile.ZipFile(io.BytesIO(sheetzip.content))
    z.extractall()
    html = open("./Technique Cheat Code.html", "r")
    soup = BeautifulSoup(html, "html.parser")
    html.close()
    imgs = [img["src"] for img in soup.find_all('img')]
    print(len(imgs))
    fr = requests.get("https://docs.google.com/spreadsheets/d/1TP0Rwawa3ELegEJ63vOX-B8gjMhH20R_usnD1WiaUow/export?format=tsv", headers= {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
    if fr.status_code != 200:
        print('Error retrieving tsv')
        exit(-2)
    f = fr.text
    data = f.split('\n')
    data = data[1::]
    print(data)
    jstext = "const techniques = [\n"
    print(len(data))
    for img, datum in zip(imgs, data):
        values = datum.split("\t")
        #print("before: ", values)
        for i in range(len(values)):
            values[i] = values[i].strip(" \n\t\r")
        #print("after: ", values)
        parts = '"' + values[2].replace(',', '","') + '"'
        partnames = str(get_item_names(parts))
        jstext+= f"{{imageURL: '{img}', Parts: [{parts}], Type: '{values[3]}', Notes: '{values[4]}', Partnames: {partnames}}},"

    jstext += "]; \n export default techniques;"

    with open("../techniques.js", "w") as j:
        j.write(jstext)

if __name__ == "__main__":
    main()

