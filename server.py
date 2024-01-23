from flask import Flask, render_template, request
from konlpy.tag import Okt
import json

okt = Okt()

def extract_nouns(text):
    nouns = okt.nouns(text)
    return nouns

app = Flask(__name__)

with open("data.json", "r", encoding="utf-8") as json_file:
    data = json.load(json_file)

with open("find_data.json", "r", encoding="utf-8") as find:
    find_data = json.load(find)

@app.route("/")
def main():
    return render_template("main.html")

@app.route("/search")
def search():
    search_query = request.args.get('q', '')

    nouns = extract_nouns(search_query)

    final_data_list = []

    for noun in nouns:
        if noun in data:
            final_data_list += data[noun]
            if noun in find_data:
                find_data[noun] += 1
            else:
                find_data[noun] = 1

    unique_tuples = set(tuple(d.items()) for d in final_data_list)

    unique_list = [dict(t) for t in unique_tuples]

    sorted_unique_list = sorted(unique_list, key=lambda x: final_data_list.count(x), reverse=True)

    final_data_list = sorted_unique_list

    with open("find_data.json", "w", encoding="utf-8") as json_data:
        json.dump(find_data, json_data, ensure_ascii=False, indent=2)

    return render_template("search.html", search_results=final_data_list)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
