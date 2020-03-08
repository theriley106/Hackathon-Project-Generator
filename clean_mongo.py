import re
from app import db, get_results
def delete_duplicates():
	all_entries = get_results(1000)
	seen_entries = set()
	for entry in all_entries:
		if entry["title"] in seen_entries or "x-raw" in entry["image_url"]:
			db.hackathon_ideas.delete_one({"_id": entry["_id"]})
		else:
			entry["title"] = entry["title"].capitalize()
			entry["title"] = re.sub(r'[^\w\s]','', entry["title"])
			db.hackathon_ideas.save(entry)
			seen_entries.add(entry["title"])
delete_duplicates()