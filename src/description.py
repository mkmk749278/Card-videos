"""Write a ready-to-paste YouTube title/description (with chapters) per language.

Usage: python3 src/description.py hi|te  -> output/youtube-<lang>.md
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

META = {
    "hi": {
        "title": "Credit Card Bill नहीं भरा तो क्या होगा? Day-by-Day सच, RBI Rules, Recovery Agent Harassment से बचाव (Hinglish)",
        "intro": "Credit card bill न भर पाने पर actually क्या होता है — due date से लेकर NPA, write-off और court stage तक, "
                 "day by day। Bank क्या कर सकता है और क्या नहीं, recovery agents कैसे pressure डालते हैं, RBI के rules आपको "
                 "क्या protection देते हैं, complaint कहाँ करें, और settlement सही तरीक़े से कैसे करें।",
        "purpose": "ये video उन लोगों के लिए है जो card rotation और बढ़ते क़र्ज़ में फँस गए हैं और सच में pay करने की हालत में नहीं हैं। "
                   "हम किसी को भी bill न भरने की सलाह नहीं देते — अगर आप pay कर सकते हैं, तो पूरा और समय पर pay कीजिए।",
        "help": "अगर आप क़र्ज़ या recovery के दबाव से बहुत परेशान हैं, तो आप अकेले नहीं हैं। Tele-MANAS (भारत सरकार) mental health helpline: 14416 या 1-800-891-4416 — free, 24×7।",
    },
    "te": {
        "title": "Credit Card Bill కట్టకపోతే ఏం జరుగుతుంది? Day-by-Day నిజం, RBI Rules, Recovery Agent Harassment నుంచి రక్షణ (Telugu)",
        "intro": "Credit card bill కట్టలేకపోతే actually ఏం జరుగుతుంది — due date నుంచి NPA, write-off, court stage వరకు, day by day. "
                 "Bank ఏం చేయగలదు, ఏం చేయలేదు, recovery agents ఎలా pressure పెడతారు, RBI rules మీకు ఇచ్చే protection, "
                 "complaint ఎక్కడ చేయాలి, settlement సరిగ్గా ఎలా చేయాలి.",
        "purpose": "ఈ video card rotation, పెరిగే అప్పుల్లో ఇరుక్కుపోయి, నిజంగా కట్టలేని పరిస్థితిలో ఉన్నవాళ్ళ కోసం. "
                   "Bill కట్టకండి అని మేము ఎవరికీ చెప్పడం లేదు — మీరు కట్టగలిగితే, పూర్తిగా, సమయానికి కట్టండి.",
        "help": "అప్పు లేదా recovery ఒత్తిడితో చాలా బాధపడుతుంటే, మీరు ఒంటరి కాదు. Tele-MANAS (భారత ప్రభుత్వం) mental health helpline: 14416 లేదా 1-800-891-4416 — free, 24×7.",
    },
}

DISCLAIMER = """DISCLAIMER
• This video is for educational and awareness purposes only, to help viewers understand RBI rules and their rights.
• We do NOT encourage anyone to skip or delay credit card payments. Wilful default harms your credit and finances. If you can pay, pay in full and on time.
• This is not legal, financial or professional advice. Every case is different. Consult a qualified advocate or a financial counsellor for your situation.
• We are not affiliated with the Reserve Bank of India, any bank, card issuer or recovery agency. No bank or agency is named or targeted.
• Information is based on publicly available RBI documents as understood in 2026. Rules and bank policies change, so verify at https://www.rbi.org.in
• Example figures (interest growth, credit score) are illustrative only. Actual charges vary by bank and card.
• The creator is not responsible for any decision taken on the basis of this video."""

SOURCES = """OFFICIAL SOURCES
• RBI Master Direction – Credit Card and Debit Card (Issuance and Conduct) Directions, 2022
• RBI circular on conduct of recovery agents (outsourcing of financial services), 12 Aug 2022
• RBI Framework for Compromise Settlements and Technical Write-offs, 8 Jun 2023
• RBI Integrated Ombudsman Scheme, 2021: https://cms.rbi.org.in · Helpline 14448
• Cyber crime reporting: https://cybercrime.gov.in"""

TAGS = ("credit card, credit card default, credit card bill not paid, RBI rules, RBI guidelines recovery agents, "
        "recovery agent harassment, credit card settlement, CIBIL, NPA, loan recovery, RBI ombudsman, debt help, "
        "card rotation, financial awareness")


def ts(sec):
    sec = int(sec)
    return f"{sec // 60}:{sec % 60:02d}" if sec < 3600 else f"{sec // 3600}:{sec % 3600 // 60:02d}:{sec % 60:02d}"


def main(lang):
    tl = json.load(open(f"{ROOT}/build/{lang}/timeline.json", encoding="utf-8"))
    chapters = [(0, "Disclaimer")]
    for s in tl["scenes"]:
        if s["id"] == "intro":
            chapters.append((s["start"], "Introduction & why this video"))
        elif s["type"] == "chapter":
            chapters.append((s["start"], f"{s['num']}. {s['title']}"))
        elif s["id"] == "disclaimer":
            chapters.append((s["start"], "Disclaimer & where to get help"))
    m = META[lang]
    body = "\n\n".join([
        m["intro"], m["purpose"],
        "CHAPTERS\n" + "\n".join(f"{ts(t)} {name}" for t, name in chapters),
        "🆘 " + m["help"], DISCLAIMER, SOURCES,
    ])
    os.makedirs(f"{ROOT}/output", exist_ok=True)
    out = f"{ROOT}/output/youtube-{lang}.md"
    with open(out, "w", encoding="utf-8") as f:
        f.write(f"# YouTube upload — {'Hinglish' if lang == 'hi' else 'Telugu'}\n\n")
        f.write(f"## Title\n\n{m['title']}\n\n## Description (paste as-is)\n\n```\n{body}\n```\n\n")
        f.write(f"## Tags\n\n{TAGS}\n\n")
        f.write("## Upload settings\n\n- Audience: **No, it's not made for kids**\n"
                "- Category: **Education**\n- Altered or synthetic content: **Yes** (AI-generated narration voice)\n"
                "- Captions are burned in; you can also upload subtitles later\n")
    print(out)


if __name__ == "__main__":
    main(sys.argv[1])
