"""Countries, regions, display names, currencies and exchange rates used by the study (2025 average rates, units per euro)."""

REGIONS = {
    'Western Europe': ['austria', 'belgium', 'france', 'germany', 'luxembourg', 'netherlands', 'liechtenstein', 'united-kingdom', 'ireland'],
    'Nordics & Baltics': ['denmark', 'finland', 'norway', 'sweden', 'iceland', 'estonia', 'latvia', 'lithuania'],
    'Southern Europe': ['spain', 'portugal', 'italy', 'greece', 'cyprus', 'malta'],
    'Central Europe': ['poland', 'czech-republic', 'slovakia', 'hungary', 'slovenia'],
    'Eastern Europe & Balkans': ['romania', 'bulgaria', 'croatia', 'ukraine', 'moldova', 'albania', 'kosovo', 'north-macedonia'],
    'North America': ['united-states', 'canada', 'mexico'],
    'Latin America': ['guatemala', 'honduras', 'dominican-republic', 'colombia', 'ecuador', 'peru', 'chile', 'paraguay', 'uruguay', 'brazil'],
    'Asia-Pacific': ['japan', 'singapore', 'australia', 'new-zealand'],
    'Middle East & Central Asia': ['israel', 'iran', 'uzbekistan', 'georgia'],
    'Africa': ['kenya', 'tanzania', 'rwanda', 'uganda', 'ghana', 'nigeria', 'zambia', 'liberia', 'south-africa'],
}
REGION_OF = {c: r for r, cs in REGIONS.items() for c in cs}
REGION_ORDER = list(REGIONS)
REGION_COLOR = {
    'Western Europe': '#1B3FC4', 'Nordics & Baltics': '#0E7C86', 'Southern Europe': '#8E5CC2', 'Central Europe': '#3A2E8C',
    'Eastern Europe & Balkans': '#9A6B3F', 'North America': '#E63B2E', 'Latin America': '#E8901A', 'Asia-Pacific': '#2E9E5B',
    'Middle East & Central Asia': '#C2457A', 'Africa': '#6E8B1F',
}
NAME = {
    'austria': 'Austria', 'belgium': 'Belgium', 'france': 'France', 'germany': 'Germany', 'luxembourg': 'Luxembourg', 'netherlands': 'Netherlands', 'liechtenstein': 'Liechtenstein',
    'united-kingdom': 'United Kingdom', 'ireland': 'Ireland', 'denmark': 'Denmark', 'finland': 'Finland', 'norway': 'Norway', 'sweden': 'Sweden', 'iceland': 'Iceland',
    'spain': 'Spain', 'portugal': 'Portugal', 'italy': 'Italy', 'greece': 'Greece', 'cyprus': 'Cyprus', 'malta': 'Malta', 'poland': 'Poland', 'czech-republic': 'Czechia',
    'slovakia': 'Slovakia', 'hungary': 'Hungary', 'slovenia': 'Slovenia', 'croatia': 'Croatia', 'romania': 'Romania', 'bulgaria': 'Bulgaria', 'estonia': 'Estonia',
    'latvia': 'Latvia', 'lithuania': 'Lithuania', 'ukraine': 'Ukraine', 'moldova': 'Moldova', 'georgia': 'Georgia', 'uzbekistan': 'Uzbekistan', 'albania': 'Albania',
    'kosovo': 'Kosovo', 'north-macedonia': 'North Macedonia', 'united-states': 'United States', 'canada': 'Canada', 'mexico': 'Mexico', 'guatemala': 'Guatemala',
    'honduras': 'Honduras', 'dominican-republic': 'Dominican Republic', 'colombia': 'Colombia', 'ecuador': 'Ecuador', 'peru': 'Peru', 'chile': 'Chile', 'paraguay': 'Paraguay',
    'uruguay': 'Uruguay', 'brazil': 'Brazil', 'japan': 'Japan', 'singapore': 'Singapore', 'australia': 'Australia', 'new-zealand': 'New Zealand', 'israel': 'Israel',
    'iran': 'Iran', 'kenya': 'Kenya', 'tanzania': 'Tanzania', 'rwanda': 'Rwanda', 'uganda': 'Uganda', 'ghana': 'Ghana', 'nigeria': 'Nigeria', 'zambia': 'Zambia',
    'liberia': 'Liberia', 'south-africa': 'South Africa',
}
# currency of the award amounts that Sell to State returns, per country
CURRENCY = {'albania': 'ALL', 'argentina': 'ARS', 'australia': 'AUD', 'austria': 'EUR', 'bahrain': 'BHD', 'belgium': 'EUR', 'brazil': 'BRL', 'bulgaria': 'EUR', 'canada': 'CAD', 'colombia': 'COP', 'croatia': 'EUR', 'cyprus': 'EUR', 'czech-republic': 'CZK', 'denmark': 'DKK', 'dominican-republic': 'DOP', 'ecuador': 'USD', 'estonia': 'EUR', 'finland': 'EUR', 'france': 'EUR', 'germany': 'EUR', 'ghana': 'GHS', 'greece': 'EUR', 'haiti': 'HTG', 'hungary': 'HUF', 'iran': 'IRR', 'ireland': 'EUR', 'israel': 'ILS', 'kenya': 'KES', 'latvia': 'EUR', 'liberia': 'USD', 'lithuania': 'EUR', 'luxembourg': 'EUR', 'malta': 'EUR', 'mexico': 'MXN', 'moldova': 'MDL', 'netherlands': 'EUR', 'new-zealand': 'NZD', 'nigeria': 'NGN', 'pakistan': 'PKR', 'paraguay': 'PYG', 'peru': 'PEN', 'philippines': 'PHP', 'poland': 'PLN', 'portugal': 'EUR', 'romania': 'RON', 'rwanda': 'RWF', 'samoa': 'WST', 'sierra-leone': 'SLE', 'singapore': 'SGD', 'slovakia': 'EUR', 'slovenia': 'EUR', 'south-africa': 'ZAR', 'spain': 'EUR', 'sweden': 'SEK', 'switzerland': 'CHF', 'taiwan': 'TWD', 'tanzania': 'TZS', 'trinidad-tobago': 'TTD', 'uganda': 'UGX', 'ukraine': 'UAH', 'united-kingdom': 'GBP', 'united-states': 'USD', 'uruguay': 'UYU', 'uzbekistan': 'UZS', 'zambia': 'ZMW'}
FX = {'EUR': 1, 'USD': 1.13, 'GBP': 0.857, 'JPY': 169, 'CAD': 1.57, 'AUD': 1.75, 'NZD': 1.92, 'SGD': 1.47, 'CHF': 0.94, 'NOK': 11.7, 'SEK': 11.0, 'DKK': 7.46,
      'ISK': 145, 'PLN': 4.24, 'CZK': 25.0, 'HUF': 400, 'RON': 5.05, 'BGN': 1.956, 'COP': 4650, 'DOP': 69, 'PYG': 8800, 'PEN': 4.15, 'CLP': 1070, 'CLF': 0.028,
      'GTQ': 8.7, 'HNL': 29.5, 'UYU': 46, 'BRL': 6.3, 'MXN': 21.5, 'ARS': 1250, 'ZAR': 20.4, 'KES': 146, 'TZS': 2950, 'RWF': 1600, 'GHS': 15, 'NGN': 1750,
      'ZMW': 30, 'LRD': 225, 'ALL': 98, 'ILS': 4.0, 'UZS': 14500, 'UAH': 47, 'MKD': 61.5, 'GEL': 3.1, 'MDL': 19.8, 'UGX': 4150, 'IRR': 47000}
# countries in Sell to State outside the 2026 study (approximate 2025 averages, units per euro)
FX.update({'BHD': 0.425, 'HTG': 148, 'PKR': 318, 'PHP': 65, 'WST': 3.1, 'SLE': 25.7, 'TWD': 35.6, 'TTD': 7.66})
REGION_OF.update({c: 'Other' for c in CURRENCY if c not in REGION_OF})
NAME.update({c: c.replace('-', ' ').title() for c in CURRENCY if c not in NAME})

def to_usd(amount, country):
    """Local-currency amount -> US dollars at 2025 average rates (None when unknown)."""
    try:
        a = float(amount)
    except (TypeError, ValueError):
        return None
    c = CURRENCY.get(country, 'EUR'); r = FX.get(c)
    return a / r * FX["USD"] if r and a > 0 else None
