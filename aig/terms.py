"""Search terms sent to the Sell to State search. The search is broad on purpose: it matches words in the tender title,
the buyer name and the supplier name, and it also matches prefixes ("AI" finds "Air"). The keyword families in
families.py then decide which hits are AI. Add a term here when a country writes AI in a way the list misses."""

COMMON = ['AI', 'artificial intelligence', 'machine learning', 'deep learning', 'neural network', 'generative', 'LLM', 'language model',
          'GPT', 'ChatGPT', 'OpenAI', 'Copilot', 'Claude', 'Gemini', 'Mistral', 'chatbot', 'voicebot', 'virtual assistant',
          'computer vision', 'facial recognition', 'speech recognition', 'agentic', 'Nvidia']

BY_LANG = {
    'de': ['KI', 'künstliche Intelligenz', 'künstlicher Intelligenz', 'maschinelles Lernen', 'Spracherkennung', 'Sprachmodell'],
    'fr': ['IA', 'intelligence artificielle', 'apprentissage automatique', 'reconnaissance vocale', 'agent conversationnel', 'assistant virtuel'],
    'es': ['IA', 'inteligencia artificial', 'aprendizaje automático', 'asistente virtual', 'reconocimiento facial', 'reconocimiento de voz'],
    'pt': ['IA', 'inteligência artificial', 'aprendizado de máquina', 'assistente virtual', 'reconhecimento facial'],
    'it': ['IA', 'intelligenza artificiale', 'apprendimento automatico', 'assistente virtuale'],
    'nl': ['kunstmatige intelligentie', 'spraakherkenning'],
    'pl': ['sztuczna inteligencja', 'sztucznej inteligencji', 'uczenie maszynowe'],
    'cs': ['umělá inteligence', 'umělé inteligence'], 'sk': ['umelá inteligencia', 'umelej inteligencie'],
    'hu': ['mesterséges intelligencia'], 'ro': ['inteligență artificială', 'inteligenta artificiala'],
    'el': ['τεχνητή νοημοσύνη', 'τεχνητής νοημοσύνης'], 'bg': ['изкуствен интелект'],
    'hr': ['umjetna inteligencija', 'umjetne inteligencije'], 'sl': ['umetna inteligenca', 'umetne inteligence'],
    'lv': ['mākslīgais intelekts', 'mākslīgā intelekta'], 'lt': ['dirbtinis intelektas', 'dirbtinio intelekto'], 'et': ['tehisintellekt', 'tehisaru'],
    'fi': ['tekoäly', 'koneoppiminen'], 'sv': ['artificiell intelligens'], 'da': ['kunstig intelligens'], 'no': ['kunstig intelligens', 'KI'], 'is': ['gervigreind'],
    'uk': ['штучний інтелект', 'штучного інтелекту', 'ШІ'], 'ru': ['искусственный интеллект'], 'he': ['בינה מלאכותית'], 'fa': ['هوش مصنوعی'],
    'ja': ['人工知能', '生成AI'], 'zh': ['人工智能'], 'id': ['kecerdasan buatan'], 'tr': ['yapay zeka'], 'ar': ['الذكاء الاصطناعي'],
}

LANGS = {
    'germany': ['de'], 'austria': ['de'], 'switzerland': ['de', 'fr', 'it'], 'luxembourg': ['fr', 'de'], 'liechtenstein': ['de'], 'belgium': ['fr', 'nl'],
    'france': ['fr'], 'netherlands': ['nl'], 'spain': ['es'], 'portugal': ['pt'], 'italy': ['it'], 'greece': ['el'], 'cyprus': ['el'], 'malta': [],
    'poland': ['pl'], 'czech-republic': ['cs'], 'slovakia': ['sk'], 'hungary': ['hu'], 'slovenia': ['sl'], 'croatia': ['hr'], 'romania': ['ro'],
    'moldova': ['ro', 'ru'], 'bulgaria': ['bg'], 'ukraine': ['uk', 'ru'], 'latvia': ['lv'], 'lithuania': ['lt'], 'estonia': ['et'],
    'finland': ['fi', 'sv'], 'sweden': ['sv'], 'denmark': ['da'], 'norway': ['no'], 'iceland': ['is'], 'israel': ['he'], 'iran': ['fa'],
    'japan': ['ja'], 'taiwan': ['zh'], 'brazil': ['pt'], 'canada': ['fr'], 'haiti': ['fr'],
    'mexico': ['es'], 'guatemala': ['es'], 'honduras': ['es'], 'dominican-republic': ['es'], 'colombia': ['es'], 'ecuador': ['es'], 'peru': ['es'],
    'chile': ['es'], 'paraguay': ['es'], 'uruguay': ['es'], 'argentina': ['es'], 'bolivia': ['es'], 'costa-rica': ['es'], 'el-salvador': ['es'],
    'panama': ['es'], 'turkey': ['tr'], 'bahrain': ['ar'], 'indonesia': ['id'],
}


def terms_for(country):
    """The English terms plus the terms of the country's languages, without duplicates."""
    out = list(COMMON)
    for lang in LANGS.get(country, []):
        out += [t for t in BY_LANG[lang] if t not in out]
    return out
