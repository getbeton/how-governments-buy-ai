"""Keyword families of the study: each family = (regex, flags, context check).
A row is AI if at least one CORE family hits with a valid context. ADJACENT families are tagged, not counted."""
import re

DE_LANG = {'germany', 'austria', 'switzerland', 'luxembourg', 'liechtenstein', 'norway'}   # Norwegian also writes KI (kunstig intelligens)
I = re.I
ENGLISH = {'united-kingdom', 'ireland', 'united-states', 'australia', 'new-zealand', 'nigeria', 'kenya', 'ghana', 'tanzania', 'uganda', 'zambia', 'liberia', 'rwanda', 'south-africa', 'singapore', 'malta', 'cyprus', 'india'}
AFRICA = {'kenya', 'tanzania', 'rwanda', 'uganda', 'ghana', 'nigeria', 'zambia', 'liberia', 'south-africa'}
IA_LANG = {'spain', 'portugal', 'france', 'belgium', 'luxembourg', 'switzerland', 'italy', 'romania', 'moldova', 'canada', 'andorra', 'monaco', 'cuba'}
SPANISH_CAPS = {'colombia', 'mexico', 'dominican-republic', 'paraguay', 'argentina', 'peru', 'ecuador', 'uruguay', 'chile', 'guatemala', 'honduras', 'brazil', 'costa-rica', 'el-salvador', 'panama', 'bolivia'}
IA_LANG |= SPANISH_CAPS

def _tok_ai(t, m, country):
    after, before = t[m.end():m.end() + 14], t[max(0, m.start() - 14):m.start()]
    if re.search(r'\b[A-Z]{0,6}\d{2,}[/-]\d{2,}\s*$', before):
        return False                                        # tender references 'H24/039 AI', 'INFQ002/24 AI'
    if re.match(r' ?-?\d', after) or before.endswith(',') or re.match(r' bis| NOGALES|II|-\d', after) or before.endswith('Altholz '):
        return False                                        # refs "AI 2024-0071", "AI-232/25", NSN ",AI", "Altholz AI"
    near = t[max(0, m.start() - 70):m.end() + 70]
    if re.search(r'insemina|semen|straws?\b|liquid nitrogen|bull\b|cattle|dairy|livestock|veterin|ganad|bovin|farmers?\b|vaccinat|heifer|breeding', t[max(0, m.start() - 250):m.end() + 250], I):
        return False                                        # AI = artificial insemination (livestock)
    if re.search(r'smart ?tv|\buhd\b|\b4k\b|televis|\btv\b|led tv|hisense|upscal|zinc|alu-?zinc|air ?condition|aircon', near, I):
        return False                                        # "4K AI Upscaler" TVs, "AI-Zinc sheet", "AI[R CONDITIONER]"
    if re.search(r'\b(gearbox|duct|valve|valv|bracket|bushing|bearing|actuator|harness)\b[^|]{0,25}$', t[max(0, m.start() - 30):m.start()], I) or re.match(r',? ?(gearbox|duct|assembly)\b', after, I):
        return False                                        # aircraft parts: 'DUCT ASSEMBLY,BLEED AI' (bleed air), 'REMAN E-3 AI GEARBOX'
    if country in AFRICA and re.search(r'ai technicians?|\bsdtp\b|\brddp\b', t[max(0, m.start() - 60):m.end() + 60], I):
        return False                                        # AI technicians = artificial insemination (dairy programmes)
    if after.startswith('&') or re.search(r'antiserum|salmonella|new england journal|nejm|tripod|штатив|gimbal|selfie', near, I):
        return False                                        # 'POLY AI&VI' antiserum, 'NEJM AI' journal, 'AI tracking' tripods
    if re.search(r'air intercept|\(AI\) training', t, I) or re.search(r'\d\w*-$', before):
        return False                                        # model codes "S5808P-E2-AI"
    if country in SPANISH_CAPS | {'romania', 'moldova', 'italy'} and \
            not re.search(r'\b(powered|based|tools?|platform|plataforma|solution|soluci[oó]n|solu[tț]i\w*|soluzion\w*|basat\w*|strument\w*|piattaform\w*|bazat\w*|software|licen\w*|agent|model|assistant|asistent|chat|generative|generativ\w*|world tour|for\b)', t[max(0, m.start() - 40):m.end() + 40], I):
        return False                                        # all-caps Spanish titles: "PUEBLO INGI AI"
    return True

