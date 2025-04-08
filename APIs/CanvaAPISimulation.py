import time
import uuid
from typing import List, Dict, Optional, Any, Union
import json

DB = {
  "Users": {
    "auDAbliZ2rQNNOsUl5OLu": {
      "user_id": "auDAbliZ2rQNNOsUl5OLu",
      "team_id": "Oi2RJILTrKk0KRhRUZozX",
      "profile": {
        "display_name": "John Doe"
      }
    }
  },
  "Designs": {
    "DAFVztcvd9z": {
      "id": "DAFVztcvd9z",
      "title": "My summer holiday",
      "design_type": {
        "type": "preset",
        "name": "doc"
      },
      "owner": {
        "user_id": "auDAbliZ2rQNNOsUl5OLu",
        "team_id": "Oi2RJILTrKk0KRhRUZozX"
      },
      "thumbnail": {
        "width": 595,
        "height": 335,
        "url": "https://document-export.canva.com/Vczz9/zF9vzVtdADc/2/thumbnail/0001.png?<query-string>"
      },
      "urls": {
        "edit_url": "https://www.canva.com/api/design/eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIiwiZXhwaXJ5IjoxNzQyMDk5NDAzMDc5fQ..GKLx2hrJa3wSSDKQ.hk3HA59qJyxehR-ejzt2DThBW0cbRdMBz7Fb5uCpwD-4o485pCf4kcXt_ypUYX0qMHVeZ131YvfwGPIhbk-C245D8c12IIJSDbZUZTS7WiCOJZQ.sNz3mPSQxsETBvl_-upMYA/edit",
        "view_url": "https://www.canva.com/api/design/eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIiwiZXhwaXJ5IjoxNzQyMDk5NDAzMDc5fQ..GKLx2hrJa3wSSDKQ.hk3HA59qJyxehR-ejzt2DThBW0cbRdMBz7Fb5uCpwD-4o485pCf4kcXt_ypUYX0qMHVeZ131YvfwGPIhbk-C245D8c12IIJSDbZUZTS7WiCOJZQ.sNz3mPSQxsETBvl_-upMYA/view"
      },
      "created_at": 1377396000,
      "updated_at": 1692928800,
      "page_count": 5,
      "pages": {
        "0": {
          "index": 0,
          "thumbnail": {
            "width": 595,
            "height": 335,
            "url": "https://document-export.canva.com/Vczz9/zF9vzVtdADc/2/thumbnail/0001.png?<query-string>"
          }
        }
      },
      "comments": {
        "threads": {
          "KeAbiEAjZEj": {
            "id": "KeAbiEAjZEj",
            "design_id": "DAFVztcvd9z",
            "thread_type": {
              "type": "comment",
              "content": {
                "plaintext": "Great work [oUnPjZ2k2yuhftbWF7873o:oBpVhLW22VrqtwKgaayRbP]!",
                "markdown": "*_Great work_* [oUnPjZ2k2yuhftbWF7873o:oBpVhLW22VrqtwKgaayRbP]!"
              },
              "mentions": {
                "oUnPjZ2k2yuhftbWF7873o:oBpVhLW22VrqtwKgaayRbP": {
                  "tag": "oUnPjZ2k2yuhftbWF7873o:oBpVhLW22VrqtwKgaayRbP",
                  "user": {
                    "user_id": "oUnPjZ2k2yuhftbWF7873o",
                    "team_id": "oBpVhLW22VrqtwKgaayRbP",
                    "display_name": "John Doe"
                  }
                }
              },
              "assignee": {
                "id": "uKakKUfI03Fg8k2gZ6OkT",
                "display_name": "John Doe"
              },
              "resolver": {
                "id": "uKakKUfI03Fg8k2gZ6OkT",
                "display_name": "John Doe"
              }
            },
            "author": {
              "id": "uKakKUfI03Fg8k2gZ6OkT",
              "display_name": "John Doe"
            },
            "created_at": 1692928800,
            "updated_at": 1692928900,
            "replies": {
              "KeAZEAjijEb": {
                "id": "KeAZEAjijEb",
                "design_id": "DAFVztcvd9z",
                "thread_id": "KeAbiEAjZEj",
                "author": {
                  "id": "uKakKUfI03Fg8k2gZ6OkT",
                  "display_name": "John Doe"
                },
                "content": {
                  "plaintext": "Great work [oUnPjZ2k2yuhftbWF7873o:oBpVhLW22VrqtwKgaayRbP]!",
                  "markdown": "*_Great work_* [oUnPjZ2k2yuhftbWF7873o:oBpVhLW22VrqtwKgaayRbP]!"
                },
                "mentions": {
                  "oUnPjZ2k2yuhftbWF7873o:oBpVhLW22VrqtwKgaayRbP": {
                    "tag": "oUnPjZ2k2yuhftbWF7873o:oBpVhLW22VrqtwKgaayRbP",
                    "user": {
                      "user_id": "oUnPjZ2k2yuhftbWF7873o",
                      "team_id": "oBpVhLW22VrqtwKgaayRbP",
                      "display_name": "John Doe"
                    }
                  }
                },
                "created_at": 1692929800,
                "updated_at": 1692929900
              }
            }
          }
        }
      }
    }
  },
  "brand_templates": {
    "DEMzWSwy3BI": {
      "id": "DEMzWSwy3BI",
      "title": "Advertisement Template",
      "design_type": {
        "type": "preset",
        "name": "doc"
      },
      "view_url": "https://www.canva.com/design/DAE35hE8FA4/view",
      "create_url": "https://www.canva.com/design/DAE35hE8FA4/remix",
      "thumbnail": {
        "width": 595,
        "height": 335,
        "url": "https://document-export.canva.com/Vczz9/zF9vzVtdADc/2/thumbnail/0001.png?<query-string>"
      },
      "created_at": 1704110400,
      "updated_at": 1719835200,
      "datasets": {
        "cute_pet_image_of_the_day": {
          "type": "image"
        },
        "cute_pet_witty_pet_says": {
          "type": "text"
        },
        "cute_pet_sales_chart": {
          "type": "chart"
        }
      }
    }
  },
  "autofill_jobs": {},
  "asset_upload_jobs": {},
  "design_export_jobs":{},
  "design_import_jobs":{},
  "url_import_jobs":{},
  "assets": {
    "Msd59349ff": {
      "type": "image",
      "id": "Msd59349ff",
      "name": "My Awesome Upload",
      "tags": [
        "image",
        "holiday",
        "best day ever"
      ],
      "created_at": 1377396000,
      "updated_at": 1692928800,
      "thumbnail": {
        "width": 595,
        "height": 335,
        "url": "https://document-export.canva.com/Vczz9/zF9vzVtdADc/2/thumbnail/0001.png?<query-string>"
      }
    },
    "Mab12345xyz": {
      "type": "image",
      "id": "Mab12345xyz",
      "name": "Sunset Over the Ocean",
      "tags": [
        "image",
        "sunset",
        "ocean",
        "nature"
      ],
      "created_at": 1704110500,
      "updated_at": 1719835300,
      "thumbnail": {
        "width": 800,
        "height": 450,
        "url": "https://document-export.canva.com/example1/thumbnail.png"
      }
    },
    "Mcd67890abc": {
      "type": "image",
      "id": "Mcd67890abc",
      "name": "Mountain Adventure",
      "tags": [
        "image",
        "mountains",
        "travel",
        "adventure"
      ],
      "created_at": 1689200000,
      "updated_at": 1699200500,
      "thumbnail": {
        "width": 1024,
        "height": 576,
        "url": "https://document-export.canva.com/example2/thumbnail.png"
      }
    }
  },
  "folders": {
    'ede108f5-30e4-4c31-b087-48f994eabeff': {
        'assets': [],
        'Designs': [],
        'folders': [],
        'folder': {
            'id': 'ede108f5-30e4-4c31-b087-48f994eabeff',
            'name': 'New Folder',
            'created_at': 1743008173,
            'updated_at': 1743008173,
            'thumbnail': {
                'width': 595,
                'height': 335,
                'url': 'https://document-export.canva.com/default-thumbnail.png'},
                'parent_id': 'root'
                }
        }
  }
}




