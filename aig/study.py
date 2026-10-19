"""The study pipeline on Sell to State data: collect AI candidates and denominators, label them with the study's rules,
aggregate, chart. Every step writes to data/ so that a rerun continues where it stopped."""
import json
import os
import re

import pandas as pd

from . import buyers, geo
from .families import tag
from .taxonomy3 import AUDIENCE, CAPABILITY, PURCHASE, TECH_PURCHASES, first, tag_brands
from .taxonomy4 import USE_CASES
from .terms import terms_for

# the study's guard: a title that buys a product (supply verb, licence, platform, GPU) and names no course is not a training purchase
SUPPLY = re.compile(r'^\s*((contrata[cç][aã]o|contrataci[oó]n) de (uma |una )?empresa( especializada)? (para|na|en) (o |a |la |el )?)?(suministro|dostawa|доставка|supply|delivery|lieferung|beschaffung|aquisi[cç][aã]o|fornecimento|adquisici[oó]n|compra de (licen|equip)|licenciamento|licen[cç]as? de uso|achizi[tț]i)', re.I)
COURSE = re.compile(r'curso|course|cursos|kurs|szkoleni|capacita[cç][aã]o de|workshop|webinar|inscri', re.I)
PROD = re.compile(r'licen[cç]|licencia|subscri|assinatura|suscripci|software|plataforma|platform|equipament|equipment|equipo(?!s? de (gesti|trabajo|docen))|esta[cç][aã]o de trabalho|workstation|computador|notebook|c[aâá]mara|camera|\bgpu|servidores de|servidor de (alto|dados)|sprz[eę]t|oprogramowani|zestaw', re.I)
COURSE2 = re.compile(r'curso|course|cursos|kurs|treinamento (em|sobre|de servidores|para servidores)|capacita[cç][aã]o (em|sobre|de servidores|para servidores|de \d)|capacitaci[oó]n(es)? (en|sobre|para)|capacitaciones|workshop|webinar|inscri|evento|palestra|semin[aá]rio|congress|p[oó]s-gradua|\bmba\b|aperfei[cç]oamento|diplomado|masterclass|bootcamp|szkoleni|schulung|formation|formaci[oó]n (en|de personal)|forma[cç][aã]o (em|de)|apprentic|vaga|participa[cç][aã]o', re.I)
P_NOTR = [r for r in PURCHASE if r[0] != 'Training and skills']


def purchase(title):
    p = first(PURCHASE, title, default='Unclear')
    if p == 'Training and skills' and ((SUPPLY.search(title) and not COURSE.search(title)) or (PROD.search(title) and not COURSE2.search(title))):
        p = first(P_NOTR, title, default='Unclear')
    return p

DATA = os.environ.get('AIG_DATA', 'data')


def _path(name):
    os.makedirs(DATA, exist_ok=True)
    return os.path.join(DATA, name)


# ---------------------------------------------------------------- 1. collect
def countries(sts):
    """Every country that Sell to State covers, with its number of records."""
    return sts.country_counts()


def collect(sts, country_list, year_min=2024, year_max=2026, lifecycle=None, max_pages=60, name='hits.jsonl', log=print):
    """Search every term of each country and keep the raw hits (title, buyer · supplier, amount, year, lifecycle, ids).
    Resumable: a (country, term) pair already in the file is skipped."""
    p = _path(name)
    done = set()
    if os.path.exists(p):
        for line in open(p, encoding='utf-8'):
            r = json.loads(line)
            done.add((r['_country'], r['_term']))
    with open(p, 'a', encoding='utf-8') as out:
        for c in country_list:
            for t in terms_for(c):
                if (c, t) in done:
                    continue
                hits, found = sts.all_hits(t, max_pages=max_pages, country=c, year_min=year_min, year_max=year_max, lifecycle=lifecycle)
                for h in hits:
                    out.write(json.dumps(dict(h, _country=c, _term=t), ensure_ascii=False) + '\n')
                if not hits:
                    out.write(json.dumps({'_country': c, '_term': t, '_empty': True}) + '\n')
            log(f'{c}: done ({sts.calls} API calls so far)')
    return load_hits(name)


def load_hits(name='hits.jsonl'):
    rows = [json.loads(line) for line in open(_path(name), encoding='utf-8')]
    d = pd.DataFrame([r for r in rows if not r.get('_empty')])
    return d.drop_duplicates('slug') if len(d) else d


def denominators(sts, years=(2024, 2025, 2026), lifecycle=None):
    """Records per country and year: the denominator of the share of AI (one call per year)."""
    rows = []
    for y in years:
        for c, n in sts.country_counts(year_min=y, year_max=y, lifecycle=lifecycle).items():
            rows.append(dict(country=c, year=y, records=n))
    d = pd.DataFrame(rows)
    d.to_csv(_path('denominators.csv'), index=False)
    return d


