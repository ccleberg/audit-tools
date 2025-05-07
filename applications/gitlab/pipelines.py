"""
Review CI/CD pipelines and their configurations for a specific GitLab project.
"""

import requests

BASE_URL = "https://gitlab.com/api/v4"
PRIVATE_TOKEN = "your_access_token"
PROJECT_ID = "project_id"
TIMEOUT = 30

HEADERS = {"PRIVATE-TOKEN": PRIVATE_TOKEN}

if __name__ == "__main__":
    page = 1
    per_page = 100

    while True:
        response = requests.get(
            f"{BASE_URL}/projects/{PROJECT_ID}/pipelines",
            headers=HEADERS,
            params={"page": page, "per_page": per_page},
            timeout=TIMEOUT,
        )
        if response.status_code == 200:
            pipelines = response.json()
            if not pipelines:
                break

            for pipeline in pipelines:
                pipeline_id = pipeline["id"]
                status = pipeline["status"]
                ref = pipeline["ref"]
                created_at = pipeline["created_at"]
                duration = pipeline.get("duration", "N/A")

                print(f"Pipeline ID: {pipeline_id}")
                print(f"  Status: {status}")
                print(f"  Ref: {ref}")
                print(f"  Created At: {created_at}")
                print(f"  Duration: {duration} seconds")

                detail_response = requests.get(
                    f"{BASE_URL}/projects/{PROJECT_ID}/pipelines/{pipeline_id}",
                    headers=HEADERS,
                    timeout=TIMEOUT,
                )
                if detail_response.status_code == 200:
                    pipeline_details = detail_response.json()
                    print(f"  Configuration: {pipeline_details.get('config', 'N/A')}")
                else:
                    print(
                        f"  Failed to fetch pipeline details: {detail_response.status_code}, {detail_response.text}"
                    )

            page += 1
        else:
            print(f"Failed to fetch pipelines: {response.status_code}, {response.text}")
            break
