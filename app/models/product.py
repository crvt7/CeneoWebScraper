from os import stat
from app.models.opinion import Opinion
import requests
import json
from bs4 import BeautifulSoup

class Product:
    def __init__(self, product_id, product_name = None, opinions = []):
        self.product_id = product_id
        self.product_name = product_name
        self.opinions = opinions.copy()
    
    def extract_product(self):
        next_page = "https://www.ceneo.pl/{}#tab=reviews".format(self.product_id)
        while next_page:
            respons = requests.get(next_page)
            page_dom = BeautifulSoup(respons.text, "html.parser")

            if self.product_name == None:
                try:
                    self.product_name = page_dom.find("h1", class_="product-top__product-info__name js_product-h1-link js_product-force-scroll js_searchInGoogleTooltip default-cursor").text[1:]
                except AttributeError:
                    try:
                        self.product_name = page_dom.find("h1", class_="product-top__product-info__name long-name js_product-h1-link js_product-force-scroll js_searchInGoogleTooltip default-cursor").text[1:]
                    except AttributeError:
                        self.product_name = "empty_product_name"
                    
            opinions = page_dom.select("div.js_product-review")
            for opinion in opinions:
                self.opinions.append(Opinion().extract_opinion(opinion).transform_opinion())
            try:
                next_page = "https://www.ceneo.pl" + \
                    page_dom.select("a.pagination__next").pop()["href"]
            except IndexError:
                next_page = None
            print(next_page)

    def __str__(self):
        return f"product_id: {self.product_id}<br>product_name: {self.product_name}<br>opinions:<br>" + "<br><br>".join(str(opinion) for opinion in self.opinions)

    def __repr__(self):
        return f"Product(product_id={self.product_id}, product_name={self.product_name}, opinions=[" + ", ".join(opinion.__repr__() for opinion in self.opinions) + "])"

    def to_dict(self):
        return {
            "product_id": self.product_id,
            "product_name": self.product_name,
            "opinions": [opinion.to_dict() for opinion in self.opinions]
        }

    def save_to_json(self):
        with open(f"app/products/{self.product_id}.json", "w", encoding="UTF-8") as fp:
            json.dump(self.to_dict(), fp, indent=4, ensure_ascii=False)
        fp.close()
    
    def create_json_stats(self):
        json_data = {}
        stats = {"id": "N/A", "name" : "N/A", "opinion_count" : 0, "pros_count" : 0, "cons_count" : 0, "avg_score": "Brak ocen"}
        score = 0

        with open(f"app/products/{self.product_id}.json", "r", encoding="UTF-8") as fp:
            json_data = json.load(fp)

        stats["id"] = json_data['product_id']
        stats["name"] = json_data["product_name"]
        for opinion in json_data["opinions"]:
            stats["opinion_count"] += 1
            stats["pros_count"] += len(opinion["pros"])
            stats["cons_count"] += len(opinion["cons"])
            score += opinion["stars"]
        if stats["opinion_count"] > 0:
            stats["avg_score"] = round((score / stats["opinion_count"]), 2)

        with open(f"app/stats/{self.product_id}_stats.json", "w", encoding="UTF-8") as file:
            json.dump(stats, file)

    def read_from_json(self):
        print(self.product_id)
        with open(f"app/products/{self.product_id}.json", "r", encoding="UTF-8") as fp:
            prod = json.load(fp)
        fp.close()
        self.product_name = prod['product_name']
        opinions = prod['opinions']
        for opinion in opinions:
            self.opinions.append(Opinion(**opinion))