def _tok_ia(t, m, country):
    if re.search(r'apneia|apnea|ronco|cpap|hipopneia|hipopnea', t[max(0, m.start() - 80):m.end() + 80], I):
        return False                                        # IA = índice de apneia (sleep devices)
    if country not in IA_LANG:
        return False                                        # 'IA' means AI only in es/pt/fr/it/ro text; elsewhere state codes, road classes
    after, before = t[m.end():m.end() + 14], t[max(0, m.start() - 30):m.start()]
    nxt = re.match(r' ([A-ZÁÉÍÓÚÑÇÃÕÊ]{3,})', after)
    if nxt and t[max(0, m.start() - 40):m.end() + 40].isupper() and nxt.group(1) not in ('PARA', 'CON', 'QUE', 'DEL', 'COMO', 'NOS', 'NAS', 'PELA', 'PELO', 'POR', 'SOBRE', 'COM', 'DOS', 'DAS', 'LOS', 'LAS') and not re.match(r'(GENERATIV|GENERAT|APLICAD|BASAD|BASEAD|CONVERSACION|AGENT|ASSIST|ASIST|MICROSOFT|COPILOT|CHAT|ETIC|ÉTIC|RESPONSABLE)', nxt.group(1)):
        return False                                        # all-caps typo 'DEL ARTÍCULO 79 DE IA CONVENCIÓN' (IA = LA)
    if re.search(r'\b[IVX]+( e|,| y|/)\s*$', before) or re.search(r'influenza aviar|gripe avi|aviaire|avian', t, I) or re.search(r'intendencia|aduana', t[max(0, m.start() - 60):m.start()], I):
        return False                                        # 'Anexo I e IA', 'categoría I, IA'; IA = influenza aviar
    if re.search(r'\b[A-Z]{2,7},\s*$', before) and re.match(r'\s*(,\s*[A-Z]{2,}|\s+E\s+[A-Z]{2,})', after):
        return False                                        # acronym lists "IFCH, FEA, IA, FEAGRI E IB"
    if re.match(r'-|:|/| (IT|IV)\b', after) or before.endswith(('/', '-')) or re.match(r' (Paita|Tacna|Puno|Callao|Chiclayo|Tumbes|Ilo|Iquitos|Mollendo|Pisco|Salaverry|Cusco|Arequipa|Lima|A[ée]rea|Mar[ií]tima)\b', after):
        return False
    ctx_b = re.search(r'\b(de|del|con|la|las|sobre|en|por|e|y|da|das|do|na|nas|no|com|à|a|par|pour|l.|di|della|dell.|dei|degli|tramite|basat[ao] sull.|basad[ao]s? en|mediante|uso de|usando|com recurso a|baseada? em|assistid[ao] por|apoiad[ao] por|of|for the|outils d.|solution d.|syst[eè]mes? d.)\s*$', before, I)
    ctx_a = re.match(r'\s*(generativ|g[ée]n[ée]rativ|\)|,|\.|;|$| y | e | et | aplicad|para|pour|en la|no |na |-ready|-native)', after, I)
    return bool(ctx_b or ctx_a or t[m.start() - 1:m.end() + 1] == '(IA)')

def _tok_ki(t, m, country):
    after, before = t[m.end():m.end() + 12], t[max(0, m.start() - 12):m.start()]
    if not (country in DE_LANG or re.search(r'(Germany|Austria|Luxembourg|Switzerland|Norway) –', t)):
        return False
    if re.match(r' (SE|SO|JE|JIH|GA|JO|SI)\b', after) or re.search(r'(UKSH|AG|UK) $', before) or re.match(r' ?(Akad|/)', after):
        return False
    if not after.startswith('-') and re.search(r'neubau|umbau|hochbau|tiefbau|bahnhof|streckenplan|abbruch|montage|catering|kapitel|sanierung|bauleistung|planung|grundschule', t, I):
        return False                                        # construction codes "KI 3.0, Kapitel 2", "Streckenplanung, KI und Hochbau"
    return True

