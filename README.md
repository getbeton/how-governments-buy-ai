# How governments buy AI: the notebook

Rerun the Sell to State study [How governments buy AI](https://www.selltostate.com/blog/how-governments-buy-ai/) on live public procurement data, through the [Sell to State API](https://www.selltostate.com/api/).

The study read 16,184 public procurements for artificial intelligence in 59 countries, January 2024 to September 2026. This repository contains the rules of that study (keyword families in 25 languages, the taxonomy of what is bought, what the AI does and who it serves) and a notebook that applies them to the current Sell to State data.

## What you get

- AI tenders per 10,000 records, by country and year, and the median country of each region
- What governments buy (courses, licences, consulting, compute...), what the AI does (generative AI, computer vision, chatbots...), the use case and the users
- The AI brands that tenders name (ChatGPT, Copilot, Claude, Gemini, Nvidia...)
- Prices in US dollars: percentiles by region, country and purchase type
- The AI tenders that are open now, with a link to each one
- CSV files of every table in `data/`

## Get access

The notebook calls the [Sell to State API](https://www.selltostate.com/api/). Use one of these:

- **API key.** Sign in at [app.selltostate.com](https://app.selltostate.com), open Settings > API, and set `STS_API_KEY`.
- **Agent signup.** No account and no browser login:
  1. `POST https://app.selltostate.com/api/oidc/register` with `{"client_name": "my agent"}`. The answer has `client_id` and `payment_link`.
  2. Pay on `payment_link` ($49 a month, [current price](https://app.selltostate.com/api/v1/price)). An agent can also `POST` a Stripe payment method token to `/api/v1/pay` with `Authorization: Bearer client:<client_id>`.
  3. Check `GET /api/v1/whoami` with `Authorization: Bearer client:<client_id>`: `"active": true`.
  4. Set `STS_CLIENT_ID=<client_id>`. Keep it private: the client id is the credential.

  `aig.client.register()` does step 1, and the first notebook cell walks you through steps 1 to 4.

## Run it

```bash
git clone https://github.com/getbeton/how-governments-buy-ai.git
cd how-governments-buy-ai
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export STS_API_KEY=your-key        # or STS_CLIENT_ID=your-client-id
jupyter notebook notebook.ipynb
```

A full run on all countries makes about 6,500 API calls and takes about 25 minutes. For a quick run, set `AIG_COUNTRIES=united-kingdom,poland` before you start Jupyter. Results are saved in `data/`; a rerun continues where it stopped.

## How the results differ from the article

- **Titles only.** The article read the full text of each notice from the original sources. The API searches titles, buyer names and supplier names. So the notebook counts AI that a title names. In the article, that was 55% of all AI procurements.
- **Other coverage.** Sell to State covers 65 countries, with its own sources and years. Its coverage grew in 2026, so compare a country with itself inside one year first.
- **The same rules.** `aig/families.py` (what counts as AI and which false matches are removed), `aig/taxonomy3.py` and `aig/taxonomy4.py` (labels) and `aig/buyers.py` (government level and branch) are the study's rules, unchanged.

## Files

| File | What it does |
|---|---|
| `notebook.ipynb` | The study, step by step |
| `aig/client.py` | Sell to State API client (API key or agent client, agent signup, rate limit, retries, paging) |
| `aig/terms.py` | Search terms per language |
| `aig/families.py` | AI keyword families in 25 languages, with the checks that remove false matches |
| `aig/taxonomy3.py`, `aig/taxonomy4.py` | What the tender buys, what the AI does, use cases, users, brands |
| `aig/buyers.py`, `aig/taxonomy_buyers.py` | Government level and branch of the buyer |
| `aig/geo.py` | Regions, currencies, exchange rates |
| `aig/study.py` | Collect, label, aggregate, chart |

## Ask an AI agent to do it

Copy this into Claude, ChatGPT or any coding agent that can run Python and make HTTP calls:

```text
Recreate the Sell to State study "How governments buy AI" with current data.
Use the Python notebook at https://github.com/getbeton/how-governments-buy-ai.

1. Clone the repository. Install requirements.txt.
2. Get access to the Sell to State API.
   - If I give you an API key, set it as STS_API_KEY and go to step 4.
   - If not, sign up as an agent: POST https://app.selltostate.com/api/oidc/register
     with the JSON body {"client_name": "<your name> for <my name>"}.
     Keep client_id and payment_link from the answer.
3. Pay for access. The price is at GET https://app.selltostate.com/api/v1/price ($49 a month).
   - Show me the price and the payment_link. Wait for my yes.
   - I pay on the payment_link. If I give you a Stripe payment method token (pm_...) instead,
     POST {"payment_method_token": "pm_..."} to https://app.selltostate.com/api/v1/pay
     with the header Authorization: Bearer client:<client_id>.
4. Check access: GET https://app.selltostate.com/api/v1/whoami must show "active": true.
   Use the header x-api-key: <key>, or Authorization: Bearer client:<client_id>.
   Set STS_CLIENT_ID=<client_id> (or STS_API_KEY). Keep the key and the client_id private.
5. Run notebook.ipynb for these countries: [your countries, or all].
6. Report: AI tenders per 10,000 records by country and year, what governments buy,
   prices in US dollars by region and purchase type, and the AI tenders open now, with links.
7. Compare the results with https://www.selltostate.com/blog/how-governments-buy-ai/.
   Explain the differences: the notebook reads titles only, Sell to State covers other sources,
   and the data is newer.
```

## Licence

The code is MIT-licensed (see `LICENSE`). The data comes from public procurement portals through Sell to State; follow the [API terms](https://www.selltostate.com/terms/) when you publish rows. If you use the results, link to the article.
