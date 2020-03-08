import requests
import json
from app import save_real_fake_idea, generate_image_url, db

def build_name_and_image(tagline):
    converted_tagline = "+".join(tagline.split()[:6])
    data = {
        "keywords": converted_tagline,
        "styles%5B%5D": "brandable",
        "lengths%5B%5D": "medium",
        "extensions%5B%5D": "com",
        "require_domains": "false",
        "premium_index": "0",
        "num": "2"
    }
    namelix_response = requests.post("https://namelix.com/app/load2.php",
                                    data = data)
    data = json.loads(namelix_response.text)
    gen_name = data[0]["title"][:-4]
    gen_name = gen_name.capitalize()
    gen_img = data[0]["logo"]
    return gen_name, gen_img

query_result = db.hackathon_ideas.find()
seen_taglines = set()
for idea in query_result:
    seen_taglines.add(idea["tagline"])
# print(("A community-driven platform for food waste management at your fingertips." not in seen_taglines))

with open('ideas.txt') as f:
    for i, tagline in enumerate(f.readlines()):
        tagline = tagline.rstrip()
        if not (tagline in seen_taglines):
            print(tagline)
            title, url = None, None
            try:
                title, url = build_name_and_image(tagline)
            except:
                # get a different title
                title = max(tagline.split(), key = lambda x : len(x))
                # get a different url
                url = generate_image_url(title, tagline)
            save_real_fake_idea(title, tagline, url)
