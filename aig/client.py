"""A small client for the Sell to State REST API (https://www.selltostate.com/api).

Auth, one of:
- STS_API_KEY: a key from https://app.selltostate.com (Settings > API), sent as x-api-key;
- STS_CLIENT_ID: an agent client from register() below, sent as Authorization: Bearer client:<id>.
  A new client has no data access until someone pays its payment link ($49 a month).
Limits: 300 search requests a minute, 50 hits a page. The client waits between calls and retries on 429 and 5xx."""
import os
import time

import requests

BASE = os.environ.get('STS_API_BASE', 'https://app.selltostate.com/api/v1')


def register(client_name='how-governments-buy-ai notebook', base=BASE):
    """Agent signup (RFC 7591 dynamic client registration). Returns client_id, client_secret and payment_link.
    Open payment_link in a browser and pay; then set STS_CLIENT_ID=<client_id>. Rate limit: 10 a hour per IP."""
    r = requests.post(base.rsplit('/api/v1', 1)[0] + '/api/oidc/register', json={'client_name': client_name}, timeout=60)
    r.raise_for_status()
    return r.json()


class STS:
    def __init__(self, key=None, client_id=None, base=BASE, per_minute=280):
        self.key = key or os.environ.get('STS_API_KEY')
        self.client_id = client_id or os.environ.get('STS_CLIENT_ID')
        if not self.key and not self.client_id:
            raise SystemExit('Set STS_API_KEY (a key from https://app.selltostate.com) or STS_CLIENT_ID (from aig.client.register()).')
        self.base = base.rstrip('/')
        self.gap = 60.0 / per_minute
        self.last = 0.0
        self.calls = 0
        self.http = requests.Session()
        auth = {'x-api-key': self.key} if self.key else {'Authorization': f'Bearer client:{self.client_id}'}
        self.http.headers.update({**auth, 'User-Agent': 'how-governments-buy-ai notebook'})

    def get(self, path, **params):
        params = {k: v for k, v in params.items() if v is not None}
        for attempt in range(8):
            wait = self.gap - (time.time() - self.last)
            if wait > 0:
                time.sleep(wait)
            self.last = time.time()
            r = self.http.get(f'{self.base}/{path}', params=params, timeout=90)
            self.calls += 1
            if r.status_code == 402:
                raise SystemExit('402 Payment Required: this credential has no active plan. Pay the payment link of your client, or start a plan at https://app.selltostate.com/plans.')
            if r.status_code == 429 or r.status_code >= 500:
                time.sleep(min(60, 2 ** attempt))
                continue
            if r.status_code == 400:
                raise ValueError(f'400 from {path}: {r.text[:300]}')
            r.raise_for_status()
            return r.json()
        raise RuntimeError(f'{path} failed after retries: {params}')

    def whoami(self):
        return self.get('whoami')

    def search(self, q='*', page=1, per_page=50, **filters):
        """One page of tender search. Filters: country, year_min, year_max, lifecycle (open|awarded|planned|cancelled), sector, ..."""
        return self.get('search', scope='tenders', q=q, page=page, per_page=per_page, **filters)

    def all_hits(self, q, max_pages=100, **filters):
        """Every hit of a query, page by page (50 a page). Returns (hits, found)."""
        first = self.search(q, page=1, **filters)
        hits, found = list(first.get('hits') or []), first.get('found') or 0
        pages = min(max_pages, (found + 49) // 50)
        for p in range(2, pages + 1):
            hits += self.search(q, page=p, **filters).get('hits') or []
        return hits, found

    def country_counts(self, **filters):
        """Records per country for the filters (one call: the country facet of a match-all search)."""
        r = self.search('*', per_page=1, **filters)
        return {f['value']: f['count'] for f in (r.get('facets') or {}).get('country', [])}
