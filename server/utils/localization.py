import re

SUPPORTED_LANGUAGES = {"en", "gu", "hi"}

TEXT = {
    "Server is healthy": (
        "સર્વર સારી રીતે ચાલી રહ્યો છે",
        "सर्वर सही तरीके से चल रहा है"
    ),
    "MongoDB connected successfully": (
        "મોંગોડીબી સફળતાપૂર્વક જોડાઈ ગયું છે",
        "मोंगोडीबी सफलतापूर्वक जुड़ गया है"
    ),
    "Please login first": (
        "કૃપા કરીને પહેલાં લૉગિન કરો",
        "कृपया पहले लॉगिन करें"
    ),
    "Please select all fields.": (
        "કૃપા કરીને બધી વિગતો પસંદ કરો.",
        "कृपया सभी जानकारी चुनें।"
    ),
    "General soil care advice": (
        "જમીનની સંભાળ અંગે સામાન્ય સલાહ",
        "मिट्टी की देखभाल की सामान्य सलाह"
    ),
    "Helpful next steps": (
        "ઉપયોગી આગળના પગલાં",
        "अगले उपयोगी कदम"
    ),
    "Low Priority": (
        "ઓછી પ્રાથમિકતા",
        "कम प्राथमिकता"
    ),
    "Medium Priority": (
        "મધ્યમ પ્રાથમિકતા",
        "मध्यम प्राथमिकता"
    ),
    "High Priority": (
        "ઊંચી પ્રાથમિકતા",
        "उच्च प्राथमिकता"
    ),
    "A soil test is the best way to decide the right fertilizer plan for your crop.": (
        "તમારા પાક માટે યોગ્ય ખાતર યોજના નક્કી કરવા માટે જમીન પરીક્ષણ શ્રેષ્ઠ રીત છે.",
        "अपनी फसल के लिए सही उर्वरक योजना तय करने का सबसे अच्छा तरीका मिट्टी परीक्षण है।"
    ),
    "Check soil moisture and drainage.": (
        "જમીનની ભેજ અને પાણી નીકળવાની વ્યવસ્થા તપાસો.",
        "मिट्टी की नमी और जल निकासी जांचें।"
    ),
    "Use compost or organic matter when suitable.": (
        "યોગ્ય હોય ત્યારે કમ્પોસ્ટ અથવા જૈવિક ખાતર વાપરો.",
        "उपयुक्त होने पर कम्पोस्ट या जैविक पदार्थ का उपयोग करें।"
    ),
    "Do not apply fertilizer without local guidance.": (
        "સ્થાનિક સલાહ વિના ખાતર ન વાપરો.",
        "स्थानीय सलाह के बिना उर्वरक का उपयोग न करें।"
    ),
    "Consult an agriculture officer for a crop-specific plan.": (
        "પાક માટે ખાસ યોજના માટે કૃષિ અધિકારીની સલાહ લો.",
        "फसल के लिए विशेष योजना हेतु कृषि अधिकारी से सलाह लें।"
    ),
    "Use a soil test and local agriculture guidance before applying any fertilizer.": (
        "કોઈપણ ખાતર વાપરતા પહેલાં જમીન પરીક્ષણ અને સ્થાનિક કૃષિ સલાહ લો.",
        "कोई भी उर्वरक डालने से पहले मिट्टी परीक्षण और स्थानीय कृषि सलाह लें।"
    ),
    "No saved records found.": (
        "કોઈ સાચવેલો રેકોર્ડ મળ્યો નથી.",
        "कोई सहेजा गया रिकॉर्ड नहीं मिला।"
    ),
    "Failed to fetch": (
        "માહિતી મેળવવામાં સમસ્યા આવી.",
        "जानकारी प्राप्त करने में समस्या आई।"
    )
}

