"""Data collection module for MoroccoDataHub."""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

HEADERS = {
    "User-Agent": "MoroccoDataHub/0.1 (Data discovery project)"
}

# -----------------------------------
# 1. Morocco Open Data - CKAN API
# -----------------------------------

def discover_opendata():
    print("\nCollecting datasets from data.gov.ma...")

    url = "https://www.data.gov.ma/data/api/3/action/package_search"

    response = requests.get(
        url,
        params={"q": "*:*", "rows": 10},
        headers=HEADERS,
        timeout=30
    )

    response.raise_for_status()

    payload = response.json()

    if not payload.get("success"):
        raise RuntimeError("CKAN API returned an error")

    datasets = []

    for item in payload["result"]["results"]:
        dataset = {
            "id": item.get("id"),
            "name": item.get("name"),
            "title": item.get("title"),
            "description": item.get("notes"),
            "source": "data.gov.ma",
            "source_url": item.get("url"),
            "license": item.get("license_title"),
            "modified": item.get("metadata_modified"),
            "resources": []
        }

        for resource in item.get("resources", []):
            dataset["resources"].append({
                "name": resource.get("name"),
                "format": resource.get("format"),
                "url": resource.get("url")
            })

        datasets.append(dataset)

    return datasets


# -----------------------------------
# 2. Haut-Commissariat au Plan (HCP)
# -----------------------------------

def discover_hcp():
    print("\nCollecting resources from HCP...")

    url = "https://www.hcp.ma/downloads/RGPH-2024_t22752.html"

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=30
    )

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    datasets = []

    for link in soup.find_all("a", href=True):
        href = link["href"]
        absolute_url = urljoin(url, href)

        if absolute_url.lower().split("?")[0].endswith(
            (".xlsx", ".xls", ".csv", ".pdf")
        ):
            dataset = {
                "title": link.get_text(" ", strip=True),
                "description": "Resource published on the HCP RGPH 2024 page.",
                "source": "HCP",
                "source_url": url,
                "license": None,
                "modified": None,
                "resources": [
                    {
                        "name": link.get_text(" ", strip=True),
                        "format": absolute_url.split("?")[0].split(".")[-1],
                        "url": absolute_url
                    }
                ]
            }

            datasets.append(dataset)

    return datasets