class CanvaAPI:
    """
    The top-level class that handles the in-memory DB and provides
    save/load functionality for JSON-based state persistence.
    """

    @staticmethod
    def save_state(filepath: str) -> None:
        with open(filepath, 'w') as f:
            json.dump(DB, f)

    @staticmethod
    def load_state(filepath: str) -> None:
        global DB
        with open(filepath, 'r') as f:
            DB = json.load(f)

class Canva:
    class Users:
        @staticmethod
        def get_current_user(user_id: str)-> Dict[str, Any]:
            if user_id in DB["Users"]:
              user_id = DB["Users"][user_id]["user_id"]
              team_id = DB["Users"][user_id]["team_id"]

              return {
                  "team_user": {
                      "user_id": user_id,
                      "team_id": team_id
                  }
              }
            else:
              return {}

        def get_current_user_profile(user_id: str)-> Dict[str, Any]:
            if user_id in DB["Users"]:
              return DB["Users"][user_id]["profile"]
            else:
              return {}

    class Design:
        @staticmethod
        def create_design(design_type: dict, asset_id: str, title: str)-> Dict[str, Any]:
            design_id = str(uuid.uuid4())
            timestamp = int(time.time())

            new_design = {
                "id": design_id,
                "design_type": design_type,
                "asset_id": asset_id,
                "title": title,
                "created_at": timestamp,
                "updated_at": timestamp
            }

            DB["Designs"][design_id] = new_design

            return new_design

        @staticmethod
        def list_designs(
            query: Optional[str] = None,
            continuation: Optional[str] = None,
            ownership: str = "any",
            sort_by: str = "relevance"
        ) -> List[Dict[str, str]]:
            designs = list(DB["Designs"].values())

            # Filtering by ownership
            if ownership == "owned":
                designs = [d for d in designs if d.get("owner", {}).get("user_id")]
            elif ownership == "shared":
                designs = [d for d in designs if not d.get("owner", {}).get("user_id")]

            # Filtering by search query
            if query:
                designs = [d for d in designs if query.lower() in d["title"].lower()]

            # Sorting options
            if sort_by == "modified_descending":
                designs.sort(key=lambda x: x["updated_at"], reverse=True)
            elif sort_by == "modified_ascending":
                designs.sort(key=lambda x: x["updated_at"], reverse=False)
            elif sort_by == "title_descending":
                designs.sort(key=lambda x: x["title"], reverse=True)
            elif sort_by == "title_ascending":
                designs.sort(key=lambda x: x["title"], reverse=False)

            # return designs
            return designs if designs else None

        def get_design(design_id: str) -> Optional[Dict[str, str]]:
            design = DB["Designs"].get(design_id)
            if design:
                return {"design": design}
            return None

        @staticmethod
        def get_design_pages(design_id: str, offset: int = 1, limit: int = 50) -> Optional[Dict[str, List[Dict[str, str]]]]:
            design = DB["Designs"].get(design_id)
            if design and "pages" in design:
                pages = list(design["pages"].values())
                offset = max(1, min(offset, len(pages))) - 1  # Ensure offset is within valid range
                limit = max(1, min(limit, 200))  # Ensure limit is within allowed range
                return {"pages": pages[offset:offset + limit]}
            return None

        class Comment:
          def create_thread(design_id: str, message: str, assignee_id: Optional[str] = None) -> dict:
            """
            Adds a comment to a design in Canva.

            Parameters:
                design_id (str): REQUIRED. The design ID.
                message (str): REQUIRED. The comment message in plaintext. This is the comment body shown in the Canva UI.
                    - Mentions can be included using the format [user_id:team_id].
                    - If assignee_id is specified, the assignee must be mentioned in the message.
                assignee_id (Optional[str]): OPTIONAL. Lets you assign the comment to a Canva user using their User ID.
                    - The assigned user must be mentioned in the message.

            Returns:
                dict: A response dictionary containing the status of the comment addition, including success status and any relevant details.
            """
            pass

          def create_reply(design_id: str, thread_id: str, message: str)-> dict:
            """
            Adds a reply to an existing comment thread in Canva.

            Parameters:
                design_id (str): REQUIRED. The design ID.
                thread_id (str): REQUIRED. The ID of the thread.
                message (str): REQUIRED. The comment message of the reply in plaintext. This is the reply comment shown in the Canva UI.
                    - Mentions can be included using the format [user_id:team_id].

            Returns:
                dict: A response dictionary containing the status of the reply addition, including success status and any relevant details.
            """
            pass

          def get_thread(design_id: str, thread_id: str) -> dict:
            """
            Retrieves a specific thread from a design in Canva.

            Parameters:
                design_id (str): REQUIRED. The design ID.
                thread_id (str): REQUIRED. The ID of the thread.

            Returns:
                dict: A response dictionary containing the thread details, including success status and any relevant details.
            """
            pass

          def get_reply(design_id: str, thread_id: str, reply_id: str) -> dict:
            """
            Retrieves a specific reply from a thread in Canva.

            Parameters:
                design_id (str): REQUIRED. The design ID.
                thread_id (str): REQUIRED. The ID of the thread.
                reply_id (str): REQUIRED. The ID of the reply.

            Returns:
                dict: A response dictionary containing the reply details, including success status and any relevant details.
            """
            pass

          def list_replies(design_id: str, thread_id: str, limit: Optional[int] = 50, continuation: Optional[str] = None) -> dict:
            """
            Retrieves a list of replies for a specific thread in Canva.

            Parameters:
                design_id (str): REQUIRED. The design ID.
                thread_id (str): REQUIRED. The ID of the thread.
                limit (Optional[int]): OPTIONAL. The maximum number of replies to retrieve. min = 1, max = 100
                continuation (Optional[str]): OPTIONAL. A token for pagination.

            Returns:
                dict: A response dictionary containing the list of replies, including success status and any relevant details.
            """
            pass

          class DesignExport:
            def create_design_export_job(
              design_id: str,
              format: str,
              type: str,
              quality: Optional[Union[int, str]] = None,
              pages: Optional[List[int]] = None,
              export_quality: Optional[str] = "regular",
              size: Optional[str] = "a4",
              height: Optional[int] = None,
              width: Optional[int] = None,
              lossless: Optional[bool] = True,
              transparent_background: Optional[bool] = False,
              as_single_image: Optional[bool] = False
          ) -> dict:
              """
              Creates a design export job in Canva.

              Parameters:
                  design_id (str): REQUIRED. The design ID.
                  format (str): REQUIRED. Details about the desired export format.
                  type (str): REQUIRED. The type of export format (pdf, jpg, png, pptx, gif, mp4).
                  quality (Optional[Union[int, str]]): SOMETIMES REQUIRED. Specifies compression quality for jpg or resolution for mp4.
                  pages (Optional[List[int]]): OPTIONAL. List of page numbers to export for multi-page designs.
                  export_quality (Optional[str]): OPTIONAL. Specifies the export quality ('regular' or 'pro'). Default is 'regular'.
                  size (Optional[str]): OPTIONAL. Specifies the paper size for PDFs. Default is 'a4'.
                  height (Optional[int]): OPTIONAL. Specifies the height in pixels of the exported image (min: 40, max: 25000).
                  width (Optional[int]): OPTIONAL. Specifies the width in pixels of the exported image (min: 40, max: 25000).
                  lossless (Optional[bool]): OPTIONAL. If true, PNG is exported without compression. Default is true.
                  transparent_background (Optional[bool]): OPTIONAL. If true, exports PNG with a transparent background. Default is false.
                  as_single_image (Optional[bool]): OPTIONAL. If true, multi-page designs are merged into a single image. Default is false.

              Returns:
                  dict: A response dictionary containing the status of the export job, including success status and any relevant details.
              """
              pass

            def get_design_export_job(job_id: str) -> dict:
              """
              Retrieves the status of a design export job in Canva.

              Parameters:
                  job_id (str): REQUIRED. The ID of the export job.

              Returns:
                  dict: A response dictionary containing the status of the export job, including success status and any relevant details.
              """
              pass

          class DesignImport:
            pass
            def create_design_import(
              import_metadata: dict,
              ) -> dict:
              """
              Creates a design import job in Canva.

              Parameters:
                  import_metadata (dict): REQUIRED. Metadata about the design, included as a header parameter when importing a design.
                                          - title_base64 (str): REQUIRED. The design's title, encoded in Base64.
                                              - Maximum length (unencoded): 50 characters.
                                          - mime_type (Optional[str]): OPTIONAL. The MIME type of the file being imported.
                                              - If not provided, Canva attempts to auto-detect the file type.

              Returns:
                  dict: A response dictionary containing the status of the import job, including success status and any relevant details.
              """
              pass
            def get_design_import_job(job_id: str) -> dict:
              """
              Retrieves the status of a design import job in Canva.

              Parameters:
                  job_id (str): REQUIRED. The ID of the import job.

              Returns:
                  dict: A response dictionary containing the status of the import job, including success status and any relevant details.
              """
              pass

            def create_url_import_job(
              title: str,
              url: str,
              mime_type: Optional[str] = None
            ) -> dict:
              """
              Creates a URL import job in Canva.

              Parameters:
                  title (str): REQUIRED. A title for the design.
                      - Minimum length: 1
                      - Maximum length: 255
                  url (str): REQUIRED. The URL of the file to import.
                      - The URL must be publicly accessible.
                      - Minimum length: 1
                      - Maximum length: 2048
                  mime_type (Optional[str]): OPTIONAL. The MIME type of the file being imported.
                      - If not provided, Canva attempts to auto-detect the file type.
                      - Minimum length: 1
                      - Maximum length: 100

              Returns:
                  dict: A response dictionary containing the status of the URL import job, including success status and any relevant details.
              """
              pass

              def get_url_import_job(job_id: str) -> dict:
                """
                Retrieves the status of a URL import job in Canva.

                Parameters:
                    job_id (str): REQUIRED. The ID of the URL import job.

                Returns:
                    dict: A response dictionary containing the status of the URL import job, including success status and any relevant details.
                """
                pass




    class BrandTemplate:
        """
        A class to interact with brand templates stored in the DB.
        """

        @staticmethod
        def get_brand_template(brand_template_id: str) -> Optional[Dict[str, Any]]:
            """
            Retrieve a brand template by its ID.

            Args:
                brand_template_id (str): The ID of the brand template.

            Returns:
                Optional[Dict[str, Any]]: The brand template details if found, otherwise None.
            """
            brand_templates = DB.get("brand_templates", {})
            template = brand_templates.get(brand_template_id)

            if not template:
                return None

            return {
                "brand_template": {
                    "id": template["id"],
                    "title": template["title"],
                    "view_url": template["view_url"],
                    "create_url": template["create_url"],
                    "thumbnail": template["thumbnail"],
                    "created_at": template["created_at"],
                    "updated_at": template["updated_at"]
                }
            }

        @staticmethod
        def get_brand_template_dataset(brand_template_id: str, ) -> Optional[Dict[str, Any]]:
            """
            Retrieve a dataset from a brand template by template ID and dataset ID.

            Args:
                brand_template_id (str): The ID of the brand template.
                dataset_id (str): The ID of the dataset.

            Returns:
                Optional[Dict[str, Any]]: The dataset details if found, otherwise None.
            """
            brand_templates = DB.get("brand_templates", {})
            template = brand_templates.get(brand_template_id)

            if not template:
                return None

            datasets = template.get("datasets", {})

            if not datasets:
                return None

            return {
                "dataset": datasets
            }


        @staticmethod
        def list_brand_templates(query: Optional[str] = None,
                                continuation: Optional[str] = None,
                                ownership: Optional[str] = "any",
                                sort_by: Optional[str] = "relevance",
                                dataset: Optional[str] = "any") -> Dict[str, Any]:
            """
            List brand templates with optional filters and sorting.

            Args:
                query (Optional[str]): Search term to filter brand templates.
                continuation (Optional[str]): Token for pagination.
                ownership (str): Filter by ownership (any, owned, shared).
                sort_by (str): Sorting method (relevance, modified_descending, etc.).
                dataset (str): Filter by dataset definitions (any, non_empty, empty).

            Returns:
                Dict[str, Any]: A list of brand templates with continuation token if applicable.
            """
            brand_templates = list(DB.get("brand_templates", {}).values())

            if query:
                brand_templates = [t for t in brand_templates if query.lower() in t["title"].lower()]

            if dataset == "non_empty":
                brand_templates = [t for t in brand_templates if "datasets" in t and t["datasets"]]
            elif dataset == "empty":
                brand_templates = [t for t in brand_templates if not t.get("datasets")]

            # Sorting options
            if sort_by == "modified_descending":
                brand_templates.sort(key=lambda x: x["updated_at"], reverse=True)
            elif sort_by == "modified_ascending":
                brand_templates.sort(key=lambda x: x["updated_at"], reverse=False)
            elif sort_by == "title_descending":
                brand_templates.sort(key=lambda x: x["title"], reverse=True)
            elif sort_by == "title_ascending":
                brand_templates.sort(key=lambda x: x["title"], reverse=False)

            continuation_token = None  # Simulated continuation token logic

            return {
                "continuation": continuation_token,
                "items": [
                    {
                        "id": t["id"],
                        "title": t["title"],
                        "view_url": t["view_url"],
                        "create_url": t["create_url"],
                        "thumbnail": t["thumbnail"],
                        "created_at": t["created_at"],
                        "updated_at": t["updated_at"]
                    } for t in brand_templates
                ]
            }

    class Autofill:
        @staticmethod
        def create_autofill_job(brand_template_id: str, data: Dict[str, Any], title: Optional[str] = None) -> Dict[str, Any]:
            """
            Creates an asynchronous job to autofill a design from a brand template with input data and stores it in DB.

            :param brand_template_id: The ID of the input brand template
            :param data: The data fields and values to autofill
            :param title: Optional title for the autofilled design
            :return: The created job information
            """
            template = Canva.BrandTemplate.get_brand_template(brand_template_id)
            if not title:
                title = template.get('brand_template',{}).get('title',None)
            Canva.Design.create_design(template.get('brand_template',{}).get('design_type',{}),asset_id={},title=title)


            job_id = str(uuid.uuid4())
            job_entry = {
                    "id": job_id,
                    "status": "success",
                    "result": {
                        "type": "create_design",
                        "design": {
                            "id": brand_template_id,
                            "title": title,
                            "url": f"https://www.canva.com/design/{brand_template_id}/edit",
                            "thumbnail": DB["Designs"].get(brand_template_id, {}).get("thumbnail", {})
                        }
                    }
                }
            DB["autofill_jobs"][job_id] = job_entry
            return job_entry

        @staticmethod
        def get_autofill_job(job_id: str) -> Dict[str, Any]:
            """
            Retrieves the status and results of an autofill job from the DB.

            :param job_id: The ID of the autofill job
            :return: The job information if found, otherwise an error message
            """
            return DB["autofill_jobs"].get(job_id, {"error": "Job not found"})

    class Asset:
        @staticmethod
        def create_asset_upload_job(name: str, tags: List[str], thumbnail_url: str) -> str:
            # job_id = str(uuid.uuid4())
            # DB.setdefault("autofill_jobs", {})[job_id] = {
            #     "id": job_id,
            #     "name": name,
            #     "tags": tags,
            #     "thumbnail": {
            #         "url": thumbnail_url
            #     },
            #     "status": "pending",
            #     "created_at": int(time.time()),
            # }
            # return job_id
            pass

        @staticmethod
        def get_asset_upload_job(job_id: str) -> Optional[Dict[str, Any]]:
            return DB.get("asset_upload_jobs", {}).get(job_id)

        @staticmethod
        def get_asset(asset_id: str) -> Optional[Dict[str, Any]]:
            return DB.get("assets", {}).get(asset_id, {})

        @staticmethod
        def update_asset(asset_id: str, name: Optional[str] = None, tags: Optional[List[str]] = None) -> bool:
            if asset_id in DB.get("assets", {}):
                if name is not None and name.strip():
                    DB["assets"][asset_id]["name"] = name[:50]  # Enforce max length of 50
                if tags is not None:
                    DB["assets"][asset_id]["tags"] = tags[:50]  # Enforce max items of 50
                DB["assets"][asset_id]["updated_at"] = int(time.time())
                return True
            return False

        @staticmethod
        def delete_asset(asset_id: str) -> bool:
            if asset_id in DB.get("assets", {}):
                del DB["assets"][asset_id]
                return True
            return False

    class Folder:
        @staticmethod
        def create_folder(name: str, parent_folder_id: str) -> Dict[str, Any]:
            if not (1 <= len(name) <= 255):
                raise ValueError("Folder name must be between 1 and 255 characters.")

            if not (1 <= len(parent_folder_id) <= 50):
                raise ValueError("Parent folder ID must be between 1 and 50 characters.")

            folder_id = str(uuid.uuid4())
            timestamp = int(time.time())  # Get current timestamp

            folder_data = {
                "id": folder_id,
                "name": name,
                "created_at": timestamp,
                "updated_at": timestamp,
                "thumbnail": {
                    "width": 595,
                    "height": 335,
                    "url": "https://document-export.canva.com/default-thumbnail.png"
                },
                "parent_id": parent_folder_id
            }

            if parent_folder_id == "root":
                DB["folders"][folder_id] = {"assets": [], "Designs": [], "folders": [], "folder": folder_data}
            else:
                if parent_folder_id not in DB["folders"]:
                    raise ValueError("Parent folder ID does not exist.")

                DB["folders"][parent_folder_id]["folders"].append(folder_id)
                DB["folders"][folder_id] = {"assets": [], "Designs": [], "folders": [], "folder": folder_data}

            return folder_data

        @staticmethod
        def get_folder(folder_id: str) -> Dict[str, Any]:
            if folder_id not in DB["folders"]:
                raise ValueError("Folder ID does not exist.")

            return {"folder": DB["folders"][folder_id]["folder"]}

        @staticmethod
        def update_folder(folder_id: str, name: str) -> Dict[str, Any]:
            if folder_id not in DB["folders"]:
                raise ValueError("Folder ID does not exist.")

            if not (1 <= len(name) <= 255):
                raise ValueError("Folder name must be between 1 and 255 characters.")

            DB["folders"][folder_id]["folder"]["name"] = name
            DB["folders"][folder_id]["folder"]["updated_at"] = int(time.time())

            return {"folder": DB["folders"][folder_id]["folder"]}

        @staticmethod
        def delete_folder(folder_id: str) -> Dict[str, Any]:
            if folder_id not in DB["folders"]:
                raise ValueError("Folder ID does not exist.")

            parent_id = DB["folders"][folder_id]["folder"].get("parent_id")

            def recursive_delete(folder_id: str):
                for subfolder_id in DB["folders"][folder_id]["folders"]:
                    recursive_delete(subfolder_id)

                for asset_id in DB["folders"][folder_id]["assets"]:
                    if asset_id in DB["assets"]:
                        del DB["assets"][asset_id]

                del DB["folders"][folder_id]

            recursive_delete(folder_id)

            if parent_id and parent_id in DB["folders"]:
                DB["folders"][parent_id]["folders"].remove(folder_id)

            return {"message": "Folder and its contents deleted successfully."}

        @staticmethod
        def list_folder_items(folder_id: str, item_types: Optional[List[str]] = None, sort_by: Optional[str] = "modified_descending", continuation: Optional[str] = None) -> Dict[str, Any]:
            if folder_id not in DB["folders"]:
                raise ValueError("Folder ID does not exist.")

            folder_items = {
                "items": [],
                "continuation": None  # Placeholder for pagination if needed
            }

            items = []

            if not item_types or "folder" in item_types:
                for subfolder_id in DB["folders"][folder_id]["folders"]:
                    items.append({
                        "type": "folder",
                        "folder": DB["folders"][subfolder_id]["folder"]
                    })

            if not item_types or "design" in item_types:
                for design_id in DB["folders"][folder_id]["Designs"]:
                    items.append({
                        "type": "design",
                        "design": DB["designs"].get(design_id, {})
                    })

            if not item_types or "image" in item_types:
                for asset_id in DB["folders"][folder_id]["assets"]:
                    items.append({
                        "type": "image",
                        "image": DB["assets"].get(asset_id, {})
                    })

            sort_options = {
                "created_ascending": lambda x: x["folder"].get("created_at", 0),
                "created_descending": lambda x: -x["folder"].get("created_at", 0),
                "modified_ascending": lambda x: x["folder"].get("updated_at", 0),
                "modified_descending": lambda x: -x["folder"].get("updated_at", 0),
                "title_ascending": lambda x: x["folder"].get("name", ""),
                "title_descending": lambda x: x["folder"].get("name", ""),
            }

            if sort_by in sort_options:
                items.sort(key=sort_options[sort_by])

            folder_items["items"] = items
            return folder_items

        @staticmethod
        def move_folder_item(to_folder_id: str, item_id: str) -> Dict[str, Any]:
          pass