TERMS = {
    "Black": ("કાળી", "काली"),
    "Black soil": ("કાળી જમીન", "काली मिट्टी"),
    "Alluvial": ("કાંપવાળી", "जलोढ़"),
    "Alluvial soil": ("કાંપવાળી જમીન", "जलोढ़ मिट्टी"),
    "Red": ("લાલ", "लाल"),
    "Red soil": ("લાલ જમીન", "लाल मिट्टी"),
    "Loamy": ("દોમી", "दोमट"),
    "Loamy soil": ("દોમી જમીન", "दोमट मिट्टी"),
    "Clay": ("ચીકણી", "चिकनी"),
    "Clay soil": ("ચીકણી જમીન", "चिकनी मिट्टी"),
    "Sandy": ("રેતાળ", "रेतीली"),
    "Sandy soil": ("રેતાળ જમીન", "रेतीली मिट्टी"),

    "Kharif": ("ખરીફ", "खरीफ"),
    "Rabi": ("રવિ", "रबी"),
    "Zaid": ("ઝાયદ", "जायद"),
    "Monsoon": ("ચોમાસું", "मानसून"),
    "Winter": ("શિયાળો", "सर्दी"),
    "Summer": ("ઉનાળો", "गर्मी"),

    "Seedling": ("અંકુર અવસ્થા", "अंकुर अवस्था"),
    "Vegetative": ("વૃદ્ધિ અવસ્થા", "वृद्धि अवस्था"),
    "Flowering": ("ફૂલ આવવાની અવસ્થા", "फूल आने की अवस्था"),
    "Fruiting": ("ફળ આવવાની અવસ્થા", "फल आने की अवस्था"),

    "Dry": ("સૂકી", "सूखी"),
    "Moderate": ("મધ્યમ", "मध्यम"),
    "Wet": ("ભીની", "गीली"),

    "Cotton": ("કપાસ", "कपास"),
    "Soybean": ("સોયાબીન", "सोयाबीन"),
    "Groundnut": ("મગફળી", "मूंगफली"),
    "Rice": ("ચોખા", "धान"),
    "Maize": ("મકાઈ", "मक्का"),
    "Wheat": ("ઘઉં", "गेहूं"),
    "Potato": ("બટાકા", "आलू"),
    "Mustard": ("રાઈ", "सरसों"),
    "Millet": ("બાજરી", "बाजरा"),
    "Pigeon Pea": ("તુવેર", "अरहर"),
    "Tomato": ("ટામેટા", "टमाटर"),
    "Chickpea": ("ચણા", "चना"),
    "Sugarcane": ("શેરડી", "गन्ना"),

    "Brown spots": ("ભૂરા ડાઘ", "भूरे धब्बे"),
    "Yellow leaves": ("પીળા પાંદડા", "पीले पत्ते"),
    "Leaf holes": ("પાંદડામાં છિદ્રો", "पत्तों में छेद"),
    "Wilting leaves": ("કરમાયેલા પાંદડા", "मुरझाए पत्ते"),
    "White powder": ("સફેદ પાવડર", "सफेद पाउडर"),
    "early blight": ("આરંભિક ઝુલસા રોગ", "आरंभिक झुलसा रोग")
}


def normalize_language(language):
    language = (language or "en").strip().lower()
    return language if language in SUPPORTED_LANGUAGES else "en"


def translation_index(language):
    return 0 if language == "gu" else 1


def translate_term(text, language):
    for english, translations in TERMS.items():
        if english.casefold() == text.casefold():
            return translations[translation_index(language)]

    return text


