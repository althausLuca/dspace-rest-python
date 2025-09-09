from dspace_rest_client.models import SimpleDSpaceObject, Bundle

from ub_blient import *
import os

"""
 Use code from: https://github.com/the-library-code/dspace-rest-python.git
 
 
 
.txt file with | seperated values NO HEADER

Format:
  eprint-id (not used) |  group  | dspace-object-id | filename | licenceIdentifier | content
  
Example:
  
  10218 | validuser | df1ebfba-be7c-4a1e-8e9e-56e2a3324e67 | 10218.pdf | publisher| accepted
"""
FILE_PATH = "data.txt"

## Relative path to the files
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

    file_names = getFiles(publication_uuid)

    if file_names is None:
        print(f"ERROR: Could not read files, id: {publication_uuid}")
        return

    if (name in file_names):
        print(F"SKIPPING: {publication_uuid}, File {name} already exists")
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
    else:
        print(f"ERROR: {publication_uuid} , set access value access value {accesValue} for file {name}")


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
            "name": parts[3],
            "licenceIdentifier": parts[4],
            "content": parts[5]
        }

        name = parts[3]
        file_dir = f"{FILE_DIR}/{parts[2]}"
        full_path = os.path.join(file_dir, name)

        if not os.path.exists(full_path):
            print(f"ERROR: {parts[2]} File not found at {full_path}")
            continue

        create_bitstream(row["uuid"], name, full_path,
                         accessTypes[row["group"]],
                         licenseTypes[row["licenceIdentifier"]],
                         contentTypes[row["content"]]
                         )

        # if os.path.isdir(file_dir):
        #     filenames = os.listdir(file_dir)
        #     for name in filenames:
        #         full_path = os.path.join(file_dir, name)
        #         create_bitstream(row["uuid"], name, full_path,
        #                          accessTypes[row["group"]],
        #                          licenseTypes[row["licenceIdentifier"]],
        #                          contentTypes[row["content"]]
        #                          )
