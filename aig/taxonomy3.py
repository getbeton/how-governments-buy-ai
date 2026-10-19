"""The study taxonomy: three separate questions, so the categories do not overlap.
  PURCHASE    what the tender buys (every AI procurement has one)
  CAPABILITY  what the AI does (only when the purchase is AI technology: software, custom build, equipment, managed service, data, pilot)
  AUDIENCE    who the AI serves (end user)
plus deep-dive tags: chatbot audience/channel, cybersecurity type, brand named + steering signals.
Rules are multilingual regexes. First match wins. The title is tried first, then the full text."""
import re
I = re.I
C = lambda rules: [(l, re.compile(r, I)) for l, r in rules]

def first(rules, *texts, default=None):
    for t in texts:
        for label, rx in rules:
            if t and rx.search(t):
                return label
    return default

PURCHASE = C([
    ('Labour: contractors and staff', r'^\s*(\S+\s+)?(prestar|prestaci[oó]n de) (los |sus )?servicios (profesionales|de apoyo|t[eé]cnicos)|apprentic|staff augment|body ?leasing|arbeitnehmerüberlass|労働者派遣|\bpersonnel\b|personal(gestellung)|secondment|interim (manager|resource)|recruit|data scientist\b|\bdeveloper\b|desarrollador|perfil profesional|contratista|expertkonsult|konsultförmedl|asiantuntijapalvelu|人材派遣'),
    ('Training and skills', r'capacita|inscri[cç][aã]o|inscripci[oó]n|treinamento|\bmba\b|p[oó]s-gradua|aperfei[cç]oamento|training|course\b|courses|curso|kurs\b|kurse|schulung|weiterbildung|fortbildung|formaci[oó]n|formação|forma[cç][aã]o|capacitaci|szkoleni|bootcamp|e-?learning|masterclass|diplomado|workshop|lehrgang|mokym|koulutu|utbildning|uddannelse|literacy|upskill|reskill|curriculum|講座|研修|教育\b|ワークショップ|навчанн|обучени'),
    ('Events and communication', r'conference|summit|cumbre|congres|forum\b|foro\b|\bevent|evento|world tour|exhibition|exposici|feira|\bstand\b|campaign|campaña|marketing|travel|viaje|deslocaç|passagem a[ée]rea|sponsorship|patrocin'),
    ('Research, pilots and challenges', r'research|forschung|investigaci[oó]n|investigação|\bi\+d\b|\bi&d\b|\br&d\b|(?<!co)pilot|proof.of.(concept|value)|\bpoc\b|prova de conceito|prueba de concepto|prototyp|innovation (challenge|partnership|procurement)|innovationspartnerschaft|pre-?commercial|\bpcp\b|\bsbri\b|hackathon|challenge\b|feasibility|machbarkeit|study\b|studie\b|estudio\b|estudo\b|étude|調査研究|調査・分析|実証|検証'),
    ('Consulting, strategy and governance', r'consult|advis|beratung|consultor|asesor|assessment|evaluat|evaluaci|avalia|audit\b|auditor|strategy|strateg|roadmap|readiness|governance|gobernanza|ethic|[ée]tica|ai act|compliance|cumplimiento|guidance|expert (support|advice)|projektträger|acompañamiento|技術支援|調査\b|コンサル'),
    ('Compute and AI hardware', r'\bgpu|\bhpc\b|supercomput|superpo[cč][ií]ta|rechenleistung|rechenzentr|data cent|centro de datos|\bserver|serwer|servidor|servrar|cluster|workstation|laptop|notebook|copilot\+ ?pc|ai pc|\bnpu\b|computador|komputer|storage|ai factory|ai gigafactor|nvidia|dgx|accelerator card|サーバ|計算機|スーパーコンピュータ'),
    ('AI-enabled equipment', r'\bmri\b|\bmrt\b|resonancia|resonância|magnetresonanz|rezonans|\bct\b|tomograf|tomogra|ultrasound|ultrason|ecógraf|ecograf|ultraschall|usg\b|endoscop|endoskop|ендоскоп|x-ray|rayos x|röntgen|rentgen|mammogra|angiograf|c-arm|c-bogen|microscop|mikroskop|camera|cámara|câmara|kamer|cctv|videovigil|drone|dron\b|drones|robot\b|robots|robotic (system|platform|surgery)|vehicle|vehículo|veículo|fahrzeug|sensor|scanner|equipo m[eé]dico|equipamento|medical device|dispositivo|ger[aä]t|apparat|aparat|equipment|equipo\b|suministro de equipos|装置|機器|カメラ|ドローン'),
    ('Data services', r'data label|annotation|anotaci|etiquetado de datos|dataset|corpus|data collection|recolecci[oó]n de datos|digiti[sz]ation|digitali[sz]aci|digitaliz|datos abiertos|open data|data cleaning'),
    ('Custom development and integration', r'develop|entwickl|desarrollo|desenvolvimento|développ|implement|implant|wdrożen|integrat|integra[cç]|\bbuild\b|aufbau|einführung|deploy|despliegue|programming|programmier|custom|customi[sz]|erstellung|anpassung|ieviešana|izstrād|kūrim|vývoj|ανάπτυξη|σχεδιασμ|design and|diseño|構築|開発|設計|改修|розробк|створенн'),
    ('Software and licences', r'licen|subscri|suscrip|assinatura|abonnement|lizenz|licencj|licencí|lisen|licenč|renewal|renovaci|renova[cç]|saas|software|softwar|programvar|ohjelmisto|logiciel|aplicativo|oprogramow|g-?cloud|cloud service|platform|plataforma|plattform|plateforme|tool\b|tools|herramienta|ferramenta|narzędzi|solution|lösung|solución|soluç|\bapp\b|application|aplicaci|access to|zugang|nuoma|利用|賃貸借|借上|ライセンス|サービスの提供|ліцензі|програмн'),
    ('Managed and operational services', r'service|servicio|serviço|usług|dienstleist|leistung|support|soporte|mantenimiento|manutenção|maintenance|wartung|betrieb|operation|operaci|monitoring|monitoreo|hosting|managed|outsourc|運用|保守|業務|послуг'),
])
TECH_PURCHASES = {'Compute and AI hardware', 'AI-enabled equipment', 'Data services', 'Custom development and integration', 'Software and licences',
                  'Managed and operational services', 'Research, pilots and challenges', None}

