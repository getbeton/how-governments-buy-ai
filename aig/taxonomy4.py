"""Use cases inside each AI capability, the context of cybersecurity tenders, fiscal-year ends (study rules).
Rules read the title and the text around the AI mention (ai_window), never the whole notice. First match wins."""
import re
I = re.I
R = lambda rules: [(l, re.compile(r, I)) for l, r in rules]

USE_CASES = {
    'Computer vision and imaging': R([
        ('Medical imaging and diagnosis', r'radiolog|teleradiolog|mammogra|tomogra|\bct\b|\bmri\b|\bmrt\b|resonanc|rezonans|x-ray|röntgen|rentgen|ultrasound|ultrason|ecograf|ultrasonograf|endoscop|endoskop|patholog|patológ|dermatolog|retin|oftalm|ophthalm|\bpacs\b|dicom|bildgeb|imagerie m|lung|cancer|screening|stroke|udar|diagnos|clinic|klinik|hospital|szpital|spital|nemocnic|画像診断'),
        ('Face recognition and biometrics', r'facial|face recogn|face detect|reconocimiento facial|reconhecimento facial|reconnaissance faciale|rostro|gesicht|twarz|biometr|顔認'),
        ('Video surveillance and public safety', r'cctv|surveillance|vigilancia|videovigil|vigilância|videoüberwach|videoschutz|monitoring kamer|kamer|cámara|câmara|camera|\bnvr\b|\bdvr\b|video ?anal|videoanal|\\bpolice|polic[ií]a|polícia|polizei|policj|security|seguridad|segurança|sicherheit|bezpiecze|監視|防犯'),
        ('Roads, traffic and transport', r'road|carretera|straße|strasse|drog|traffic|tráfico|tránsito|verkehr|ruch drog|pavement|pavimento|condition survey|highway|autopista|vehic|vehíc|parking|estacionam|plate|matrícul|kennzeichen|rail|ferrov|bahn|airport|aeropuert|port\b|道路|交通'),
        ('Earth observation and drones', r'satellite|satélite|satelit|aerial|aérea|luftbild|drone|dron|\buav\b|orthophoto|ortofoto|lidar|teledetec|remote sensing|earth observation|copernicus|衛星|ドローン|航空写真'),
        ('Infrastructure and industrial inspection', r'inspection|inspección|inspeç|inspekt|defect|defekt|sewer|kanal|pipe|tuber|bridge|puente|brücke|most\b|crack|fissur|tunnel|asset|weld|schweiß|ダム|点検'),
        ('Laboratory and research imaging', r'microscop|mikroskop|spectro|laborator|cell|célula|zell|research|investiga|forsch|scientif|研究'),
        ('Environment, agriculture and wildlife', r'wildlife|fauna|crop|cultivo|agricult|forest|bosque|wald|fire|incendio|waldbrand|plant|cosecha|fish|pesca|environment|ambiental|umwelt|森林|農'),
    ]),
    'Speech and transcription': R([
        ('Clinical dictation and notes', r'dictat|diktat|dictée|dictáfono|dictafone|dragon medical|ambient scrib|speech to summary|clinic|klinik|krankenhaus|hospital|szpital|arzt|médic|medic|health board|nhs|khzg|kis\b|orbis|pacs|radiolog|patient'),
        ('Courts, police and investigations', r'court|tribunal|gericht|judicial|judici|justi|\\bpolice|polic[ií]a|polícia|polizei|policj|interrogat|vernehm|fiscal[ií]a|prosecut|sąd'),
        ('Meetings, councils and parliaments', r'minutes|議事録|会議録|protokoll|stenogra|parliament|parlament|seim|council meeting|plenar|session|sitzung|acta|actas|assembl|gremi|meeting'),
        ('Emergency and contact-centre calls', r'call cent|contact cent|\bivr\b|notruf|emergency|\b112\b|\b911\b|通報|telephone|telefon|switchboard|centralita|atendimento telef|disposition|dispatch|leitstelle'),
        ('Subtitles, captions and accessibility', r'subtit|caption|legenda|untertitel|subtítul|sous-titr|sign language|vélotypie|velotyp|accessib|impaired|hearing|deaf|sordo|surdo'),
        ('Caseworkers and social care', r'social work|social care|caseworker|case worker|magic notes|assessment|care act|children.s services|sozialarbeit'),
        ('Translation and interpreting', r'translat|interpret|traduc|tradu|übersetz|dolmetsch|tłumacz|翻訳|通訳'),
    ]),
    'Generative AI and LLMs': R([
        ('Office assistants for staff (licences)', r'chat ?gpt|copilot|gemini|claude|perplexity|microsoft 365|\bm365\b|office 365|team plan|teams? de|plus\b|enterprise licen|licen|lizenz|licenc|subscri|suscrip|assinatura|abonament|abonnement|ライセンス|利用'),
        ('Citizen-facing assistants', r'citizen|ciudadan|cidad|bürger|obywatel|vecin|whatsapp|atención al|atendimento|customer|cliente|público|public-facing|residents|usuari|住民|国民'),
        ('Document drafting and knowledge search', r'\brag\b|retrieval|knowledge|conocimiento|wissen|document|dokument|documento|search|búsqueda|busca|suche|wyszukiw|legal|jurídic|juridic|law\b|drafting|redac|minutes|summar|resum|archiv|文書|検索'),
        ('Software development and code', r'\bcode\b|coding|codigo|código|transpil|github|programming|programaci|programmier|developer|desarrollador|software engineer|devops'),
        ('Compute and hosting for generative AI', r'\bgpu|server|servidor|serwer|hosting|inference|inferenz|cloud|nube|platform|plataforma|plattform|sovereign|souverän|soberan|on-prem|local|lokal|infrastruct|infraestructura|サーバ|基盤'),
        ('Studies, pilots and evaluation', r'study|studie|estudio|estudo|étude|research|investigaci|forschung|調査|研究|pilot|piloto|proof|evaluat|evaluaci|assessment|impact|survey|encuesta|sbir|r&d'),
        ('Teaching and students', r'student|estudiant|alumn|school|escuela|escola|schule|szkoł|teacher|docente|profesor|lehrer|educa|universit'),
    ]),
    'Prediction, risk and analytics': R([
        ('Health risk and diagnostics', r'patient|paciente|clinic|clínic|hospital|szpital|diagnos|ecg|ekg|genom|\bdna\b|cancer|cáncer|health|salud|saúde|zdrow|medic|médic|disease|enfermedad|epidem|児童'),
        ('Infrastructure, energy and water', r'grid|energy|energ|power|electric|water|agua|wasser|woda|leak|fuga|predictive maintenance|maintenance|mantenimiento predict|asset|bridge|road|carretera|pipeline|port\b|dredg|rail|bahn|transport|traffic|tráfico|verkehr|building|edific'),
        ('Fraud, tax and audit', r'fraud|fraude|betrug|tax|fiscal|tribut|impuest|steuer|audit|auditor|anomal|compliance|money laundering|blanqueo|customs|aduana|zoll|benefit fraud'),
        ('Weather, climate and disasters', r'weather|clima|climate|flood|inundaci|hochwasser|starkregen|drought|sequía|wildfire|incendio|early warning|alerta temprana|frühwarn|forecast|pronóstico|prognose|meteo|disaster|desastre|katastroph'),
        ('Public safety, defence and intelligence', r'\\bpolice|polic[ií]a|polícia|polizei|policj|crime|delito|kriminal|defen[cs]|military|militar|army|navy|air force|intelligence service|osint|threat|missile|warfare|border|frontera|grenz'),
        ('Social services and education', r'child|niñ|kinder|social|welfare|bienestar|benefit|employment|empleo|job ?seeker|student|school|escuela|educa'),
        ('Dashboards and data platforms', r'dashboard|business intelligence|power ?bi|big data|data platform|plataforma de datos|datenplattform|data lake|data warehouse|\bbi\b|analytics platform|observatorio|observatório|indicator|indicador'),
        ('Research and science', r'research|investigaci|investigação|forschung|laborator|scientif|científic|wissenschaft|sbir|r&d|i\+d|研究'),
    ]),
    'Chatbots and virtual assistants': R([
        ('Health bookings and patient helplines', r'patient|paciente|pacjent|hospital|szpital|clinic|klinik|health|salud|saúde|zdrow|rejestrac|cita m[eé]dica|consulta m[eé]dica|appointment|e-rejestr|\\bnhs\\b'),
        ('Utilities and transport customers', r'water|agua|wasser|woda|energ|electricity|electricidad|\\bgas\\b|transport|tránsito|\\bbus\\b|metro|rail|ferrov|billing|facturaci|abonent|абонент|водопост'),
        ('Students and universities', r'student|estudiant|alumn|universit|school|escuela|escola|schule|admission|matrícul|campus'),
        ('Staff helpdesk and internal assistants', r'staff|employee|empleado|funcionari|mitarbeit|pracownik|internal|interno|interne|\\bintern\\b|helpdesk|help desk|service desk|\\bhr\\b|recursos humanos|intranet|power virtual agents'),
        ('Tourism, culture and visitors', r'touris|turis|visitor|visitante|museum|museo|museu|culture|cultura|heritage|gastronom'),
        ('Courts, police and elections', r'justi|court|tribunal|\\bpolice|polic[ií]a|polícia|polizei|policj|\\belecci|\\belection|eleitor|electoral|\\bwahl'),
        ('Tax, benefits and permits', r'\\btax|impuest|tribut|steuer|benefit|subsid|permit|trámite|tramite|registro civil|passport|pasaporte'),
        ('Contact-centre platforms (voice and chat)', r'contact cent|call ?cent|centro de contacto|central de atendimento|kõnekeskus|centralita|atendimento telef|voicebot|callbot|\\bivr\\b|omnichannel|omnicanal|multicanal|multichannel'),
        ('General citizen information', r'citizen|ciudadan|cidad|bürger|obywatel|vecin|municip|ayuntamiento|alcald|prefeitura|câmara|council|gemeinde|gmina|\\bcity|ciudad|público|whatsapp|portal|sitio web|website|atendimento|atención al|customer|cliente'),
        ('Assistant features in office software', r'ai assistant|asistente de ia|assistente de ia|ki-assistent|articulate|adobe|acrobat|copilot'),
        ('Chatbot licences, user not named', r'licen|subscri|suscrip|assinatura|renova|abonament'),
    ]),
}

