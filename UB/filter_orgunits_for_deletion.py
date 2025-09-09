import csv
import os

if __name__ == "__main__":
    import setWD

import helpers
from helpers import ub_logger
import ub_blient as ub

id_file = "UB/data/boris4.test_orgunit_ids_20250908_1018.csv"

COUNT_CONFIGS = [
    "RELATION.OrgUnit.rppublications",
    "RELATION.OrgUnit.people",
    "RELATION.OrgUnit.suboupeople",
    "RELATION.OrgUnit.subouprojects",
    "RELATION.OrgUnit.suboupublications",
    "RELATION.OrgUnit.organizations",
    "RELATION.OrgUnit.projects",
    "RELATION.OrgUnit.researchdata",
    "RELATION.OrgUnit.researchdatasearch"
]

resultFile = id_file.replace(".csv", "_to_delete.csv")

logger = ub_logger.Logger(resultFile)

logger.info(f"Start filtering {resultFile}")

with open(resultFile, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=["name", "link"])
    writer.writeheader()

    base_url = f"{ub.WEBSIDE}/entities/orgunit/"

    for id in helpers.load_lines(id_file):
        total = 0
        item_response = ub.client.get_item(id, embeds=["owningCollection"])
        if (item_response.status_code != 200):
            logger.error(f"failed to get item {id} ({item_response.status_code})")
            continue

        item = item_response.json()

        try:
            if (item['metadata']['dspace.entity.type'][0]['value'] != 'OrgUnit' or
                    item["_embedded"]["owningCollection"]["name"] != 'OrgUnit'):
                logger.warning(f"Item {id} is not an OrgUnit.")
                continue

            for config in COUNT_CONFIGS:
                url = f"{ub.WEBSIDE}/server/api/discover/search/objects?configuration={config}&scope={id}"
                res = ub.client.api_get(url).json()
                total += len(res["_embedded"]["searchResult"]["_embedded"]["objects"])
                total += res["_embedded"]["searchResult"]["page"]["totalElements"]

            if total == 0:
                print("hallo")
                writer.writerow({
                    "name": item["name"],
                    "link": f"{base_url}{id}"
                })

        except Exception as ex:
            logger.error(f"failed to get item {id}: \n {ex}")