# ---------------------------------------------------------------- 2. label
def label(hits):
    """Apply the study's rules to the titles. Keeps only the hits that the keyword families mark as AI."""
    d = hits.copy()
    d['title'] = d['title'].fillna('')
    d['buyer'] = d['sub'].fillna('').str.split(' · ').str[0]
    d['supplier'] = d['sub'].fillna('').str.split(' · ').str[1]
    d['core'] = [sorted(k for k, v in tag(t, c).items() if v == 'core') for t, c in zip(d.title, d.country)]
    d = d[d.core.str.len() > 0].copy()
    d['region'] = d.country.map(lambda c: geo.REGION_OF.get(c, 'Other'))
    d['purchase'] = [purchase(t) for t in d.title]
    d['capability'] = [first(CAPABILITY, t, default='General-purpose or not specified') if p in TECH_PURCHASES or p == 'Unclear'
                       else 'n/a (not a technology purchase)' for p, t in zip(d.purchase, d.title)]
    d['use_case'] = [first(USE_CASES[c], t, default='Other or not stated') if c in USE_CASES else None for c, t in zip(d.capability, d.title)]
    d['level'] = [buyers.level(b) for b in d.buyer]
    d['branch'] = [buyers.branch(b, lv) for b, lv in zip(d.buyer, d.level)]
    d['audience'] = [first(AUDIENCE, t, default='Not stated') for t in d.title]
    d['brands'] = [tag_brands(t) for t in d.title]
    amounts = d['amount'] if 'amount' in d.columns else [None] * len(d)          # open tenders carry no amount
    d['value_usd'] = pd.to_numeric(pd.Series([geo.to_usd(a, c) for a, c in zip(amounts, d.country)], index=d.index, dtype='object'), errors='coerce')
    d.loc[d.value_usd < 10, 'value_usd'] = None          # values under $10 are placeholders (1 EUR, 0.01 EUR) in some notices
    d['app_url'] = [f'https://app.selltostate.com/tenders/{c}/{s}' for c, s in zip(d.country, d.slug)]
    return d


# ---------------------------------------------------------------- 3. aggregate
def shares(ai, den, min_records=2000):
    """AI tenders per 10,000 records, by country and year (titles only: the API searches titles, buyers and suppliers)."""
    n = ai.groupby(['country', 'year']).size().rename('ai').reset_index()
    s = den.merge(n, on=['country', 'year'], how='left').fillna({'ai': 0})
    s['per_10k'] = 1e4 * s.ai / s.records
    s['region'] = s.country.map(lambda c: geo.REGION_OF.get(c, 'Other'))
    s['name'] = s.country.map(lambda c: geo.NAME.get(c, c))
    return s[s.records >= min_records].sort_values(['year', 'per_10k'], ascending=[True, False])


def mix(ai, col, by=None):
    """Share of AI tenders in each value of a label (optionally by region or country), in %."""
    if by:
        return (ai.groupby(by)[col].value_counts(normalize=True) * 100).round(1).unstack(fill_value=0)
    return (ai[col].value_counts(normalize=True) * 100).round(1)


def brands(ai):
    b = ai.explode('brands').dropna(subset=['brands'])
    return b.groupby('brands').agg(tenders=('slug', 'nunique'), median_usd=('value_usd', 'median')).sort_values('tenders', ascending=False)


def prices(ai, by='region', min_n=20):
    """Percentiles of the contract value in US dollars."""
    v = ai.dropna(subset=['value_usd'])
    q = v.groupby(by).value_usd.describe(percentiles=[.1, .25, .5, .75, .9])
    return q[q['count'] >= min_n].sort_values('50%')


# ---------------------------------------------------------------- 4. charts (matplotlib)
def chart_ranking(s, year, top=40, ax=None):
    import matplotlib.pyplot as plt
    x = s[s.year == year].nlargest(top, 'per_10k').iloc[::-1]
    ax = ax or plt.subplots(figsize=(8, 0.28 * len(x) + 1))[1]
    ax.barh(x.name, x.per_10k, color='#1B3FC4')
    ax.set_xlabel('AI tenders per 10,000 records (AI in the title)')
    ax.set_title(f'AI tenders per 10,000 records, {year}')
    return ax


def chart_mix(m, title, ax=None):
    import matplotlib.pyplot as plt
    m = m.sort_values()
    ax = ax or plt.subplots(figsize=(8, 0.32 * len(m) + 1))[1]
    ax.barh(m.index, m.values, color='#E8901A')
    ax.set_xlabel('% of AI tenders')
    ax.set_title(title)
    return ax


def chart_prices(q, title, ax=None):
    import matplotlib.pyplot as plt
    ax = ax or plt.subplots(figsize=(8, 0.4 * len(q) + 1))[1]
    y = range(len(q))
    ax.hlines(y, q['10%'], q['90%'], color='#B8B8B0', lw=2)
    ax.hlines(y, q['25%'], q['75%'], color='#1B3FC4', lw=8)
    ax.plot(q['50%'], y, 'o', color='white', mec='black')
    ax.set_yticks(list(y), q.index)
    ax.set_xscale('log')
    ax.set_xlabel('Contract value, US$ (line: 10th-90th percentile, bar: 25th-75th, dot: median)')
    ax.set_title(title)
    return ax
