import csv

ideas = set()
training = set()

with open("web_scraping.csv", encoding="utf-8") as f:
    csv_reader = csv.reader(f.readlines())
    for row in csv_reader:
        training.add(row[1])

with open("ideas.txt", encoding="utf-8") as f:
    for tagline in f.readlines():
        tagline = tagline.strip()
        ideas.add(tagline)

with open("ideas2.txt", "w", encoding="utf-8") as f: 
    for idea in ideas - training:
        f.write(idea + "\n")