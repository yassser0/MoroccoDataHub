
from discovery.collector import discover_opendata, discover_hcp

print("Testing Morocco Open Data...")
opendata = discover_opendata()
print(f"Datasets found: {len(opendata)}")

for dataset in opendata[:3]:
    print("-", dataset["title"])

print("\nTesting HCP...")
hcp = discover_hcp()
print(f"Resources found: {len(hcp)}")

for dataset in hcp[:3]:
    print("-", dataset["title"])