def translate_templates(text, language):
    index = translation_index(language)

    suggested = re.fullmatch(
        r"(?:Suggested|Recommended) crops:\s*(.+)",
        text,
        flags=re.IGNORECASE
    )

    if suggested:
        crops = [
            translate_term(crop.strip(), language)
            for crop in suggested.group(1).split(",")
        ]

        prefix = (
            "ભલામણ કરેલા પાકો: "
            if language == "gu"
            else "सुझाई गई फसलें: "
        )

        return prefix + ", ".join(crops)

    crop_reason = re.fullmatch(
        r"(.+?) soil stores moisture well and is suitable for these (.+?) crops\.",
        text,
        flags=re.IGNORECASE
    )

    if crop_reason:
        soil = translate_term(crop_reason.group(1).strip(), language)
        season = translate_term(crop_reason.group(2).strip(), language)

        if language == "gu":
            return f"{soil} જમીન ભેજ સારી રીતે જાળવે છે અને આ {season} પાકો માટે યોગ્ય છે."

        return f"{soil} मिट्टी नमी अच्छी तरह रखती है और इन {season} फसलों के लिए उपयुक्त है।"

    fertilizer_advice = re.fullmatch(
        r"(.+?) plants at the (.+?) stage need balanced nutrition and stable watering\.",
        text,
        flags=re.IGNORECASE
    )

    if fertilizer_advice:
        crop = translate_term(fertilizer_advice.group(1).strip(), language)
        stage = translate_term(fertilizer_advice.group(2).strip(), language)

        if language == "gu":
            return f"{crop}ના છોડને {stage} તબક્કે સંતુલિત પોષણ અને નિયમિત પાણી જરૂરી છે."

        return f"{crop} के पौधों को {stage} अवस्था में संतुलित पोषण और नियमित पानी की आवश्यकता होती है।"

    irrigation_advice = re.fullmatch(
        r"The (.+?) soil appears (.+?)\. Your (.+?) crop may need irrigation soon\.",
        text,
        flags=re.IGNORECASE
    )

    if irrigation_advice:
        soil = translate_term(irrigation_advice.group(1).strip(), language)
        moisture = translate_term(irrigation_advice.group(2).strip(), language)
        crop = translate_term(irrigation_advice.group(3).strip(), language)

        if language == "gu":
            return f"{soil} જમીન {moisture} લાગે છે. તમારા {crop} પાકને ટૂંક સમયમાં સિંચાઈની જરૂર પડી શકે છે."

        return f"{soil} मिट्टी {moisture} लग रही है। आपकी {crop} फसल को जल्द सिंचाई की आवश्यकता हो सकती है।"

    disease_advice = re.fullmatch(
        r"(.+?) on (.+?) leaves can be a sign of (.+?)\.",
        text,
        flags=re.IGNORECASE
    )

    if disease_advice:
        symptom = translate_term(disease_advice.group(1).strip(), language)
        crop = translate_term(disease_advice.group(2).strip(), language)
        disease = translate_term(disease_advice.group(3).strip(), language)

        if language == "gu":
            return f"{crop}ના પાંદડા પરના {symptom} {disease}નું લક્ષણ હોઈ શકે છે."

        return f"{crop} की पत्तियों पर {symptom} {disease} का संकेत हो सकते हैं।"

    if " · " in text:
        parts = text.split(" · ")
        translated_parts = [translate_text(part, language) for part in parts]

        if translated_parts != parts:
            return " · ".join(translated_parts)

    if "," in text:
        parts = [part.strip() for part in text.split(",")]
        translated_parts = [translate_term(part, language) for part in parts]

        if all(
            translated != original
            for translated, original in zip(translated_parts, parts)
        ):
            return ", ".join(translated_parts)

    return None


def translate_text(text, language):
    if not isinstance(text, str):
        return text

    language = normalize_language(language)

    if language == "en":
        return text

    before = text[: len(text) - len(text.lstrip())]
    after = text[len(text.rstrip()):]
    clean_text = text.strip()

    if not clean_text:
        return text

    if clean_text in TEXT:
        translated = TEXT[clean_text][translation_index(language)]
        return f"{before}{translated}{after}"

    translated_term = translate_term(clean_text, language)

    if translated_term != clean_text:
        return f"{before}{translated_term}{after}"

    translated_template = translate_templates(clean_text, language)

    if translated_template:
        return f"{before}{translated_template}{after}"

    return text


def localize_payload(value, language):
    language = normalize_language(language)

    if isinstance(value, dict):
        return {
            key: localize_payload(item, language)
            for key, item in value.items()
        }

    if isinstance(value, list):
        return [
            localize_payload(item, language)
            for item in value
        ]

    if isinstance(value, str):
        return translate_text(value, language)

    return value