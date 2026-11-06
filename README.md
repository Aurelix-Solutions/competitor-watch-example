<!-- PUBLISH AFTER: competitor-watch is public on the Apify Store -->
# Competitor Watch: Python example

A small, runnable example for **[Competitor Watch](https://apify.com/aurelix/competitor-watch)**, an Apify Actor by Aurelix.

## What it does

Competitor Watch takes a list of competitors (domains such as `allbirds.com`, or brand names) and, on each run, returns only what is new for each one since the previous run with the same state key:

- new ads in the Meta Ad Library (Facebook and Instagram);
- new ads in the TikTok Ad Library (EU/EEA, UK, Switzerland and Turkey);
- text changes on the pages you choose, with prices that appeared or disappeared;
- new products and price changes in the competitor's Shopify store;
- new postings on its public job board (optional).

Each competitor gets one `competitor_report` row with a plain-language summary, plus one `change` row per new item. The first run saves a baseline; later runs report only changes.

This repository holds a short Python script that starts the Actor, prints a few fields and saves every row to `results.csv`. The monitoring itself runs on Apify; this code only calls it.

## Why this over alternatives

- One run and one report per competitor instead of five separate scrapers, schedules and output formats.
- Only what is new: nothing already reported is returned or charged again.
- $0.03 per competitor per run ($0.027 on paid Apify plans) plus $0.001 per new item; no per-item charge on the baseline run.

## When to use it

- Agencies sending each client a weekly competitor digest
- E-commerce brands watching rivals' launches, price cuts and home-page sales
- Performance marketers keeping a swipe file of competitors' new ads
- Product marketing teams tracking competitors' pricing pages

## Input used in this example

```json
{
  "competitors": ["allbirds.com", "glossier.com"],
  "sources": ["meta_ads", "website", "shopify"],
  "stateKey": "my-competitors"
}
```

Every field is described on the [Actor's page](https://apify.com/aurelix/competitor-watch) under Input. Change `RUN_INPUT` in `main.py` to watch your own competitors; keep the same `stateKey` between runs.

## How to run

You need Python 3.10 or newer and an Apify account. Copy your API token from **Apify Console > Settings > API & Integrations**.

```bash
pip install -r requirements.txt
export APIFY_TOKEN=your_token_here
python main.py
```

The first run prints one report per competitor ("First check of Allbirds: now tracking ..."). Run it again later with the same state key and you get only the new ads, page changes, products and price changes.

## Sample output

One report from a real run (lists shortened):

```json
{
  "record_type": "competitor_report",
  "competitor": "Glossier",
  "domain": "glossier.com",
  "status": "ok",
  "baseline": false,
  "summary": "Glossier: nothing new since the last check.",
  "new_items_total": 0,
  "new_meta_ads": 0,
  "pages_changed": 0,
  "new_products": 0,
  "price_changes": 0,
  "tracking": {
    "meta_page_name": "Glossier",
    "meta_active_ads": 235,
    "meta_ads_seen": 29,
    "pages_watched": 1,
    "products_tracked": 116,
    "store_currency": "USD"
  }
}
```

## Export to CSV, Google Sheets, Slack and n8n

**CSV.** `main.py` writes `results.csv`, or download any run's results from Apify Console (Storage > Datasets > Export).

**Slack.** Put a Slack incoming-webhook URL in `slackWebhookUrl`: after each run that found something new, the channel gets one line per competitor.

**Email.** Put a Zapier, Make or n8n webhook in `webhookUrl` and send the `text` field as an email from there.

**n8n.** Use the Apify node ("Run an Actor" with actor `aurelix/competitor-watch`), schedule it with a Schedule Trigger node and keep the same `stateKey`.

## Limits

Stated as on the Actor's page:

- Meta ads are the brand page's active ads, newest first, 30 per run by default.
- TikTok's public Ad Library covers only the EU/EEA, the UK, Switzerland and Turkey.
- Website changes are text changes; pages that need JavaScript are reported, not compared.
- Shopify stores only, up to 5,000 products per store and run.
- No Google ads, news, traffic or keyword data.

## Pricing

At the time of writing (check the [Actor's page](https://apify.com/aurelix/competitor-watch) for current prices): $0.03 per competitor checked per run on Apify's free plan ($0.027 on paid plans), $0.001 per new item, plus a $0.015 start fee per run at the default 1 GB of memory.

Running `main.py` starts a real, billed Actor run on your Apify account.

## Links

- Actor on the Apify Store: https://apify.com/aurelix/competitor-watch
- All Aurelix tools: https://apify.com/aurelix
- Questions, bugs and feature requests: the Issues tab on the Actor's Store page

## Licence

The example code in this repository is released under the MIT licence (see `LICENSE`). The Actor itself is a separate service on the Apify Store and is not covered by this licence.
