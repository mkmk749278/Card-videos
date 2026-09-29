"""Source of truth for the add-on clips. Writes content/addons/<id>/scenes.json
and narration.<lang>.json. Run: python3 content/addons/build_addons.py
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
STYLES_CLEAR = ["rules", "table", "compare", "checklist", "stack"]
END = {"id": "end", "type": "addonend"}


def dlg(id, topic, icon):
    return {"id": id, "type": "dialogue", "topic": topic, "icon": icon}


A = {}

# ---------------------------------------------------------------- A1
A["a1-multiple-cards"] = {
 "scenes": [
  {"id": "title", "type": "addon", "part": 1, "title": "Many Cards, Many Banks — How to Handle Them", "sub": "One total debt, or separate? Which to settle first? A worked example.", "icon": "credit-card"},
  dlg("dlg", "\"I have 5 cards in 4 banks — is it one big debt?\"", "credit-card"),
  {"id": "rules", "type": "rules", "heading": "How banks actually see it", "icon": "classical-building", "badge": "", "source": "Each card is its own account and its own contract", "items": [
    "Each card = a separate account, separate dues, separate settlement",
    "Different banks never combine — each bank settles only its own dues",
    "Same bank, many cards or loans: ask for ONE letter covering all of them",
    "One default is reported to CIBIL — every lender sees it",
    "Other banks may cut your limits or close your cards"], "cue": [1, 2, 3, 4, 4]},
  {"id": "example", "type": "table", "heading": "Example: 5 cards, 4 banks, ₹5.2 lakh total", "note": "Illustrative. Numbers are principal (what was actually spent).",
   "cols": ["Bank", "Cards", "Principal", "How it closes"], "rows": [
    ["Bank A", "2 cards", "₹1,80,000", "ONE settlement letter for both"],
    ["Bank B", "1 card", "₹1,40,000", "Its own settlement"],
    ["Bank C", "1 card", "₹1,00,000", "Its own settlement"],
    ["Bank D", "1 card", "₹1,00,000", "Its own settlement"]], "cue": [1, 2, 2, 2], "tag": "Not one ₹5.2L debt — four separate negotiations", "tagCue": 3},
  {"id": "priority", "type": "table", "heading": "What to protect & settle first", "note": "General order — your own situation decides.",
   "cols": ["Order", "What"], "rows": [
    ["1st — protect", "Loans / EMIs with auto-debit or cheque (bounce = criminal risk)"],
    ["2nd — protect", "The bank that holds your salary / savings account (set-off risk)"],
    ["Then settle", "The bank giving the best written offer — close it fully"],
    ["Then", "Next bank — one at a time, each with its own letter"]], "cue": [1, 2, 3, 4]},
  {"id": "tips", "type": "bullets", "heading": "Mistakes to avoid", "icon": "warning", "tone": "amber", "items": [
    {"icon": "coin", "text": "Paying ₹1,000 here and there to every bank — closes nothing"},
    {"icon": "memo", "text": "Keep one sheet: bank, card's last 4 digits, principal, offer, status"},
    {"icon": "page-facing-up", "text": "Every settled card: its own letter + NOC + CIBIL check"},
    {"icon": "counterclockwise-arrows-button", "text": "Never use one card to settle another"}], "cue": [1, 2, 3, 4]},
  END],
 "te": {
  "title": ["చాలా cards, చాలా banks ఉన్నప్పుడు ఏం చేయాలి? ఈ add-on లో చూద్దాం."],
  "dlg": [
   {"q": "అన్నా, నాకు ఐదు cards ఉన్నాయి, నాలుగు banks లో. మొత్తం కలిపి ఒకటే పెద్ద అప్పా? అన్నీ ఒకేసారి settle చేయాలా?", "style": "fear"},
   "లేదు. ఇది చాలామంది తప్పుగా అనుకునే విషయం. Clear గా చూద్దాం."],
  "rules": [
   "Bank దృష్టిలో ఎలా ఉంటుందో చూడండి.",
   "ప్రతి card ఒక separate account. వేరు బాకీ, వేరు settlement.",
   "వేరు వేరు banks ఎప్పుడూ కలవవు. ప్రతి bank తన బాకీ మాత్రమే settle చేస్తుంది.",
   "ఒకే bank లో రెండు మూడు cards గానీ, loans గానీ ఉంటే, అన్నిటికీ కలిపి ఒకే settlement letter అడగండి.",
   "ఒక్క default అయినా CIBIL లో అందరికీ కనిపిస్తుంది. వేరే banks కూడా మీ limits తగ్గించొచ్చు, cards close చేయొచ్చు."],
  "example": [
   "ఒక example. ఐదు cards, నాలుగు banks, మొత్తం principal ఐదు లక్షల ఇరవై వేలు.",
   "Bank A లో రెండు cards, లక్షా ఎనభై వేలు. దానికి రెండు cards కలిపి ఒకే letter.",
   "Bank B, C, D — ఒక్కొక్కటి వేరే settlement.",
   "అంటే ఇది ఐదు లక్షల ఒకే అప్పు కాదు. నాలుగు వేరు వేరు negotiations."],
  "priority": [
   "ఇప్పుడు ముందు ఏది కాపాడుకోవాలి, ఏది settle చేయాలి.",
   "మొదట, auto-debit లేదా cheque ఉన్న loans, EMIs. అవి bounce అయితే criminal risk.",
   "రెండోది, మీ salary లేదా savings account ఉన్న bank. అక్కడ set-off risk ఉంటుంది.",
   "తర్వాత, ఏ bank మంచి written offer ఇస్తే, దాన్ని పూర్తిగా close చేయండి.",
   "తర్వాత ఇంకో bank. ఒక్కొక్కటిగా, ప్రతిదానికీ సొంత letter తో."],
  "tips": [
   "కొన్ని తప్పులు చేయకండి.",
   "అన్ని banks కి కొంచెం కొంచెం, వెయ్యి రెండు వేలు కట్టడం — దానివల్ల ఏదీ close అవ్వదు.",
   "ఒక sheet పెట్టుకోండి. Bank, card చివరి నాలుగు అంకెలు, principal, offer, status.",
   "Settle అయిన ప్రతి card కి, సొంత letter, NOC, CIBIL check.",
   "ఒక card తో ఇంకో card ని settle చేయడం — ఎప్పుడూ వద్దు."],
  "end": ["పూర్తి వివరాల కోసం, మా main video చూడండి. ఒత్తిడిగా ఉంటే, Tele-MANAS ఒకటి నాలుగు నాలుగు ఒకటి ఆరు కి call చేయండి."]}}

# ---------------------------------------------------------------- A2
A["a2-20-lakh-auction"] = {
 "scenes": [
  {"id": "title", "type": "addon", "part": 2, "title": "₹20 Lakh & ₹25 Lakh — DRT, Auction, Wilful Defaulter", "sub": "When can property really be auctioned? What the numbers mean.", "icon": "classical-building"},
  dlg("dlg", "\"They say they'll auction my property…\"", "house"),
  {"id": "drt", "type": "rules", "heading": "The ₹20 lakh line — DRT", "icon": "balance-scale", "badge": "", "source": "Recovery of Debts and Bankruptcy Act, 1993 — Sec 1(4)", "items": [
    "Debts Recovery Tribunal (DRT) handles only dues of ₹20 lakh or more",
    "Counted per bank — NOT your total across all banks",
    "Below ₹20 lakh: civil court, arbitration or Lok Adalat",
    "Property can be attached / auctioned only after a decree or recovery certificate",
    "An agent can never auction or seize anything"], "cue": [1, 2, 3, 4, 4]},
  {"id": "sarf", "type": "compare", "heading": "Auction: secured vs unsecured", "left": {"title": "SARFAESI auction", "icon": "house", "color": "amber", "items": ["Only for SECURED loans (home, property)", "Bank gives 60-day notice, then can take possession", "Needs a registered charge on the asset"]},
   "right": {"title": "Credit card", "icon": "credit-card", "color": "green", "items": ["UNSECURED — SARFAESI does not apply", "Bank must first win a case (court / DRT)", "Only then can any property be attached"]}, "cue": [0, 1]},
  {"id": "examples", "type": "table", "heading": "Examples", "note": "DRT is only a forum — even there, you get notice and a chance to defend.",
   "cols": ["Situation", "DRT possible?"], "rows": [
    ["5 cards in 5 banks, ₹12 lakh total", "No — every bank is below ₹20 lakh"],
    ["One bank: ₹8L card + ₹14L personal loan", "Possible — ₹22 lakh with one bank"],
    ["One card, ₹3 lakh", "No — civil court / arbitration route"]], "cue": [1, 2, 3]},
  {"id": "wilful", "type": "rules", "heading": "The ₹25 lakh line — 'wilful defaulter'", "source": "RBI Master Direction on Wilful Defaulters, 2024", "items": [
    "Applies only when ₹25 lakh or more is outstanding",
    "AND the default is wilful — could pay but didn't, or misused the money",
    "Genuine hardship (job loss, illness) is not wilful default",
    "Keep proof of hardship; deal honestly and in writing"], "cue": [1, 2, 3, 4]},
  END],
 "te": {
  "title": ["ఇరవై లక్షలు, ఇరవై ఐదు లక్షలు — ఈ రెండు numbers వెనక ఉన్న నిజం చూద్దాం."],
  "dlg": [
   {"q": "అన్నా, మీ property auction చేస్తాం అని agent అంటున్నాడు. నిజంగా చేయగలరా?", "style": "fear"},
   "Auction అనే మాట వినగానే భయం వేస్తుంది. కానీ దాని వెనక కొన్ని clear rules ఉన్నాయి."],
  "drt": [
   "ముందుగా ఇరవై లక్షల line.",
   "Debts Recovery Tribunal, అంటే DRT — ఇది ఒక bank కి ఇరవై లక్షలు లేదా అంతకంటే ఎక్కువ బాకీ ఉంటేనే.",
   "ఇది ప్రతి bank కి విడిగా లెక్క. మీ అన్ని banks మొత్తం కాదు.",
   "ఇరవై లక్షల లోపు అయితే, civil court, arbitration, లేదా Lok Adalat మాత్రమే.",
   "ఏ property అయినా attach చేయాలన్నా, auction చేయాలన్నా, ముందు decree గానీ recovery certificate గానీ రావాలి. Agent ఎప్పుడూ ఏదీ auction చేయలేడు."],
  "sarf": [
   "SARFAESI auction అనేది secured loans కి మాత్రమే. Home loan లాంటివి. అక్కడ అరవై రోజుల notice తర్వాత bank possession తీసుకోగలదు.",
   "Credit card unsecured. దానికి SARFAESI వర్తించదు. Bank ముందు case గెలవాలి. ఆ తర్వాతే ఏదైనా."],
  "examples": [
   "కొన్ని examples.",
   "ఐదు banks లో ఐదు cards, మొత్తం పన్నెండు లక్షలు. DRT కుదరదు. ఏ bank కూడా ఇరవై లక్షలు దాటలేదు.",
   "ఒకే bank లో ఎనిమిది లక్షల card, పద్నాలుగు లక్షల personal loan. అది ఇరవై రెండు లక్షలు, DRT అవకాశం ఉంది.",
   "ఒక card, మూడు లక్షలు. DRT కాదు, civil court లేదా arbitration route."],
  "wilful": [
   "ఇక ఇరవై ఐదు లక్షల line. Wilful defaulter tag.",
   "ఇది ఇరవై ఐదు లక్షలు లేదా అంతకంటే ఎక్కువ బాకీ ఉన్నప్పుడే.",
   "అది కూడా, కట్టే శక్తి ఉండి కావాలని కట్టకపోతే, లేదా డబ్బు దుర్వినియోగం చేస్తే.",
   "Job పోవడం, అనారోగ్యం లాంటి నిజమైన ఇబ్బంది, wilful default కాదు.",
   "మీ ఇబ్బందికి proof ఉంచుకోండి. అన్నీ నిజాయితీగా, written గా."],
  "end": ["పూర్తి వివరాల కోసం, main video చూడండి. ఒత్తిడిగా ఉంటే, Tele-MANAS ఒకటి నాలుగు నాలుగు ఒకటి ఆరు కి call చేయండి."]}}

# ---------------------------------------------------------------- A3
A["a3-lok-adalat"] = {
 "scenes": [
  {"id": "title", "type": "addon", "part": 3, "title": "Lok Adalat Notice — The Real Picture", "sub": "Is attending compulsory? What happens if you don't go? How to use it well.", "icon": "balance-scale"},
  dlg("dlg", "\"I got a Lok Adalat notice — will they arrest me if I don't go?\"", "page-facing-up"),
  {"id": "rules", "type": "rules", "heading": "What Lok Adalat really is", "icon": "balance-scale", "badge": "", "source": "Legal Services Authorities Act, 1987", "items": [
    "A settlement meeting — not a regular court case",
    "Attending is voluntary — no arrest, no fine for not going",
    "No award without YOUR consent — both sides must agree",
    "If you skip, the bank may later file a regular case",
    "If you agree, the award is final — there is no appeal"], "cue": [1, 2, 3, 4, 5]},
  {"id": "go", "type": "compare", "heading": "Go, or skip?", "left": {"title": "Worth going if…", "icon": "handshake", "color": "green", "items": ["You can arrange some money now", "You want to close the account", "Offers here are often lower"]},
   "right": {"title": "It's okay to skip if…", "icon": "hourglass-not-done", "color": "amber", "items": ["You have no money right now", "You don't want to sign under pressure", "Send a written reply to the bank instead"]}, "cue": [1, 2]},
  {"id": "carry", "type": "checklist", "heading": "If you go — checklist", "items": [
    "Carry ID proof, the notice and your statements",
    "Know your principal — negotiate from it",
    "Ask for instalments if you can't pay at once",
    "Read the award: amount, dates, 'full and final'",
    "Get a certified copy of the award",
    "Pay only to the bank's official account"], "cue": [1, 2, 3, 4, 5, 5]},
  END],
 "te": {
  "title": ["Lok Adalat notice వస్తే ఏం చేయాలి? నిజమైన picture చూద్దాం."],
  "dlg": [
   {"q": "అన్నా, Lok Adalat notice వచ్చింది. వెళ్ళకపోతే arrest చేస్తారా?", "style": "fear"},
   "అస్సలు కాదు. Lok Adalat గురించి చాలా అపోహలు ఉన్నాయి. నిజం ఇది."],
  "rules": [
   "Lok Adalat అంటే ఏంటో చూడండి.",
   "ఇది ఒక settlement meeting. Regular court case కాదు.",
   "వెళ్ళడం మీ ఇష్టం. వెళ్ళకపోతే arrest లేదు, fine లేదు.",
   "మీ అంగీకారం లేకుండా award రాదు. రెండు వైపులా ఒప్పుకుంటేనే.",
   "మీరు వెళ్ళకపోతే, bank తర్వాత regular case వేసే అవకాశం ఉంది.",
   "మీరు ఒప్పుకుంటే మాత్రం, ఆ award final. Appeal ఉండదు."],
  "go": [
   "ఎప్పుడు వెళ్ళడం మంచిది?",
   "ఇప్పుడు కొంత డబ్బు ఏర్పాటు చేయగలిగితే, account close చేయాలనుకుంటే, వెళ్ళండి. అక్కడ offers తరచుగా తక్కువగా ఉంటాయి.",
   "డబ్బు అస్సలు లేకపోతే, ఒత్తిడిలో sign చేయడం ఇష్టం లేకపోతే, వెళ్ళకపోయినా పర్లేదు. Bank కి written reply పంపండి."],
  "carry": [
   "వెళ్తే, ఈ checklist.",
   "ID proof, notice, మీ statements తీసుకెళ్ళండి.",
   "మీ principal ఎంతో తెలుసుకోండి. దాని నుంచే negotiate చేయండి.",
   "ఒకేసారి కట్టలేకపోతే installments అడగండి.",
   "Award లో amount, dates, full and final అని ఉందో చదవండి.",
   "Award certified copy తీసుకోండి. Payment bank official account కి మాత్రమే."],
  "end": ["పూర్తి వివరాల కోసం, main video చూడండి. ఒత్తిడిగా ఉంటే, Tele-MANAS ఒకటి నాలుగు నాలుగు ఒకటి ఆరు కి call చేయండి."]}}

# ---------------------------------------------------------------- A4
A["a4-notices"] = {
 "scenes": [
  {"id": "title", "type": "addon", "part": 4, "title": "Notices Decoded — Which One Is Serious?", "sub": "WhatsApp 'notice', lawyer's notice, arbitration, court summons, cheque bounce.", "icon": "page-facing-up"},
  {"id": "table", "type": "table", "heading": "Five kinds of 'notice'", "note": "When in doubt, show it to an advocate or your nearest free Legal Services Authority.",
   "cols": ["Notice", "Who sends it", "Seriousness", "What to do"], "rows": [
    ["WhatsApp 'legal notice' PDF", "Agent", "Pressure", "Screenshot, don't panic, complain"],
    ["Advocate's legal notice", "Bank's lawyer", "Not a case yet", "Reply in writing"],
    ["Arbitration notice", "Arbitrator / bank", "Serious", "Respond, raise objections"],
    ["Court summons", "Court", "Must respond", "Appear or send an advocate"]], "cue": [1, 2, 3, 4]},
  {"id": "cheque", "type": "rules", "heading": "Cheque bounce / NACH notice", "icon": "page-facing-up", "badge": "", "source": "NI Act Sec 138 · PSS Act Sec 25", "items": [
    "Comes only if a cheque or bank auto-debit you gave has bounced",
    "This one is criminal — you get 15 days after the notice",
    "Pay or reply within the time; meet an advocate immediately"], "cue": [1, 2, 3]},
  {"id": "arb", "type": "rules", "heading": "Arbitration — know this", "icon": "balance-scale", "badge": "", "source": "Arbitration & Conciliation Act · Supreme Court, Perkins Eastman (2019)", "items": [
    "An arbitration award can be enforced like a court decree",
    "An arbitrator appointed by one side alone is not valid",
    "Reply in writing and raise your objection early",
    "Ignoring it can lead to an award in your absence"], "cue": [1, 2, 3, 4]},
  {"id": "verify", "type": "bullets", "heading": "Is it genuine? Check", "icon": "magnifying-glass-tilted-left", "tone": "teal", "items": [
    {"icon": "classical-building", "text": "Court summons: court name, case number, seal & signature"},
    {"icon": "globe-with-meridians", "text": "Check the case number on eCourts: services.ecourts.gov.in"},
    {"icon": "page-facing-up", "text": "Lawyer's notice: letterhead with enrolment number & address"},
    {"icon": "balance-scale", "text": "Free legal help: your District Legal Services Authority"}], "cue": [1, 2, 3, 4]},
  END],
 "te": {
  "title": ["Notice వచ్చిన ప్రతిసారీ భయపడాల్సిన అవసరం లేదు. ఏది serious, ఏది కాదో చూద్దాం."],
  "table": [
   "ఐదు రకాల notices ఉంటాయి.",
   "WhatsApp లో వచ్చే legal notice PDF — ఇది agent పంపే pressure. Screenshot తీసుకోండి, భయపడకండి, complaint చేయండి.",
   "Advocate పంపే legal notice — ఇది ఇంకా case కాదు. Written గా reply ఇవ్వండి.",
   "Arbitration notice — ఇది serious. Respond అవ్వండి, మీ objections చెప్పండి.",
   "Court summons — దీనికి తప్పకుండా respond అవ్వాలి. మీరు వెళ్ళండి, లేదా advocate ని పంపండి."],
  "cheque": [
   "ఇంకొకటి — cheque bounce, లేదా NACH notice.",
   "మీరు ఇచ్చిన cheque గానీ, bank auto-debit గానీ bounce అయితేనే ఇది వస్తుంది.",
   "ఇది criminal. Notice వచ్చిన తర్వాత పదిహేను రోజుల సమయం ఉంటుంది.",
   "ఆ సమయంలోనే కట్టండి, లేదా reply ఇవ్వండి. వెంటనే advocate ని కలవండి."],
  "arb": [
   "Arbitration గురించి ఇవి తెలుసుకోండి.",
   "Arbitration award ని court decree లాగానే enforce చేయొచ్చు.",
   "కానీ ఒక వైపు మాత్రమే arbitrator ని నియమిస్తే, అది చెల్లదు అని Supreme Court చెప్పింది.",
   "Written గా reply ఇవ్వండి, మీ objection మొదట్లోనే చెప్పండి.",
   "Ignore చేస్తే, మీరు లేకుండానే award రావొచ్చు."],
  "verify": [
   "Notice నిజమైనదో కాదో ఎలా check చేయాలి?",
   "Court summons లో court పేరు, case number, seal, sign ఉంటాయి.",
   "ఆ case number ని eCourts website లో check చేయొచ్చు.",
   "Advocate notice అయితే, letterhead మీద enrolment number, address ఉంటాయి.",
   "Free legal help కోసం, మీ District Legal Services Authority ని కలవండి."],
  "end": ["పూర్తి వివరాల కోసం, main video చూడండి. ఒత్తిడిగా ఉంటే, Tele-MANAS ఒకటి నాలుగు నాలుగు ఒకటి ఆరు కి call చేయండి."]}}

# ---------------------------------------------------------------- A5
A["a5-principal"] = {
 "scenes": [
  {"id": "title", "type": "addon", "part": 5, "title": "Calculate Your Real Principal — in 4 Steps", "sub": "Your strongest number in any settlement talk.", "icon": "abacus"},
  {"id": "steps", "type": "plan", "heading": "4 steps", "steps": [
    "Download all statements since the card was opened (or last 2–3 years)",
    "Add up every purchase and cash withdrawal",
    "Subtract every payment and refund you made",
    "What's left = your principal (no interest, fees or GST)"], "cue": [1, 2, 3, 4]},
  {"id": "stack", "type": "table", "heading": "Example", "note": "Illustrative numbers.",
   "cols": ["From your statements", "Amount"], "rows": [
    ["Purchases + cash withdrawals", "₹2,60,000"],
    ["Payments + refunds", "− ₹1,75,000"],
    ["Your principal", "₹85,000"]], "cue": [1, 2, 3], "tag": "Negotiate from ₹85,000 — not from their total", "tagCue": 3},
  {"id": "tips", "type": "bullets", "heading": "Tips", "icon": "light-bulb", "tone": "teal", "items": [
    {"icon": "e-mail", "text": "Missing statements? Ask the bank by e-mail — they must give them"},
    {"icon": "memo", "text": "Keep the calculation on one page — show it in every negotiation"},
    {"icon": "handshake", "text": "Open with a number near your principal, not their total"}], "cue": [1, 2, 3]},
  END],
 "te": {
  "title": ["Settlement లో మీ బలమైన number — మీ principal. దాన్ని ఎలా లెక్కపెట్టాలో చూద్దాం."],
  "steps": [
   "నాలుగు steps.",
   "ఒకటి, card తీసుకున్నప్పటి నుంచి, లేదా కనీసం రెండు మూడు సంవత్సరాల statements download చేయండి.",
   "రెండు, మీరు చేసిన ప్రతి purchase, cash withdrawal కలపండి.",
   "మూడు, మీరు కట్టిన ప్రతి payment, refund తీసేయండి.",
   "మిగిలింది మీ principal. ఇందులో interest, fees, GST ఏవీ ఉండవు."],
  "stack": [
   "ఒక example చూడండి.",
   "Purchases, cash కలిపి రెండు లక్షల అరవై వేలు.",
   "మీరు కట్టింది, refunds కలిపి లక్షా డెబ్బై ఐదు వేలు.",
   "అంటే మీ principal ఎనభై ఐదు వేలు మాత్రమే. Bank ఎంత చూపించినా, మీ లెక్క ఇదే."],
  "tips": [
   "కొన్ని tips.",
   "Statements లేకపోతే, email లో bank ని అడగండి. ఇవ్వాల్సిందే.",
   "మీ లెక్కని ఒక page లో రాసి పెట్టుకోండి. ప్రతి negotiation లో చూపించండి.",
   "మొదటి offer, వాళ్ళ total దగ్గర కాదు, మీ principal దగ్గర మొదలుపెట్టండి."],
  "end": ["పూర్తి వివరాల కోసం, main video చూడండి. ఒత్తిడిగా ఉంటే, Tele-MANAS ఒకటి నాలుగు నాలుగు ఒకటి ఆరు కి call చేయండి."]}}

# ---------------------------------------------------------------- A6
A["a6-more-answers"] = {
 "scenes": [
  {"id": "title", "type": "addon", "part": 6, "title": "12 More Questions People Ask", "sub": "ARC, other accounts, references, recording calls, jobs, passport, CIBIL errors…", "icon": "thinking-face"},
  {"id": "faq", "type": "faq", "pairs": [
    ["My debt was sold to an ARC — now what?", "Same debt, new owner — RBI rules still apply. Ask for the assignment letter; settle only with them, in writing."],
    ["Can they debit my account in another bank?", "Only if you gave a mandate (NACH / standing instruction). Cancel old mandates."],
    ["They're calling my friends and references!", "They may try to trace you, but must not reveal your debt or harass them. Complain."],
    ["Can I record recovery calls?", "Recording your own calls as evidence is generally fine. Keep them safe."],
    ["Will calls stop after I settle?", "They should. If calls continue after the NOC, complain to the bank and RBI."],
    ["Can default affect my job?", "Some employers (banks, finance) check credit reports. Otherwise, usually not."],
    ["Passport or visa problems?", "Card default alone doesn't affect your passport. Look-out circulars are for serious fraud or huge cases."],
    ["My card had 'credit shield' insurance?", "Check it — it may cover death, disability or job loss."],
    ["Should I take a personal loan to pay cards?", "Only if the rate is much lower, EMI is affordable, and you stop using cards. Never app loans."],
    ["Can I convert my card dues into EMI?", "Yes — ask BEFORE default. It's much cheaper than revolving."],
    ["CIBIL still wrong after settlement?", "Dispute with CIBIL & the bank. Not fixed in 30 days → ₹100/day compensation (RBI)."],
    ["Can I settle while my card is still regular?", "Usually no — ask for an EMI plan or restructuring instead."]]},
  END],
 "te": {
  "title": ["ఇంకా మీరు అడిగే పన్నెండు ప్రశ్నలు. Quick గా చూద్దాం."],
  "faq": [
   "మొదలుపెడదాం.",
   {"q": "నా అప్పుని ARC కి అమ్మేశారు. ఇప్పుడు ఏంటి?"},
   "అదే అప్పు, కొత్త owner అంతే. RBI rules అలాగే వర్తిస్తాయి. Assignment letter అడగండి. వాళ్ళతోనే, written గా settle చేయండి.",
   {"q": "వేరే bank లో ఉన్న నా account నుంచి డబ్బు కట్ చేయగలరా?"},
   "మీరు mandate ఇచ్చి ఉంటేనే. NACH, standing instruction లాంటివి. పాత mandates cancel చేయండి.",
   {"q": "నా friends కి, references కి calls చేస్తున్నారు!", "style": "anger"},
   "మిమ్మల్ని వెతకడానికి ప్రయత్నించొచ్చు. కానీ మీ అప్పు గురించి చెప్పకూడదు, వాళ్ళని వేధించకూడదు. Complaint చేయండి.",
   {"q": "Recovery calls record చేయొచ్చా?"},
   "మీ సొంత calls ని సాక్ష్యం కోసం record చేయడం సాధారణంగా పర్లేదు. జాగ్రత్తగా దాచుకోండి.",
   {"q": "Settle చేశాక calls ఆగిపోతాయా?"},
   "ఆగాలి. NOC వచ్చాక కూడా calls వస్తే, bank కి, RBI కి complaint చేయండి.",
   {"q": "Default వల్ల నా job మీద effect ఉంటుందా?"},
   "Banks, finance లాంటి కొన్ని companies credit report చూస్తాయి. మిగతా చోట్ల సాధారణంగా ఉండదు.",
   {"q": "Passport, visa సమస్యలు వస్తాయా?"},
   "కేవలం card default వల్ల passport మీద effect ఉండదు. Look-out circulars పెద్ద fraud cases కి మాత్రమే.",
   {"q": "నా card కి credit shield insurance ఉంది."},
   "Check చేయండి. మరణం, అంగవైకల్యం, job పోవడం లాంటివి cover అవ్వొచ్చు.",
   {"q": "Cards కట్టడానికి personal loan తీసుకోవచ్చా?"},
   "Interest చాలా తక్కువగా ఉంటే, EMI కట్టగలిగితే, cards వాడటం ఆపేస్తేనే. App loans మాత్రం ఎప్పుడూ వద్దు.",
   {"q": "Card బాకీని EMI గా మార్చుకోవచ్చా?"},
   "అవును. కానీ default అవ్వకముందే అడగండి. Revolving కంటే చాలా తక్కువ ఖర్చు.",
   {"q": "Settle చేశాక కూడా CIBIL లో తప్పుగా ఉంది."},
   "CIBIL కి, bank కి dispute పెట్టండి. ముప్పై రోజుల్లో సరిచేయకపోతే, RBI rule ప్రకారం రోజుకి వంద రూపాయల compensation.",
   {"q": "Card ఇంకా regular గా ఉన్నప్పుడే settle చేయొచ్చా?"},
   "సాధారణంగా కాదు. దానికి బదులు EMI plan గానీ, restructuring గానీ అడగండి."],
  "end": ["పూర్తి వివరాల కోసం, main video చూడండి. ఒత్తిడిగా ఉంటే, Tele-MANAS ఒకటి నాలుగు నాలుగు ఒకటి ఆరు కి call చేయండి."]}}


def main():
    for pid, d in A.items():
        od = os.path.join(HERE, pid)
        os.makedirs(od, exist_ok=True)
        json.dump(d["scenes"], open(f"{od}/scenes.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        for lang, lname in (("te", "Telugu"), ("hi", "Hindi")):
            if lang not in d:
                continue
            styles = {s["id"]: "clear" for s in d["scenes"] if s["type"] in STYLES_CLEAR}
            n = {"_engine": "svara", "_fx": "A", "_lang": lname, "_styles": styles, **d[lang]}
            json.dump(n, open(f"{od}/narration.{lang}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(pid, len(d["scenes"]), "scenes")


if __name__ == "__main__":
    main()
