import csv
import os

if __name__ == "__main__":
  import setWD

import helpers
from helpers import ub_logger
import ub_blient as ub

id_file = f"UB/data/{ub.WEBSIDE_NAME}_person_ids.csv"

COUNT_CONFIGS = [
    "RELATION.Person.countprojects",
    "RELATION.Person.countresearchoutputs",
    "RELATION.Person.countproducts",
    "RELATION.Person.countfundings"
]

resultFile = id_file.replace(".csv", "_to_delete.csv")

logger = ub_logger.Logger(resultFile)


logger.info(f"Start filtering {resultFile}")
with open(resultFile, 'w', newline='' , encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=["name", "link"])
    writer.writeheader()
    base_url = f"{ub.WEBSIDE}/entities/person/"

    for id in helpers.load_lines(id_file):
        contribution_count = 0
        item_response = ub.client.get_item(id, embeds=["owningCollection"])

        if (item_response.status_code != 200):
            logger.error(f"failed to get item {id} ({item_response.status_code})")
            continue

        item = item_response.json()

        try:
            if(item['metadata']['dspace.entity.type'][0]['value'] != 'Person' or  item["_embedded"]["owningCollection"]["name"] != 'Person'):
                logger.warning(f"Item {id} is not a person.")
                continue

            for config in COUNT_CONFIGS:
                url = f"{ub.WEBSIDE}/server/api/discover/search/objects?configuration={config}&scope={id}"
                res = ub.client.api_get(url).json()
                contribution_count += len(res["_embedded"]["searchResult"]["_embedded"]["objects"])
                contribution_count += res["_embedded"]["searchResult"]["page"]["totalElements"]
            print(f"Found {contribution_count} total contributions")
            if contribution_count == 0:
                writer.writerow({
                    "name": item["name"],
                    "link": f"{base_url}{id}"
                })
                # logger.error(f"Found {base_url}{id} to delete")
                continue

        except Exception as ex:
            logger.error(f"failed to get data for person {id}: \n {ex}")