CAPABILITY = C([
    ('Cybersecurity', r'cyber|ciber|kyber|threat|amenaza|bedrohung|\bsoc\b|security operations|siem|\bedr\b|\bxdr\b|\bndr\b|intrusion|malware|ransomware|phishing|darktrace|vectra|sentinelone|crowdstrike|ciberseguran|cybersécurité|cyberbezpiecze|セキュリティ|サイバー|кібер'),
    ('Chatbots and virtual assistants', r'chat ?bot|chatbot|voice ?bot|voicebot|callbot|virtual (assistant|agent)|digital assistant|conversational|asistente (virtual|conversacional|digital)|agente (virtual|conversacional)|assistente (virtual|digital)|assistant virtuel|agent conversationnel|sprachassistent|digitaler assistent|ki-assistent|ai assistant|ai agent|asystent\w* (wirtualn|g[lł]osow|ai|ai)|virtuaaliavust|chattbot|чат-?бот|віртуальн\w* асистент|チャットボット|対話型'),
    ('Generative AI and LLMs', r'copilot|chatgpt|openai|\bgpt|\bllm|large language|language model|sprachmodell|modelos? de lenguaje|modelo de linguagem|modèle de langage|generativ|g[ée]n[ée]rativ|\bgen ?ai\b|claude|mistral|gemini|watsonx|aleph alpha|hugging ?face|\brag\b|retrieval.augmented|foundation model|deepseek|qwen|llama|生成ai|生成ＡＩ|大規模言語|генеративн|мовн\w* модел'),
    ('Speech and transcription', r'speech|voice recogn|spracherkenn|reconocimiento de voz|reconhecimento de voz|reconnaissance vocale|dictation|diktat|transcri|transkri|sanelu|puheentunnist|taligenk|minutes|議事録|文字起こし|音声認識|音声|subtit|untertitel|subtítul|rozpoznawani\w* mowy|розпізнаванн\w* мов'),
    ('Translation and text analysis', r'translat|übersetz|traducc|tradu[cç]|t[lł]umacz|překlad|翻訳|natural language|\bnlp\b|text (analytic|mining|classif)|semantic|sémant|summari|resum|search engine|suchmaschine|wyszukiw|knowledge (base|management)|wissensmanagement|legal (research|ai)|jur[ií]dic|自然言語'),
    ('Computer vision and imaging', r'computer vision|vision artificial|visión artificial|visão computacional|vision par ordinateur|machine vision|bildverarbeitung|bilderkenn|bildanalys|image (recogn|analy|process|classif|segment|detect)|images? (médic|medic)|imaging|imagenolog|bildgeb|imagerie|análisis de imágenes|análise de imagens|analiza obraz|rozpoznawani\w* obraz|video(?! ?confer|konferen|llamada|call)|vídeo(?! ?confer)|cctv|camera|cámara|câmara|kamer|facial|face (recogn|detect)|gesicht|object detection|radiolog|mammogra|patholog|patológ|dermatolog|retin|oftalm|ophthalm|\bpacs\b|dicom|x-ray|röntgen|rentgen|\bct\b|\bmri\b|tomograf|endoscop|endoskop|ultrasound|ultrason|ecograf|satellite|satélite|aerial|drone|dron\b|drones|lidar|inspection|defect|plate recogn|\banpr\b|画像|映像|顔認|відео'),
    ('Documents and process automation', r'document|dokument|akte|expediente|archiv|\bocr\b|intelligent (automation|process|document)|process automation|\brpa\b|automati[sz]|automatisier|automatizaci|classif|klassifi|correspond|e-?mail|posteingang|invoice|factura|faktur|claims|workflow|帳票|書類|文書'),
    ('Prediction, risk and analytics', r'predict|forecast|prognos|predicci|previs|analytic|anal[ií]tica|analys|análisis|analiz|data scien|ciencia de datos|ci[eê]ncia de dados|statist|estad[ií]stic|risk|riesgo|risiko|fraud|betrug|anomal|detect|monitor|optimi[sz]|decision support|entscheidungsunterst|scoring|recommend|matching|demand|需要予測|異常検知|予測|分析|判断'),
    ('Robotics and autonomous systems', r'robot|autonom|unmanned|no tripulad|não tripulad|self-driving|selbstfahr|vehículo autónomo|ロボット|自律|自動運転'),
])

