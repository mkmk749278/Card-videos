"""English (Indian English) full video = main video + the six deep-dive add-ons,
each inserted where it belongs. Writes content/english/scenes.json and
narration.en.json. Run: python3 content/english/build_english.py
"""
import copy, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "content", "addons"))
from build_addons import A  # noqa: E402

MAIN = json.load(open(os.path.join(ROOT, "content", "scenes.json"), encoding="utf-8"))

# which add-on goes after which main scene
INSERT_AFTER = {"afternpa": ["a5-principal"], "settletips": ["a1-multiple-cards", "a3-lok-adalat"],
                "heirs": ["a2-20-lakh-auction"], "scripts": ["a4-notices"], "faq": ["a6-more-answers"]}
PREFIX = {"a1-multiple-cards": "a1", "a2-20-lakh-auction": "a2", "a3-lok-adalat": "a3",
          "a4-notices": "a4", "a5-principal": "a5", "a6-more-answers": "a6"}

EN = {
 # ------------------------------------------------------------------ main
 "cold": [
  {"q": "Bro, I have not paid my credit card bill for three months, yaar. Every day calls are coming. They are saying police will come tomorrow. I am really scared.", "style": "fear"},
  "Arre, wait, wait. First take a deep breath, okay? You are not alone. Lakhs of people are in the same situation only.",
  "In this video, we will see what actually happens, what the bank can do and cannot do, and how to settle properly. Everything, start to end, no tension."],
 "opendisc": [
  "Before we start, one important thing.",
  "This video is only for awareness. To understand RBI rules and your rights, that's it.",
  "We are not telling anybody to skip their bill. If you can pay, please pay in full and on time. That is always the cheapest way.",
  "This video is for people who genuinely cannot pay right now."],
 "intro": [
  "So, credit card bill not paid. What actually happens after that?",
  "What can the bank do? How do recovery agents put pressure? And what protection do RBI rules give you?",
  "Let's see one by one. Calmly, with facts."],
 "why": [
  "Why are we making this video, you ask?",
  "See, many people pay one card using another card, and they get stuck in this rotation. Every month, the debt keeps growing.",
  "Then default comes, recovery calls come, threats come... and the person starts feeling totally alone and helpless.",
  {"t": "Some people, under this pressure, even think of ending their life. This should not happen.", "style": "sad"},
  "Remember one thing. Debt is a money problem, and money problems have solutions. Your life is priceless.",
  "If you are feeling very stressed, call the government's Tele-MANAS helpline, one four four one six. It's free, any time."],
 "agenda": [
  "Today we will cover ten things.",
  "Secured versus unsecured loans, the interest trap, the day by day timeline, and the truth behind the amount the bank shows.",
  "How much settlement discount is possible, what happens to your property and family, the bank's limits, agents, and RBI rules.",
  "And finally, quick answers to your questions, plus an action plan. Watch till the end, okay?"],
 "sec_dlg": [
  {"q": "Bro, is a credit card loan like a home loan only? If I don't pay, will they take my house?", "style": "fear"},
  "Very good question. If you understand this one difference, half your fear will go. See."],
 "secured": [
  "Loans are of two types. Secured, and unsecured.",
  "Secured means you have given some asset as security. For a home loan, the house. For a gold loan, the gold. For a car loan, the vehicle.",
  "So if you don't pay a secured loan, the bank can take that asset. For big loans, even without going to court, under the SARFAESI law.",
  "Credit card, personal loan, app loans, all these are unsecured. You have not pledged anything. They gave it on your word only.",
  "So for unsecured debt, the bank cannot directly take your house or land. First they have to go to court and win the case. That is a long process."],
 "rates": [
  "Now, interest. Credit card is the most expensive loan you can take.",
  "Most cards charge around three and a half to three point seven five percent per month. That means forty two to forty five percent per year!",
  "And on top of that, eighteen percent GST on the interest and on every fee."],
 "mad": [
  "Your statement shows two amounts. Total Amount Due, and Minimum Amount Due.",
  "If you pay only the minimum, there is no late fee and the account stays regular. But, the interest keeps running on the full balance.",
  "One more trap. Until you pay the full bill, even new purchases don't get the interest-free period. Interest starts from the day you buy."],
 "growth": [
  "See this example. One lakh rupees pending, and nothing paid for one full year.",
  "Interest, late fees and GST together... it becomes almost one lakh eighty thousand.",
  "That means, without spending even one new rupee, the debt has almost doubled."],
 "rotation": [
  "Now, card rotation. Paying one card's bill with another card.",
  "Every time, one to three percent goes as fees. The debt does not reduce, it just shifts from one card to another. That's all.",
  "And taking money from loan apps to pay your card is even more dangerous. Higher interest, and much worse harassment."],
 "t0": [
  "Okay, now the timeline. The due date has passed. What next?",
  "As per RBI rules, if you pay within three days after the due date, the bank cannot charge a late fee, and cannot report you as past due to CIBIL.",
  "Interest may still come. Reminder messages will start."],
 "t1": [
  "From the fourth day, late fee starts. Depending on the bill, from one hundred up to thirteen hundred rupees or more, plus GST.",
  "Interest on the full balance, and reminder calls from the bank.",
  "The bank sends data every month, so your credit report starts showing DPD, days past due. Your score starts falling."],
 "t2": [
  "After one month, the second due date is also missed.",
  "Now the bank's collection team calls many times a day. In most cases, the card gets blocked.",
  "Thirty plus DPD on your report. The score drops fast."],
 "t3": [
  "After sixty days, the account goes into SMA two. That is the stage just before NPA.",
  "Here, the case is often handed over to an outside recovery agency.",
  "Final reminder letters, WhatsApp messages, and sometimes home visits also start."],
 "t4": [
  "Once ninety days cross, the account becomes NPA. Non Performing Asset.",
  "The card is permanently blocked. And this default can show on your credit report for up to seven years.",
  "Interesting thing is, from exactly here, settlement offers start coming."],
 "t5": [
  "Around six months, many banks write off the account in their books.",
  "But write off does not mean waiver! The bank does not give up its right to recover.",
  "At this stage, a legal notice, Lok Adalat notice, or arbitration notice can come. And settlement discounts can also be bigger."],
 "t6": [
  "The bank can also file a recovery suit in civil court. For small amounts, this is rare.",
  "Law gives three years' limitation for recovery. But even a small part payment, or accepting the debt in writing, restarts that clock.",
  "Most important. If a court summons comes, never ignore it. Otherwise the decision can come without you."],
 "shows_dlg": [
  {"q": "Bro, I spent only one lakh. But the statement is showing one lakh eighty thousand. How?", "style": "surprise"},
  "This is exactly what most people don't understand. Let's open up that amount and see what is inside."],
 "stack": [
  "Look at the bank's total in four pieces.",
  "First is principal. That means what you actually spent, minus what you have paid. Here, one lakh.",
  "Everything else got added on top. Interest on interest, late fee every month, and GST on all of it. That is the eighty thousand.",
  "So when you talk settlement, start from your principal, not from their total. Calculate your principal yourself from old statements."],
 "afternpa": [
  "Even after NPA, their system keeps adding interest and charges. The statement keeps growing.",
  "Even after write off, that is only in the bank's books. Their claim on you remains.",
  "Agents will always quote the inflated total. Even in court, the bank usually claims with interest.",
  "But settlement is a negotiation. And there, your strength is simple. Know your principal."],
 "set_dlg": [
  {"q": "Okay bro, how much will they reduce in settlement? When do we get the maximum discount?"},
  "Everybody asks this. I will tell you honestly."],
 "norule": [
  "First, one fact. RBI has not fixed any settlement percentage.",
  "Every bank has its own board approved policy. That is what RBI's two thousand twenty three framework says.",
  "The discount depends on how old the default is, how big the amount is, and how genuine your hardship is.",
  "However much an agent promises, he has no power to approve. Anything final must come on the bank's letterhead."],
 "stages": [
  "Let's see the ranges commonly seen in the market. These are not rules, just experience.",
  "Before ninety days, mostly they waive late fees and some interest. Or they give an EMI plan.",
  "From ninety days up to one year, around twenty to thirty five percent off the total.",
  "Between one and three years, around forty to sixty five percent off.",
  "After three years, sometimes even seventy to ninety percent. But till then, the case risk and the CIBIL damage remain."],
 "amounts": [
  "Now with amounts. Roughly, after one year.",
  "Say you spent ten thousand. Because of fees, the bank may show around thirty thousand. Settlement usually between eleven and eighteen thousand. For such a small amount, a court case almost never comes.",
  "Twenty thousand spent? They may show around forty seven thousand. Settlement, seventeen to twenty eight thousand.",
  "One lakh? Around one lakh eighty thousand shown. Settlement from sixty three thousand to one lakh eight thousand. Here, a legal notice or Lok Adalat can come.",
  "Two lakhs? Around three lakh forty thousand shown. Settlement from one lakh twenty thousand to two lakh six thousand. At this size, arbitration or a case is more likely.",
  "Simple rule to remember. After about one year, the target is to settle near your principal, or below it."],
 "settletips": [
  "Some negotiation tips.",
  "Never accept the first offer. It is always on the higher side.",
  "One time lump sum gets the best discount. Two to six instalments are also possible, but the discount is smaller.",
  "Lok Adalat notice? Don't panic. It is free, the settlement is only with your consent, and the award there is final.",
  "Whatever the offer, ask for it in writing, from the bank's official email."],
 "prop_dlg": [
  {"q": "Bro, I have a small piece of land in my name. My parents' house is also there. Will they take these?", "style": "fear"},
  "This question doesn't let many people sleep. Let me explain one by one."],
 "property": [
  "Card debt is unsecured. So see what happens to what.",
  "Your wife's, parents', or brothers' property, nobody can touch it. Unless they signed as a co-borrower or guarantor.",
  "Joint property? Only your share. That too, only after a court decree.",
  "Land or property in your name? Only if the bank goes to court, wins, gets a decree, and files for execution. The one house you live in usually gets protection under law.",
  "Salary? Only a part, after a court order. The law protects the rest.",
  "Bank accounts? In other banks, they need a court order. In the same bank, set-off is possible."],
 "heirs": [
  "Some more doubts about family.",
  "If the cardholder passes away, the heirs are responsible only up to what they inherit. Not from their own pocket.",
  "Add-on card? The responsibility is the primary cardholder's.",
  "One big warning. Never pledge land or gold to pay a card. If you do, unsecured debt becomes secured debt."],
 "cancant": [
  "Now clearly, what the bank can do, and what it cannot.",
  "The bank can charge interest and fees, report to CIBIL, call you between eight in the morning and seven in the evening, send an authorised agent, and go to court.",
  "If your savings account is in the same bank, they can adjust from it. This is called set-off.",
  "But the bank cannot get you arrested. Cannot take property without a court order. Cannot threaten you. And cannot tell your relatives or office about your debt."],
 "civil": [
  "Biggest truth. Not being able to pay a credit card bill is not a crime. It is a civil matter.",
  "A criminal case comes only in three situations. A cheque you gave bounces, a NACH auto debit from your bank account bounces, or there was fraud from day one.",
  "So if you have given a cheque or auto debit for the card, be careful about that."],
 "tactics": [
  "Now, recovery agents. This is where the real fear starts, no?",
  "Nonstop calls from different numbers. Calls to family, friends, office. Fake legal notices on WhatsApp. Threats like police will come tomorrow.",
  "Some pretend to be advocates, police, or court officers. Some come in groups to the house or office to shame you.",
  "Remember. Most of these are completely against RBI rules."],
 "chat": [
  "You must have also got messages like these.",
  "Legal action in twenty four hours. Arrest warrant issued. Team will come to your home and office tomorrow. Your photo will go to all contacts.",
  "All these are pressure tactics. The only aim is, you get scared and pay something today itself."],
 "myths": [
  "Myth one. Police will arrest you. Truth. Just for not paying a bill, there is no police case.",
  "Myth two. Arrest warrant is issued. Truth. Only a court issues warrants. Before that, a proper summons comes, not on WhatsApp.",
  "Myth three. We will seize your house today. Truth. An agent has no such power. Only with a court decree.",
  "Myth four. We will stop your salary. Truth. Only with a court order, and that too only a part. An agent cannot come to your office and shame you.",
  "Myth five. Pay something now and the case will close. Truth. A small payment closes nothing. Pay only into the bank's official account, with a written plan."],
 "rbiagents": [
  "Now let's see what RBI actually says.",
  "As per RBI's circular of twelve August, two thousand twenty two, recovery calls cannot be made before eight in the morning or after seven in the evening.",
  "Threats, abuse, public humiliation, intruding on the privacy of your family and friends, all are prohibited.",
  "Anonymous calls, wrong messages on social media, and telling lies are also prohibited.",
  "And most important. The bank is responsible for every mistake its agent makes."],
 "rbicards": [
  "For credit cards, RBI has a separate Master Direction. The two thousand twenty two one.",
  "For three days after the due date, no late fee, and no past due reporting.",
  "No interest on unpaid fees and charges. And no over limit charges without your consent.",
  "The minimum amount due must not make the debt keep growing forever.",
  "And after settlement, the bank must update CIBIL within thirty days."],
 "ladder": [
  "If there is harassment, this is the path to complain.",
  "One. Written complaint to the bank's customer care. Take the complaint number.",
  "Two. No reply? Email the bank's Grievance or Principal Nodal Officer.",
  "Three. No reply in thirty days, or the reply is not okay? File a free complaint with the RBI Ombudsman at cms dot rbi dot org dot in. Helpline, one four four four eight.",
  "Threats, abuse, or morphed photos? Go straight to the police, or complain on cybercrime dot gov dot in."],
 "evidence": [
  "For any complaint, the real power is evidence.",
  "Screenshot every message. Note the date, time and number of every call. If possible, record the calls.",
  "If an agent comes home, ask for his ID card and the bank's authorisation letter.",
  "Talk to the bank only on email. Everything should be in writing."],
 "scripts": [
  "Now some ready-made lines you can use.",
  "When an agent calls: please send everything in writing to my registered email. I will reply there.",
  "If they call your relative, the relative should say: telling someone's loan to others is against RBI rules. This call is being recorded. Don't call again.",
  "At your door: show your ID and the bank's authorisation letter. I will deal with the bank in writing. You can leave now.",
  "Stay calm. Don't argue. And never get into any fight."],
 "faq": [
  "Now, the questions you ask the most. Quick answers.",
  {"q": "Will I have to go to jail?", "style": "fear"},
  "No. Not for just not paying a bill. Only a cheque bounce, NACH bounce, or fraud is criminal.",
  {"q": "Will they freeze my bank accounts?"},
  "In other banks, not without a court order. In the same bank, set-off is possible.",
  {"q": "Will they call my office?"},
  "They cannot tell your employer or colleagues about your debt. If they do, it's a complaint.",
  {"q": "After seven years, does the debt disappear?"},
  "No. The history on your credit report fades, but the bank's claim and the case risk don't just vanish.",
  {"q": "Can I pay a settlement in instalments?"},
  "Many times, yes. Two to six parts. But take the letter first.",
  {"q": "Will my home loan or other EMIs be affected?"},
  "If you keep paying them, they continue normally. New loans will be difficult, that's all.",
  {"q": "Can I travel abroad?"},
  "Card default alone does not stop travel. But never ignore a court summons.",
  {"q": "Can the agent take my bike or phone?", "style": "fear"},
  "No. An agent has no right to take anything.",
  {"q": "After settlement, will they ask again?"},
  "Not if you have a proper full and final letter and an NOC.",
  {"q": "Should I pay in full, or settle?"},
  "If you can, pay in full. A Closed status is much better than Settled.",
  {"q": "Will I ever get a card again?", "style": "happy"},
  "Yes. After some time with a clean record, start small. For example, with a secured card."],
 "plan": [
  "Now the most important part. The plan.",
  "One. Stop using the card and stop the rotation, right now.",
  "Two. Make a list of every debt. How much pending, minimum due, due date, interest rate.",
  "Three. Essentials first. Rent, food, medicines, and EMIs with auto debit or cheques.",
  "Four. As early as possible, email the bank and ask for EMI conversion or restructuring.",
  "Five. Explain your hardship honestly, in writing.",
  "Six. Plan to collect a lump sum for settlement.",
  "And seven. Never take a new loan from loan apps to pay a card."],
 "compare": [
  "Before ninety days, options like EMI conversion and restructuring are there. The score also gets less damaged.",
  "After NPA, you may pay less in settlement, but CIBIL shows Settled. New loans become hard for years.",
  "So choose carefully, based on your situation."],
 "settle": [
  "Settle wrongly, and you lose the money and the debt also stays. So listen carefully.",
  "Negotiate on the principal, with the bank, in writing.",
  "Before paying anything, get the settlement letter on the bank's letterhead. It must clearly mention the amount, account number, and full and final settlement.",
  "Pay only to the bank's official account or official link. Never to an agent's personal UPI, never in cash.",
  "Then take the No Dues Certificate. And after thirty to forty five days, definitely check your CIBIL report."],
 "settled": [
  "Settled and Closed are not the same.",
  "Settled means you did not pay in full. Lenders see it as negative.",
  "Later, if you have money, you can pay the rest and get the status changed to Closed.",
  "With on time payments and low usage, the score slowly comes back."],
 "cautions": [
  "Finally, some cautions.",
  "Never ignore a court summons. Lok Adalat is voluntary, but it's often your cheapest chance to settle.",
  "Never give OTP, card details, or Aadhaar to any caller. Frauds also happen in the name of recovery.",
  "Be careful of companies that ask for big fees upfront in the name of settlement.",
  "Never sign any paper without reading it.",
  "If your card dues are in the same bank where your salary or savings are, understand the set-off risk."],
 "outro": [
  "The summary. Credit card default is not a crime. But ignoring it is also not a solution.",
  "Talk to the bank before ninety days. Keep everything in writing.",
  "If there is harassment, don't be afraid. RBI rules are on your side.",
  "Always settle only with a letter. And please share this video with someone who needs it."],
 "disclaimer": [
  "And finally, the disclaimer.",
  "This video is only for awareness. We never advise wilful default. This is not legal or financial advice, and we are not connected to RBI, any bank, or any agency.",
  "The information is based on RBI's public documents. Rules can change, so verify on rbi dot org dot in. For your own case, take advice from a qualified advocate.",
  "However big the problem, you are not alone. Please ask for help."],
 # ------------------------------------------------------------------ add-ons
 "a1_title": ["Now, deep dive. Many cards, many banks. How to handle?"],
 "a1_dlg": [
  {"q": "Bro, I have five cards in four banks. Is it all one big debt? Should I settle everything at once?", "style": "fear"},
  "No. This is something many people get wrong. Let's see clearly."],
 "a1_rules": [
  "See how the bank looks at it.",
  "Every card is a separate account. Separate dues, separate settlement.",
  "Different banks never combine. Each bank settles only its own dues.",
  "If you have two or three cards or loans in the same bank, ask for one settlement letter covering all of them.",
  "Even one default shows on CIBIL to everybody. Other banks may also cut your limits or close your cards."],
 "a1_example": [
  "Example. Five cards, four banks, total principal five lakh twenty thousand.",
  "Bank A has two cards, one lakh eighty thousand. For that, one letter covering both cards.",
  "Banks B, C and D, each one a separate settlement.",
  "So this is not one debt of five lakhs. It is four separate negotiations."],
 "a1_priority": [
  "Now, what to protect first, and what to settle first.",
  "First, loans and EMIs with auto debit or cheques. If they bounce, there is criminal risk.",
  "Second, the bank where your salary or savings account is. There, set-off risk is there.",
  "Then, whichever bank gives a good written offer, close that one fully.",
  "Then the next bank. One by one, each with its own letter."],
 "a1_tips": [
  "Some mistakes to avoid.",
  "Paying a thousand here, two thousand there, to every bank. Nothing closes that way.",
  "Keep one sheet. Bank, last four digits of the card, principal, offer, status.",
  "For every settled card, its own letter, NOC, and a CIBIL check.",
  "Settling one card using another card. Never."],
 "a2_title": ["Twenty lakhs and twenty five lakhs. Let's see the truth behind these two numbers."],
 "a2_dlg": [
  {"q": "Bro, the agent is saying they will auction my property. Can they really do that?", "style": "fear"},
  "The word auction itself scares people. But there are clear rules behind it."],
 "a2_drt": [
  "First, the twenty lakh line.",
  "The Debts Recovery Tribunal, DRT, is only when one bank is owed twenty lakhs or more.",
  "It is counted separately for each bank. Not the total of all your banks.",
  "Below twenty lakhs, it is only civil court, arbitration, or Lok Adalat.",
  "To attach or auction any property, first a decree or recovery certificate must come. An agent can never auction anything."],
 "a2_sarf": [
  "SARFAESI auction is only for secured loans, like a home loan. There, after a sixty day notice, the bank can take possession.",
  "Credit card is unsecured. SARFAESI doesn't apply. The bank must first win a case. Only after that, anything."],
 "a2_examples": [
  "Some examples.",
  "Five cards in five banks, twelve lakhs total. No DRT. No single bank crossed twenty lakhs.",
  "In one bank, an eight lakh card and a fourteen lakh personal loan. That's twenty two lakhs, so DRT is possible.",
  "One card, three lakhs. Not DRT. Civil court or arbitration route."],
 "a2_wilful": [
  "Now the twenty five lakh line. The wilful defaulter tag.",
  "This applies only when twenty five lakhs or more is outstanding.",
  "And only if you had the capacity to pay but deliberately didn't, or misused the money.",
  "Genuine hardship, like losing a job or illness, is not wilful default.",
  "Keep proof of your hardship. Deal honestly, and in writing."],
 "a3_title": ["Lok Adalat notice. What to do? Let's see the real picture."],
 "a3_dlg": [
  {"q": "Bro, I got a Lok Adalat notice. If I don't go, will they arrest me?", "style": "fear"},
  "Not at all. There are too many myths about Lok Adalat. Here is the truth."],
 "a3_rules": [
  "See what Lok Adalat actually is.",
  "It is a settlement meeting. Not a regular court case.",
  "Going is your choice. If you don't go, no arrest, no fine.",
  "No award comes without your consent. Only if both sides agree.",
  "If you don't go, the bank may file a regular case later.",
  "But if you agree there, that award is final. No appeal."],
 "a3_go": [
  "So when is it worth going?",
  "If you can arrange some money now, and you want to close the account, go. The offers there are often lower.",
  "If you have no money at all, or you don't want to sign under pressure, it's okay to skip. Send a written reply to the bank instead."],
 "a3_carry": [
  "If you go, here is a checklist.",
  "Carry ID proof, the notice, and your statements.",
  "Know your principal. Negotiate from there.",
  "If you can't pay at once, ask for instalments.",
  "Read the award properly. Amount, dates, and full and final.",
  "Take a certified copy of the award. And pay only to the bank's official account."],
 "a4_title": ["Every notice is not a reason to panic. Let's see which one is serious, and which one is not."],
 "a4_table": [
  "There are five kinds of notices.",
  "A legal notice PDF on WhatsApp is pressure from the agent. Take a screenshot, don't panic, and complain.",
  "A legal notice from an advocate is still not a case. Reply in writing.",
  "An arbitration notice is serious. Respond, and raise your objections.",
  "A court summons, you must respond. Go yourself, or send an advocate."],
 "a4_cheque": [
  "One more. Cheque bounce, or NACH notice.",
  "This comes only if a cheque you gave, or a bank auto debit, has bounced.",
  "This one is criminal. After the notice, you get fifteen days.",
  "Pay or reply within that time. And meet an advocate immediately."],
 "a4_arb": [
  "About arbitration, know these things.",
  "An arbitration award can be enforced just like a court decree.",
  "But if only one side appoints the arbitrator, the Supreme Court has said that is not valid.",
  "Reply in writing, and raise your objection early.",
  "If you ignore it, the award can come without you."],
 "a4_verify": [
  "How to check if a notice is genuine?",
  "A court summons has the court's name, case number, seal and signature.",
  "You can check that case number on the eCourts website.",
  "An advocate's notice has a letterhead with enrolment number and address.",
  "For free legal help, contact your District Legal Services Authority."],
 "a5_title": ["In settlement, your strongest number is your principal. Let's see how to calculate it."],
 "a5_steps": [
  "Four steps.",
  "One. Download statements from when the card was opened, or at least the last two or three years.",
  "Two. Add every purchase and every cash withdrawal.",
  "Three. Subtract every payment and refund you made.",
  "What's left is your principal. No interest, no fees, no GST in it."],
 "a5_stack": [
  "See one example.",
  "Purchases and cash together, two lakh sixty thousand.",
  "Payments and refunds together, one lakh seventy five thousand.",
  "So your principal is only eighty five thousand. Whatever the bank shows, this is your number."],
 "a5_tips": [
  "Some tips.",
  "Statements missing? Ask the bank by email. They have to give them.",
  "Write your calculation on one page. Show it in every negotiation.",
  "Start your first offer near your principal, not near their total."],
 "a6_title": ["Twelve more questions people ask. Quickly, let's go."],
 "a6_faq": [
  "Let's start.",
  {"q": "They sold my debt to an ARC. Now what?"},
  "Same debt, new owner, that's all. RBI rules still apply. Ask for the assignment letter, and settle with them only, in writing.",
  {"q": "Can they cut money from my account in another bank?"},
  "Only if you gave a mandate, like NACH or a standing instruction. Cancel old mandates.",
  {"q": "They are calling my friends and references!", "style": "anger"},
  "They may try to trace you. But they cannot tell them about your debt, or harass them. Complain.",
  {"q": "Can I record the recovery calls?"},
  "Recording your own calls as evidence is generally fine. Keep them safe.",
  {"q": "After I settle, will the calls stop?"},
  "They should. If calls continue even after the NOC, complain to the bank and to RBI.",
  {"q": "Will default affect my job?"},
  "Some companies, like banks and finance firms, check credit reports. Otherwise, usually no.",
  {"q": "Any passport or visa problem?"},
  "Card default alone doesn't affect your passport. Look out circulars are for big fraud cases only.",
  {"q": "My card had credit shield insurance."},
  "Check it. Death, disability, or job loss may be covered.",
  {"q": "Can I take a personal loan to pay the cards?"},
  "Only if the interest is much lower, the EMI is affordable, and you stop using cards. Loan apps, never.",
  {"q": "Can I convert my card dues into EMI?"},
  "Yes. But ask before default. It's much cheaper than revolving.",
  {"q": "Even after settlement, CIBIL is showing wrong data."},
  "Raise a dispute with CIBIL and the bank. If not fixed in thirty days, RBI rules give you one hundred rupees per day as compensation.",
  {"q": "Can I settle while my card is still regular?"},
  "Usually no. Instead, ask for an EMI plan or restructuring."],
}