def _tok_local(t, m, country):
    """SI (pl), UI (cs/sk), MI (hu/lv), DI (lt), ИИ (bg/uz/ua-ru), ШІ (ua): only in its own country and after a strong AI context."""
    tok = m.group(0); before = t[max(0, m.start() - 45):m.start()].lower(); after = t[m.end():m.end() + 20].lower()
    rule = {
        'SI': ({'poland'}, r'(narzędzi\w*|systemu|systemów|rozwiąza\w*|algorytm\w*|technologi\w*|wykorzystaniem|opart\w* na|asystent\w*|modułem|zastosowani\w*)\s+$'),
        'UI': ({'czech-republic', 'slovakia'}, r'(s využitím|pomocí|nástroj\w*|technologi\w*|řešení|riešení|na bázi|založen\w* na|s podporou|podporou)\s+$'),
        'MI': ({'hungary', 'latvia'}, r'(alapú|izmantojot|ar)\s+$'),
        'DI': ({'lithuania'}, r'(naudojant|pagrindu veikianč\w*)\s+$'),
        'ИИ': ({'bulgaria', 'uzbekistan', 'ukraine'}, r'(с использованием|на основе|с помощью|използване на|чрез)\s+$'),
        'ШІ': ({'ukraine'}, r'(з використанням|на основі|за допомогою)\s+$'),
    }[tok]
    if country not in rule[0]:
        return False
    return bool(re.search(rule[1], before, I)) or (tok == 'MI' and after.startswith('-alapú'))

BIODEV = re.compile(r'eletr[oô]nicos? de ponto|registradores? eletr[oô]nicos?|rel[oó]gios? (eletr[oô]nicos? )?de ponto|\brep-?c\b|controle eletr[oô]nico de (frequ|ponto|jornada)|assiduidade|frequ[eê]ncia de servidores|estaci[oó]n de puerta|portero|videoportero|intercom\w*|door station|control horario|control de horario|marcaci[oó]n|catraca|controle de acesso|controlador\w* de acesso|registr\w* de ponto|ponto eletr|rel[oó]gio( de)? ponto|ponto facial|molinete|talanquera|zutritt|door access|reloj|ponche|marcador|biom[eé]tric|attendance|attandance|time ?& ?att|time clock|control de asistencia|control de acceso|access control|torniquete|turnstile|cerradura|door lock', I)

PHRASE_CORE = (r'artificial intelligence|machine learning|deep learning|neural net|\bgenerative\b|\bgen ?ai\b|language model|foundation model|natural language processing|\bagentic|'
               r'inteligencia artificial|aprendizaje (autom|profundo)|redes neuronales|modelos? de lenguaje|intelig[eê]ncia artificial|aprendizagem (autom|profunda)|aprendizado de m[aá]quina|redes neurais|'
               r'intelligence artificielle|apprentissage (automatique|profond)|r[eé]seaux? de neurones|k[uü]nstliche[nrs]? intelligenz|maschinelle[ns]? lernen|neuronale[n]? netz|sprachmodell|'
               r'intelligenza artificiale|apprendimento automatico|kunstmatige intelligentie|machinaal leren|sztuczn\w* inteligencj|uczeni\w* (maszynow|g[lł][eę]bok)|sieci neuronow|um[eě]l\w* inteligenc|strojov\w* u[cč]en|neuronov\w* s[ií]t|'
               r'mesters[eé]ges intelligenci|g[eé]pi tanul[aá]s|m[aā]ksl[iī]g\w* intelekt|ma[sš][iī]nm[aā]c[iī]|dirbtin\w* intelekt|ma[sš]inin\w* mokym|tehisintellekt|tehisaru|masin[oõ]pe|teko[aä]ly|koneoppi|'
               r'artificiell intelligens|maskininl[aä]rning|kunstig intelligens|maskinl[aæ]ring|umjetn\w* inteligencij|umetn\w* inteligenc|strojno u[cč]enje|inteligen\w* artificial|τεχνητ\w* νοημοσ[υύ]ν|μηχανικ\w* μ[αά]θηση|'
               r'изкуствен\w* интелект|машинно обучение|штучн\w* інтелект|машинн\w* навчанн|искусственн\w* интеллект|нейросет|нейронн\w* сет|машинн\w* обучени|сунъий интеллект|inteligjenc\w* artificial|vještačk\w* inteligencij|veštačk\w* inteligencij|вештачк\w* интелигенциј|вештачк\w* интелиґенциј|ხელოვნური ინტელექტ|машинско учење|mašinsko učenje|sun.iy intellekt|בינה מלאכותית|למידת מכונה|למידה עמוקה|هوش مصنوعی')