AUDIENCE = C([
    ('Citizens and service users', r'citizen|ciudadan|cidad[aã]|bürger|burger|obywatel|občan|kansalai|medborgar|borger|utente|resident|taxpayer|contribuyente|claimant|beneficiar|applicant|solicitante|job ?seeker|demandante|tourist|turist|visitor|passenger|pasajer|public.facing|front.?office|contact cent|call cent|helpline|hotline|enquir|atenci[oó]n al (ciudadano|p[uú]blico|usuario)|atendimento|customer service|servicio al cliente|bürgerservice|línea 1|línea de atención|ventanilla|whatsapp|住民|国民|市民|相談|громадян'),
    ('Patients and clinicians', r'patient|paciente|patient|pacjent|pacient|potilas|clinic|clínic|klinik|hospital|krankenhaus|szpital|nemocnic|sairaala|ziekenhuis|radiolog|diagnos|medical|médic|medizin|health|salud|saúde|zdrow|zdravot|terveys|nurse|enfermer|pflege|care home|医療|病院|患者|пацієнт|лікар'),
    ('Students and teachers', r'student|estudiante|alumn|pupil|schüler|uczni|žák|opiskelija|\belev(er|erna)?\b|teacher|docente|profesor|lehrer|nauczyciel|učitel|opettaja|school|escuela|escola|schule|szkoł|škol|koulu|classroom|aula\b|学生|児童|教員|学校|студент|учн'),
    ('Police, defence and security staff', r'police|polic[ií]a|polizei|policja|polícia|gendarm|guardia civil|carabin|defen[cs]e|defensa|defesa|bundeswehr|military|militar|army|ejército|navy|armada|air force|border|frontera|grenz|customs|aduana|zoll|intelligence service|forensic|forense|forensisch|prison|penitenci|gefängnis|陸自|海上|航空自衛|防衛|自衛隊|警察|поліці|військ'),
    ('Researchers', r'research|investigaci[oó]n|investigação|forschung|badania|výzkum|tutkimus|forskning|laborator|scientist|científic|wissenschaft|hpc|supercomput|研究'),
    ('Civil servants (internal use)', r'staff|employee|empleado|funcionari|personal\b|mitarbeit|beschäftigte|pracownik|zaměstnan|henkilöst|medarbetar|medarbejder|internal|interno|interne|intern\b|back.?office|case ?work|caseworker|officials|servidores p[uú]blicos|productivity|productividad|productivité|produktivit|copilot|m365|microsoft 365|office 365|minutes|議事録|職員|行政事務|文書作成|працівник'),
    ('Infrastructure and assets', r'traffic|tráfico|verkehr|ruch drogow|road|carretera|straße|rail|ferrovi|bahn|water|agua|wasser|energy|energ[ií]a|energie|grid|electric|building|edificio|gebäude|bridge|puente|brücke|dam\b|ダム|河川|道路|tunnel|port\b|airport|aeropuert|flughafen|asset|infrastructure|infraestructura|infrastruktur|leak|fuga'),
])

