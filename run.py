from dspace_rest_client.models import SimpleDSpaceObject , Bundle

from ub_blient import *
import os

FILE_PATH = "data.txt"
FILE_DIR = "files"

accessTypes = {"public": "openaccess", "validuser": "validuser"}

licenseTypes = {"cc_by": "https://creativecommons.org/licenses/by/4.0/",
                "cc_by_nc": "https://creativecommons.org/licenses/by-nc/4.0/",
                "cc_by_nc_nd": "https://creativecommons.org/licenses/by-nc-nd/4.0",
                "cc_by_sa": "https://creativecommons.org/licenses/by-sa/4.0",
                "cc_by_nc_sa": "https://creativecommons.org/licenses/by-nc-sa/4.0",
                "publisher": "publisher",
                "boris": "https://www.ub.unibe.ch/services/open_science/boris_publications/index_eng.html#collapse_pane631832"
                }

contentTypes = {"draft": "draft",
                "updated": "updated",
                "coverimage": "coverimage",
                "presentation": "presentation",
                "published": "published",
                "submitted": "submitted",
                "supplemental": "supplemental",
                "other": "other",
                "accepted": "accepted",
                "": "published"
                }


def create_bitstream(publication_uuid, name, file_path, accesValue, licenseValue, contentType):
    client.authenticate()

    publication_response = client.get_item(publication_uuid)

    if publication_response.status_code != 200:
        print(f"ERROR: Could not find publication , id: {publication_response}")
        return



    files = getFiles(publication_uuid)

    if files is None:
        print(f"ERROR: Could not read files, id: {publication_uuid}")
        return

    file_names = [file['metadata']['dc.title'][0]["value"] for file in files]

    if (name in file_names):
        print(F"SKIPPING: {name} already exists")
        ## uncomment line below if you want to skip files that already exist
        return

    file_index = len(file_names)  # we will add one item so we do not need to decrease by 1

    dso = SimpleDSpaceObject(publication_response.json())

    bundle_link = dso.links["bundles"]["href"]
    bundle_data = client.api_get(bundle_link)

    bundles = bundle_data.json()['_embedded']['bundles']

    if len(bundles) == 0:
        print(f"ERROR: {publication_uuid} ,Could not find bundle with id: {bundle_link}")
        return

    original_bundle = bundles[0]

    bundle = Bundle(original_bundle)

    mime = "application/octet-stream"
    metadata = {
        "dc.rights": [{"value": "This work is licensed under CC BY 4.0"}],
        "dc.rights.uri": [{"value": licenseValue}],
        "unibe.content": [{"value": contentType}],
    }

    bitstream = client.create_bitstream(bundle,
                                        name,
                                        file_path,
                                        mime,
                                        metadata)

    if bitstream is None:
        print(f"ERROR: {publication_uuid} Could not create bitstream, id: {bitstream}")
        return

    r = setAcces(publication_uuid, file_index, accesValue)
    if (r.status_code == 200):
        print(f"SUCCESS: {publication_uuid}, created File {name}, access: {accesValue}")


with open(FILE_PATH, "r", encoding="utf-8") as f:
    for line in f:
        # Skip empty lines
        if not line.strip():
            continue

        parts = [part.strip() for part in line.strip().split("|")]

        row = {
            "id": int(parts[0]),
            "group": parts[1],
            "uuid": parts[2],
            "licenceIdentifier": parts[3],
            "content": parts[4]
        }
        file_dir = f"{FILE_DIR}/{parts[2]}"

        if os.path.isdir(file_dir):
            filenames = os.listdir(file_dir)
            for name in filenames:
                full_path = os.path.join(file_dir, name)
                create_bitstream(row["uuid"], name, full_path,
                                 accessTypes[row["group"]],
                                 licenseTypes[row["licenceIdentifier"]],
                                 contentTypes[row["content"]]
                                 )
