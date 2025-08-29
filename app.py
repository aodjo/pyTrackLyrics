import xmltodict
import json
from bs4 import BeautifulSoup

with open("data.xml", "r", encoding="utf-8") as f:
    xml_data = f.read()

soup = BeautifulSoup(xml_data, "xml") 

data_dict = xmltodict.parse(soup.prettify())
json_data = json.dumps(data_dict, indent=4, ensure_ascii=False)

with open("parsed.json", "w", encoding="utf-8") as f:
    f.write(json_data)
    f.close()

# print(json_d/ata)
