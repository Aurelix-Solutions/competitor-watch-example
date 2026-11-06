# PUBLISH AFTER: competitor-watch is public on the Apify Store
import csv
import json
import os

from apify_client import ApifyClient

ACTOR_ID = "aurelix/competitor-watch"

RUN_INPUT = {'competitors': ['allbirds.com', 'glossier.com'], 'sources': ['meta_ads', 'website', 'shopify'], 'stateKey': 'my-competitors'}

PRINT_FIELDS = ['record_type', 'competitor', 'source', 'change', 'summary']


def flat(value):
    if isinstance(value, (list, dict)):
        return json.dumps(value, ensure_ascii=False)
    return value


def main():
    client = ApifyClient(os.environ["APIFY_TOKEN"])
    run = client.actor(ACTOR_ID).call(run_input=RUN_INPUT)
    items = list(client.dataset(run["defaultDatasetId"]).iterate_items())

    print(f"Run {run['status']}: {len(items)} items")
    if run.get("statusMessage"):
        print(run["statusMessage"])
    for item in items[:5]:
        print(" | ".join(str(item.get(f)) for f in PRINT_FIELDS))

    columns = []
    for item in items:
        columns += [k for k in item if k not in columns]
    with open("results.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        for item in items:
            writer.writerow({k: flat(v) for k, v in item.items()})
    print(f"Wrote results.csv ({len(items)} rows, {len(columns)} columns)")


if __name__ == "__main__":
    main()