CYBER_CONTEXT = R([
    ('Defence and national security', r'defen[cs]|military|militar|army|navy|air force|armed forces|sił zbrojnych|cyberprzestrzeni|bundeswehr|ministry of defence|ministerstwo obrony|threat analysis|nation-state|intelligence (agency|service)|national security|seguridad nacional|seguran[cç]a nacional|polic[eíj]a?|gendarm'),
    ('Hospital digitalisation package', r'hospital|szpital|spital|krankenhaus|klinik|clinic|nemocnic|health|salud|saúde|zdrow|medic|opieki zdrowotnej|zoz\b|dokumentacji medycznej|P1\b|nhs'),
    ('University labs and cyber research', r'universit|uniwersytet|politechni|hochschule|laborator|research|investigaci|forsch|cercet|scientif|sbir|r&d|i\+d|course|curso|formaci|training|kurs|szkoleni'),
    ('Networks, servers and firewalls', r'network|sieć|sieci|red de|redes|netzwerk|firewall|utm\b|server|serwer|servidor|infrastruct|infrastruktur|infraestructura|data ?cent|centrum danych|backup|kopi\w* bezpiecze|storage|switch|router|connectivity'),
    ('Office software suites with security features', r'microsoft|m365|office 365|licen|lizenz|licencj|software|oprogramowani|suite|antivirus|antywirus|endpoint|e-?mail'),
    ('Digital public services platforms', r'e-?usług|e-?servic|e-?government|portal|platform|plataforma|platforma|digital services|servicios digitales|usług cyfrowych|transformacj\w* cyfrow|smart city|municip|gmina|urząd'),
])

