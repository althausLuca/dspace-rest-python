import os
from datetime import datetime
if __name__ == "__main__":
  import setWD

import ub_blient as ub

# person , orgunit
configuration = "person"


pub_ids_file = f"UB/data/{ub.WEBSIDE_NAME}_{configuration}_ids.csv"

os.makedirs("data", exist_ok=True)

size = 20
page = 0
pub_ids = []
for i in range(round(2000000/size)):

    url = f"{ub.WEBSIDE}/server/api/discover/search/objects?size={size}&page={i}&configuration={configuration}"
    publications = ub.client.api_get(url)
    objects = publications.json()["_embedded"]["searchResult"]["_embedded"]["objects"]
    newIds = [obj["_embedded"]["indexableObject"]["id"] for obj in objects]

    print(f"found {len(newIds)} new ids")

    if(len(newIds) == 0):
        break
    pub_ids += newIds
    with open(pub_ids_file, "a") as f:  # append mode
        for new_id in newIds:
            f.write(new_id + "\n")