import unittest
import uuid
from copy import deepcopy

def setUp():
    """Reset the database before each test"""
    global DB
    global original_db
    original_db = deepcopy(DB)

def tearDown():
    """Restore the database after each test"""
    global DB
    DB = deepcopy(original_db)

def test_create_design():
    """Test creating a new design"""
    setUp()
    design = Canva.Design.create_design(
        design_type={"type": "custom", "name": "presentation"},
        asset_id="sample_asset",
        title="Test Design"
    )
    assert design["id"] in DB["Designs"]
    assert design["title"] == "Test Design"
    tearDown()

def test_list_designs():
    """Test listing designs with different filters"""
    setUp()
    designs = Canva.Design.list_designs()
    assert isinstance(designs, list)
    assert len(designs) > 0

    filtered_designs = Canva.Design.list_designs(query="summer")
    assert all("summer" in d["title"].lower() for d in filtered_designs)
    tearDown()

def test_get_design():
    """Test retrieving a specific design by ID"""
    setUp()
    design_id = list(DB["Designs"].keys())[0]
    design = Canva.Design.get_design(design_id)
    assert design is not None
    assert design["design"]["id"] == design_id
    tearDown()

def test_get_design_pages():
    """Test retrieving design pages with pagination"""
    setUp()
    design_id = list(DB["Designs"].keys())[0]
    pages = Canva.Design.get_design_pages(design_id, offset=1, limit=1)
    assert pages is not None
    assert len(pages["pages"]) == 1
    tearDown()

