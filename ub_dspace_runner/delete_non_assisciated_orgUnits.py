import csv
import ub_logger

logger = ub_logger.Logger()

if __name__ == "__main__":
  import setWD

import ub_blient as ub

logger.info(f"Loading Projects")

### Get All Researcher ids
size = 20
page = 0
pub_ids = []
for i in range(round(20/size)):
    url = f"{ub.WEBSIDE}/server/api/discover/search/objects?size={size}&page={i}&configuration=person"

    publications = ub.client.api_get(url)
    print(publications)
    objects = publications.json()["_embedded"]["searchResult"]["_embedded"]["objects"]
    newIds = [ obj["_embedded"]["indexableObject"]["id"] for obj in objects]

    print(f"Found {len(newIds)} new IDs")
    if(len(newIds) == 0):
        break
    pub_ids += newIds


COUNT_CONFIGS = [
    "RELATION.Person.countprojects",
    "RELATION.Person.countresearchoutputs",
    "RELATION.Person.countproducts",
    "RELATION.Person.countfundings"
]

persons_id_with = []
person_ids_without = []
not_a_person = []

for id in pub_ids:
    total = 0
    item = ub.client.get_item(id, embeds=["owningCollection" , "configuration"]).json()
    if(item['metadata']['dspace.entity.type'][0]['value'] != 'Person' or  item["_embedded"]["owningCollection"]["name"] != 'Person'):
        not_a_person += [id]
        continue

    for config in COUNT_CONFIGS:
        url = f"{ub.WEBSIDE}/server/api/discover/search/objects?configuration={config}&scope={id}"
        res = ub.client.api_get(url).json()
        total += len(res["_embedded"]["searchResult"]["_embedded"][ "objects" ])
        total += res["_embedded"]["searchResult"]["page"]["totalElements"]
    print(f"Found {total} total IDs")
    if total == 0:
        person_ids_without += [id]
        continue
    persons_id_with += [id]


print(len(persons_id_with))
print(len(person_ids_without))
print(len(not_a_person))