# Last month of the central-government fiscal year (official finance ministries / budget laws).
FY_END = {
    'united-states': 9,                                   # federal year 1 Oct - 30 Sep
    'united-kingdom': 3, 'japan': 3, 'canada': 3, 'singapore': 3, 'south-africa': 3, 'iran': 3,
    'australia': 6, 'new-zealand': 6, 'kenya': 6, 'tanzania': 6, 'uganda': 6, 'rwanda': 6, 'egypt': 6, 'pakistan': 6,
}   # every other country in the data: 12 (calendar year; Liberia moved to the calendar year in 2024)
FY_LABEL = {12: 'Budget year ends 31 December', 3: 'Budget year ends 31 March', 6: 'Budget year ends 30 June', 9: 'Budget year ends 30 September'}

def fy_end(country):
    return FY_END.get(country, 12)

# When the text names no use, the buyer branch decides (a clinic that buys speech recognition buys clinical dictation).
BRANCH_FALLBACK = {
    'Computer vision and imaging': {'Health': 'Medical imaging and diagnosis', 'Police, justice and home affairs': 'Video surveillance and public safety',
                                    'Defence': 'Video surveillance and public safety', 'Transport': 'Roads, traffic and transport',
                                    'Research and science': 'Laboratory and research imaging', 'Education and universities': 'Laboratory and research imaging',
                                    'Environment, energy and utilities': 'Environment, agriculture and wildlife', 'Agriculture and food': 'Environment, agriculture and wildlife'},
    'Speech and transcription': {'Health': 'Clinical dictation and notes', 'Police, justice and home affairs': 'Courts, police and investigations',
                                 'Head of government, parliament and cabinet': 'Meetings, councils and parliaments'},
    'Prediction, risk and analytics': {'Health': 'Health risk and diagnostics', 'Environment, energy and utilities': 'Infrastructure, energy and water', 'Transport': 'Infrastructure, energy and water',
                                       'Defence': 'Public safety, defence and intelligence', 'Police, justice and home affairs': 'Public safety, defence and intelligence',
                                       'Tax, finance and customs': 'Fraud, tax and audit', 'Social security and employment': 'Social services and education',
                                       'Research and science': 'Research and science', 'Education and universities': 'Research and science'},
    'Chatbots and virtual assistants': {'Health': 'Health bookings and patient helplines', 'Environment, energy and utilities': 'Utilities and transport customers',
                                        'Transport': 'Utilities and transport customers', 'Education and universities': 'Students and universities',
                                        'Police, justice and home affairs': 'Courts, police and elections', 'Tax, finance and customs': 'Tax, benefits and permits',
                                        'Social security and employment': 'Tax, benefits and permits', 'Local and regional government (general)': 'General citizen information',
                                        'Central government (general)': 'General citizen information', 'Culture, media and sport': 'Tourism, culture and visitors'},
    'Generative AI and LLMs': {'Education and universities': 'Teaching and students', 'Research and science': 'Studies, pilots and evaluation'},
}