CHATBOT_CHANNEL = C([('Phone / voice', r'voice ?bot|voicebot|callbot|phone|telef|tel[eé]fon|call cent|ivr|voz\b|voice|sprach|puhel|電話|音声'),
                     ('WhatsApp / messaging', r'whatsapp|telegram|messenger|viber|sms\b|mensajer'),
                     ('Web / app', r'web|portal|sitio|site|app\b|aplicaci|online|página|homepage|ウェブ|ホームページ'),
                     ('Internal / staff', r'staff|employee|internal|interno|intern\b|mitarbeit|職員|servidores')])

CYBER_TYPE = C([('Threat intelligence and alerting', r'threat (intelligence|notification|correlat|feed|hunting)|amenințări|threat landscape'),
                ('Network detection and response', r'\bndr\b|network detection|darktrace|vectra|intrusion|ids\b|ips\b|traffic analysis|network (security|monitoring)|netzwerk'),
                ('Endpoint protection (EDR/XDR)', r'\bedr\b|\bxdr\b|endpoint|antivirus|anti-virus|sentinelone|crowdstrike|defender'),
                ('SOC / SIEM and managed detection', r'detection (and|&) response|\bsoc\b|security operations|siem|\bmdr\b|managed detection|monitoring|monitoreo|sentinel\b|splunk|qradar'),
                ('Email and phishing protection', r'e-?mail|phishing|spam|correo'),
                ('Identity, fraud and access', r'identity|identidad|fraud|fraude|access|acceso|authentication|autentic|biometr|kyc'),
                ('Vulnerability testing and threat intelligence', r'vulnerab|pentest|penetration|red team|threat intelligence|inteligencia de amenazas|scan\b|assessment|audit'),
                ('Training and awareness', r'training|awareness|capacitaci|formaci|schulung|concienciaci'),
                ('OT / industrial security', r'\bot\b|scada|industrial|ics\b'),
                ('Other / unspecified', r'.')])

BRANDS = C([('OpenAI / ChatGPT', r'chat ?gpt|openai|\bgpt-?\d|\bgpt ?4o|\bgpt (plus|team|enterprise|business|pro)\b|\bo3-mini'),
            ('Microsoft Copilot / Azure OpenAI', r'copilot|azure openai|azure ai\b|microsoft 365 copilot|m365 copilot'),
            ('Google Gemini / Vertex', r'gemini|vertex ai|\bbard\b|google ai (pro|studio)|notebooklm'),
            ('Anthropic Claude', r'anthropic|(?<!jean )(?<!jean-)\bclaude\b(?=.{0,40}(\bai\b|\bia\b|pro\b|team|code|sonnet|opus|haiku|\d\.\d|anthropic|enterprise|max\b|licen|plan))|(chat ?gpt|gemini|perplexity)[^|]{0,40}\bclaude\b|\bclaude\b[^|]{0,40}(chat ?gpt|gemini|perplexity)'),
            ('Mistral', r'mistral ai\b|mistral ?\d|mistral (large|medium|small|le chat|nemo)|\ble chat\b|codestral'),
            ('Aleph Alpha', r'aleph alpha'), ('Meta Llama', r'meta llama|\bll?hama ?\d|\bllama-?\d|\bllama (model|llm)'), ('DeepSeek', r'deepseek'), ('Alibaba Qwen', r'\bqwen'),
            ('IBM watsonx', r'watsonx|ibm watson\b'), ('AWS (Bedrock / SageMaker)', r'amazon bedrock|aws bedrock|sagemaker|amazon q\b'), ('Palantir', r'palantir'),
            ('Nvidia', r'nvidia|\bdgx\b'), ('Darktrace', r'darktrace'), ('Nuance / Dragon', r'nuance|dragon medical'), ('DeepL', r'\bdeepl\b'), ('Perplexity', r'perplexity')])
OR_EQUIVALENT = re.compile(r'or equivalent|or equal|o equivalente|o similar|ou [ée]quivalent|oder gleichwertig|o equivalenti|of gelijkwaardig|lub równoważn|nebo rovnocenn|alebo rovnocenn|vagy azzal egyenérték|tai vastaava|eller likvärdig|eller tilsvarende|ή ισοδύναμ|или еквивалент|або еквівалент|ili jednakovrijedn|ali enakovredn|arba lygiavert|või samaväärne|vai ekvivalent|sau echivalent', I)
EXCLUSIVE = re.compile(r'exclusiv|sole source|single source|proprietary|único proveedor|proveedor exclusivo|alleinstellung|ausschließlichkeit|technical reasons|razones técnicas|technische gründe|protection of exclusive rights|derechos exclusivos|direitos exclusivos|droits exclusifs|ausschließliche rechte', I)

def tag_brands(text):
    return sorted({b for b, rx in BRANDS if rx.search(text or '')})
