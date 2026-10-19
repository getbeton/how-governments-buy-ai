---
name: how-governments-buy-ai
description: Rerun the Sell to State study "How governments buy AI" on live procurement data. Use when the user asks to recreate, update or extend the study, or wants AI tenders per 10,000 procurements, AI purchase types, AI prices in US dollars or open AI tenders for one or more countries.
---

# Rerun "How governments buy AI"

The study: https://www.selltostate.com/blog/how-governments-buy-ai/
The code: https://github.com/getbeton/how-governments-buy-ai (MIT). It needs Sell to State API access ($49 a month).

Ask the user for the countries first (default: all). Then do these steps.

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
