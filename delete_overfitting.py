import re
from app import db, get_results



def delete_overfitting():
	generated_taglines = {x.strip() for x in open('ideas2.txt').readlines()}

	all_entries = get_results(1000)
	for entry in all_entries:
		if entry["tagline"] not in generated_taglines:
			db.hackathon_ideas.delete_one({"_id": entry["_id"]})
			
delete_overfitting()