STYLES_CLEAR = {"opendisc", "secured", "rates", "stack", "norule", "stages", "amounts", "property",
                "rbiagents", "rbicards", "ladder", "cancant", "disclaimer"}


def main():
    scenes = []
    for s in MAIN:
        s = copy.deepcopy(s)
        if s["id"] == "cautions":
            s["items"][0]["text"] = "Never ignore a court summons — Lok Adalat is voluntary but often the cheapest settlement"
        scenes.append(s)
        for pid in INSERT_AFTER.get(s["id"], []):
            pre = PREFIX[pid]
            for a in A[pid]["scenes"]:
                if a["type"] == "addonend":
                    continue
                a = copy.deepcopy(a)
                a["id"] = f"{pre}_{a['id']}"
                if a["type"] == "addon":
                    a["kicker"] = f"DEEP DIVE · {a['part']} of 6"
                scenes.append(a)
    ids = [s["id"] for s in scenes]
    assert len(ids) == len(set(ids)), "duplicate scene ids"
    missing = [i for i in ids if i not in EN and not i.startswith("ch")]
    assert not missing, f"no English narration for {missing}"
    styles = {i: "clear" for i in STYLES_CLEAR}
    for s in scenes:
        if s["id"][:3] in {f"{p}_" for p in PREFIX.values()} and s["type"] in ("rules", "table", "compare", "checklist"):
            styles[s["id"]] = "clear"
    json.dump(scenes, open(f"{HERE}/scenes.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    narr = {"_engine": "svara", "_fx": "A", "_lang": "English", "_styles": styles, **EN}
    json.dump(narr, open(f"{HERE}/narration.en.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(scenes), "scenes,", sum(len(v) for v in EN.values()), "lines")


if __name__ == "__main__":
    main()