def test_get_brand_template():
    """Test retrieving a brand template"""
    setUp()
    template_id = list(DB["brand_templates"].keys())[0]
    template = Canva.BrandTemplate.get_brand_template(template_id)
    assert template is not None
    assert template["brand_template"]["id"] == template_id
    tearDown()

def test_get_brand_template_dataset():
    """Test retrieving dataset from a brand template"""
    setUp()
    template_id = list(DB["brand_templates"].keys())[0]
    dataset = Canva.BrandTemplate.get_brand_template_dataset(template_id)
    assert dataset is not None
    assert len(dataset["dataset"]) > 0
    tearDown()

def test_create_autofill_job():
    """Test creating an autofill job"""
    setUp()
    template_id = list(DB["brand_templates"].keys())[0]
    data = {"cute_pet_image_of_the_day": "https://example.com/image.jpg"}
    job = Canva.Autofill.create_autofill_job(template_id, data, title="Autofilled Design")
    assert job["id"] in DB["autofill_jobs"]
    assert job["status"] == "success"
    tearDown()

def test_get_autofill_job():
    """Test retrieving an autofill job"""
    setUp()
    template_id = list(DB["brand_templates"].keys())[0]
    data = {"cute_pet_image_of_the_day": "https://example.com/image.jpg"}
    job = Canva.Autofill.create_autofill_job(template_id, data, title="Autofilled Design")
    job_id = job["id"]
    retrieved_job = Canva.Autofill.get_autofill_job(job_id)
    assert retrieved_job is not None
    assert retrieved_job["id"] == job_id
    tearDown()

if __name__ == "__main__":
    test_create_design()
    test_list_designs()
    test_get_design()
    test_get_design_pages()
    test_get_brand_template()
    test_get_brand_template_dataset()
    test_create_autofill_job()
    test_get_autofill_job()
    print("All tests passed.")
