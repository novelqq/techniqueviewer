from bs4 import BeautifulSoup
html = open("./techniques/Technique Cheat Code.html", "r")
soup = BeautifulSoup(html, "html.parser")
html.close()
imgs = [img["src"] for img in soup.find_all('img')]
print(len(imgs))

with open("./Techniques Cheat code - Technique Cheat Code.tsv", "r") as f:
    _ = f.readline()
    data = [x for x in f.readlines()] 
    jstext = "const techniques = [\n"
    imgindex = 0
    print(len(data))
    for img, datum in zip(imgs, data):
        values = datum.strip(" \n").split("\t")
        parts = '"' + values[2].replace(',', '","') + '"'
        jstext+= f"{{imageURL: '{img}', Parts: [{parts}], Type: '{values[3]}', Notes: '{values[4]}'}},"

    jstext += "];"

with open("./techniques.js", "w") as j:
    j.write(jstext)