FAMILIES = {  # name: (kind, regex, flags, validator or None)
    'phrase_ai':      ('core', PHRASE_CORE, I, None),
    'tok_AI':         ('core', r'\bAI\b', 0, _tok_ai),
    'tok_IA':         ('core', r'\bIA\b', 0, _tok_ia),
    'tok_KI':         ('core', r'\bKI\b', 0, _tok_ki),
    'tok_local':      ('core', r'\b(SI|UI|MI|DI)\b|ИИ|ШІ', 0, _tok_local),
    'tok_LLM_GPT':    ('core', r'\b(LLM|GPT|NLP)\b', 0, lambda t, m, c: not re.search(r'lease management|local municipality|\(LLM\) WITH|north lanarkshire|nlp (condition|propert)', t, I) and c != 'south-africa' and t[m.end():m.end() + 1] != '/' and t[m.start() - 1:m.start()] != '/'
                       and not (m.group(0) == 'NLP' and re.search(r'nefrostom|nephrostom|cateter|catheter|urolog|\bCH \d', t, I))
                       and not (m.group(0) == 'GPT' and re.search(r'reactiv|reagent|reagenz|odczynnik|laborator|transaminas|\bALT\b|\bAST\b|ALAT|ASAT|GOT\b|glutam|analiz|consumabil|medicament', t, I))),
    'genai_products': ('core', r'(?<!\w)copilot(?!e\b)|chatgpt|openai|azure openai|watsonx|vertex ai|sagemaker|\banthropic\b|aleph alpha|hugging ?face|\bclaude\b|\bmistral (ai\b(?!r)|large|medium|small|le chat|\d)|\bbedrock\b', I,
                       lambda t, m, c: (m.group(0).lower() not in ('claude', 'bedrock') and not m.group(0).lower().startswith('mistral') or bool(re.search(r'\b(ai|ia|ki|llm|model|licen|platform|plateforme|cloud|aws|software)\b', t, I)))
                       and (not m.group(0).lower().startswith('copilot') or not re.search(r'aircraft|cockpit|helicopter|airframe|\bseat\b|windshield|\bwindow\b|\bc-? ?\d{2,3}\b|pilot.{0,20}copilot', t, I) and bool(re.search(r'microsoft|github|m365|\b365\b|office|azure|security copilot|copilot (pro|studio|chat|for)\b|\b(ai|ia|ki)\b|licen|lizenz|suscrip|subscri|assinatura', t, I)))),
    'conversational': ('core', r'chat ?bot|voice ?bot|virtual (assistant|agent)|digital assistant|conversational (ai|agent|assistant|platform|interface)|asistente (virtual|conversacional)|agente conversacional|assistente virtual|agent conversationnel|assistant virtuel|sprachassistent|asystent\w* (wirtualn|g[lł]osow)|чат-?бот', I, lambda t, m, c: not re.search(r'pantalla|televis|smart ?tv|\btv\b|mando universal|smart ?speaker|altavoz|alto-?falante|soundbar|person(al|nel) digital assistant|asistentes? personal\w* digital|\bpda\b', t[max(0, m.start() - 120):m.end() + 120], I)),
    'biometric_dev':  ('adjacent', r'(catraca|controle de acesso|controlador\w* de acesso|ponto|reloj|ponche|marcador|biom[eé]tric|attendance|time clock|control de asistencia|control de acceso|access control|torniquete|turnstile|talanquera|terminal).{0,120}(facial|face|rostro)|(facial|face|rostro).{0,120}(catraca|acesso|ponto|reloj|ponche|marcador|asistencia|attendance|access control|control de acceso)', I, None),
    'recognition':    ('core', r'computer vision|image recognition|object detection|video analytic|(?<!rostro y )facial recognition|face recognition|(?<!interactive )speech recognition|(?<!interactive )voice recognition|speech.to.text|reconocimiento (de voz|facial|de im[aá]genes)|reconhecimento (de voz|facial|de imagem)|reconnaissance (vocale|faciale|d.images|de la parole)|spracherkennung|gesichtserkennung|bilderkennung|spraakherkenning|rozpoznawani\w* (mowy|twarzy|obrazu)|rozpozn[aá]v[aá]n\w* (re[cč]i|tv[aá][rř]|obrazu)|puheentunnist|taligenk[aä]nning', I, lambda t, m, c: not BIODEV.search(t[max(0, m.start() - 150):m.end() + 150])),
    'translation':    ('core', r'machine translation|traducci[oó]n autom[aá]tica|tradu[cç][aã]o autom[aá]tica|traduction automatique|maschinelle[ns]? übersetzung|t[lł]umaczeni\w* maszynow|strojov\w* p[rř]eklad|\bdeepl\b', I, None),
    # adjacent: tagged, not counted unless a core family also hits
    'predictive':     ('adjacent', r'predictive (analytic|model|maintenance)|anal[ií]tica predictiva|an[aá]lise preditiva|analityk\w* predykcyjn|anomaly detection|fraud detection|recommendation engine|sentiment analysis|text (mining|analytic)', I, None),
    'data_science':   ('adjacent', r'data science|ciencia de datos|ci[eê]ncia de dados|mlops|\bpalantir\b', I, None),
    'automation':     ('adjacent', r'robotic process automation|\bRPA\b|automatizaci[oó]n rob[oó]tica|intelligent (automation|process)|ohjelmistorobotiik|cognitive (search|service|automation)', 0, None),
    'plates_ivr':     ('adjacent', r'license plate recognition|number plate recognition|\bANPR\b|\bLPR\b|reconocimiento de matr[ií]culas|kennzeichenerkennung|rozpoznawani\w* tablic|interactive voice', I, None),
    'ocr':            ('adjacent', r'\bOCR\b|texterkennung|reconocimiento [oó]ptico|intelligent document', 0, None),
    'speech_vendor':  ('adjacent', r'\bnuance\b|dragon medical', I, None),
}
COMPILED = {k: (kind, re.compile(rx, fl), val) for k, (kind, rx, fl, val) in FAMILIES.items()}

