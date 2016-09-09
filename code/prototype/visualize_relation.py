from prototype.lib import sample_repo
from py import paths
from py import wikidata

relation = "P206"

client = wikidata.WikidataClient()
samples = sample_repo.load_samples(relation)

html = "<h1>" + relation + ": " + client.get_name(relation) + "</h1>"

for sample in samples:
    html += "<li>" + sample['subject'] + " " + sample['object'] + " " + sample['sentence']

print(html)
