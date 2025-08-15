import csv
import ub_logger

logger = ub_logger.Logger()

name_to_remove = "license.txt"

if __name__ == "__main__":
  import setWD


import ub_blient as ub

def getDirtyBitstreamFromProjectId(project_id):
    bundles = list(ub.client.get_bundles(parent=type("Item", (), {"uuid": project_id})()))

    bitstreams = []
    for b in bundles:
        bs = list(ub.client.get_bitstreams(bundle=b))
        for bitstream in bs:
            if bitstream.name == name_to_remove:
                bitstreams.append(bitstream.id)

    if(len(bitstreams) == 1):
        return [{"bs_id": bitstreams[0] , "project_id": project_id }]
    return bitstreams



logger.info(f"Loading Projects")
### Get All publication ids
size = 10
page = 0
pub_ids = []
for i in range(round(10000/size)):
    publications = ub.client.api_get(f"{ub.WEBSIDE}/server/api/discover/search/objects?configuration=project&size={size}&page={i}")
    objects = publications.json()["_embedded"]["searchResult"]["_embedded"]["objects"]
    newIds = [ obj["_embedded"]["indexableObject"]["id"] for obj in objects]
    if(len(newIds) == 0):
        break
    pub_ids += newIds


logger.info(f"Found {len(pub_ids)} Projects")


## Get all dirty bitstreams
logger.info(f"Loading bitstreams with name {name_to_remove}")

dirtyBitsStreams = []
for id in pub_ids:
    dbs = getDirtyBitstreamFromProjectId(id)
    if(len(dbs) > 0):
        logger.info(f"{dbs[0]}")
    dirtyBitsStreams += dbs

logger.info(f"Found {len(dirtyBitsStreams)} bitstreams to remove")


logger.info(f" \n \n ----------------Removing Bitstream---------------- \n")

for dbs in dirtyBitsStreams:
    bs_id = dbs["bs_id"]
    r = ub.deleteBitstream(bs_id)
    logger.info( f"{r.status_code} bitstream {bs_id} project {dbs["project_id"]}")