# literal stems: a family regex runs only if one of its stems is in the lower-case text (speed only, same result)
PREFILTER = {
    'phrase_ai': ['intellig', 'intelig', 'inteligj', 'интелиген', 'ინტელექტ', 'учење', 'učenje', 'intelekt', 'intellekt', 'learning', 'neural', 'generativ', 'gen ai', 'genai', 'language model', 'foundation model', 'natural language',
                  'agentic', 'aprendiza', 'neuronal', 'neurais', 'de lenguaje', 'apprentissage', 'neurone', 'künstlich', 'kunstlich', 'maschinell', 'sprachmodell', 'apprendimento',
                  'kunstmatige', 'machinaal', 'sztuczn', 'uczeni', 'neuronow', 'strojov', 'neuronov', 'gépi tanul', 'gepi tanul', 'mašīnm', 'masinm', 'mašinm', 'masīnm', 'mokym',
                  'tehisaru', 'masinope', 'masinõpe', 'tekoäly', 'tekoaly', 'koneoppi', 'maskininl', 'maskinl', 'strojno u', 'τεχνητ', 'μηχανικ', 'изкуствен', 'машинно', 'штучн',
                  'машинн', 'искусствен', 'нейрос', 'нейронн', 'сунъий', 'בינה', 'למידת', 'למידה', 'هوش'],
    'recognition': ['vision', 'recogn', 'object detect', 'video analytic', 'facial', 'speech', 'reconocim', 'reconhecim', 'reconnaissance', 'erkennung', 'herkenning', 'rozpozn',
                    'tunnist', 'igenkänn', 'igenkann'],
    'genai_products': ['copilot', 'chatgpt', 'openai', 'watsonx', 'vertex ai', 'sagemaker', 'anthropic', 'aleph alpha', 'hugging', 'claude', 'mistral', 'bedrock'],
    'predictive': ['predictive', 'predictiva', 'preditiva', 'predykcyjn', 'anomaly', 'fraud', 'recommendation', 'sentiment', 'text mining', 'text analytic'],
    'translation': ['translation', 'traducci', 'tradução', 'traducao', 'traduction', 'übersetzung', 'ubersetzung', 'tłumacz', 'tlumacz', 'překlad', 'preklad', 'deepl'],
    'plates_ivr': ['plate recognition', 'anpr', 'lpr', 'matr', 'kennzeichen', 'tablic', 'interactive voice'],
    'data_science': ['data science', 'ciencia de datos', 'ciência de dados', 'ciencia de dados', 'mlops', 'palantir'],
    'speech_vendor': ['nuance', 'dragon medical'],
    'biometric_dev': ['facial', 'face', 'rostro'],
    'automation': ['robotic process', 'rpa', 'automatizaci', 'intelligent', 'ohjelmistorobot', 'cognitive'],
    'ocr': ['ocr', 'texterkennung', 'reconocimiento', 'intelligent document'],
    'conversational': ['chat', 'bot', 'virtual', 'digital assistant', 'conversation', 'conversaci', 'asistente', 'assistente', 'assistant virtuel', 'sprachassistent', 'asystent', 'чат'],
}

def tag(t, country):
    hits = {}
    tl = t.lower()
    for name, (kind, rx, val) in COMPILED.items():
        pf = PREFILTER.get(name)
        if pf and not any(s in tl for s in pf):
            continue
        for m in rx.finditer(t):
            if val is None or val(t, m, country):
                hits[name] = kind; break
    return hits
