# -*- coding: utf-8 -*-
import json, os, shutil, html, re, zipfile
from PIL import Image
from content import SERVICES, GUIDES, GENERAL_FAQ, S
from icons import icon
from content2 import EXTRA, LAWS, LAW_OF, SOURCES, TITLES, SHORTS, FAQ_FIX, FAQ_ADD, FAQ_DROP, TABLES_ADD

SITE_URL = "https://tallawyer.com"
SRC = os.path.dirname(os.path.abspath(__file__))
OUT = "/home/claude/tal-law"
PHONE_INTL = "+972536199967"; PHONE = "053-619-9967"; WA = "972536199967"
ADDR = "כצנלסון 97, גבעתיים"; NAME = 'עו"ד טל אשכנזי'
GTAG = ""  # מזהה גוגל אדס / אנליטיקס, למשל AW-123456789

e = html.escape
shutil.rmtree(OUT, ignore_errors=True)
os.makedirs(OUT + "/assets")

def conv():
    for n in os.listdir(SRC + "/raw"):
        s = n.rsplit(".", 1)[0]
        im = Image.open(f"{SRC}/raw/{n}").convert("RGB")
        w = 1920 if s == "hero" else 1200
        if im.width > w: im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
        im.save(f"{OUT}/assets/{s}.webp", quality=78, method=6)
conv()
PORTRAIT = os.path.exists(f"{OUT}/assets/tal.webp")
def has(n): return os.path.exists(f"{OUT}/assets/{n}.webp")
def url(n): return f"assets/{n}.webp"

ICON_PHONE = '<svg aria-hidden="true" viewBox="0 0 24 24" width="18" height="18" fill="currentColor"><path d="M6.6 10.8a15 15 0 0 0 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.100.4 2.300.6 3.600.6.600 0 1 .4 1 1V20c0 .6-.4 1-1 1C10.600 21 3 13.400 3 4c0-.6.400-1 1-1h3.500c.6 0 1 .4 1 1 0 1.300.2 2.500.6 3.600.1.300 0 .7-.2 1z"/></svg>'
ICON_WA = '<svg aria-hidden="true" viewBox="0 0 24 24" width="18" height="18" fill="currentColor"><path d="M12 2a10 10 0 0 0-8.600 15l-1.300 4.800 4.900-1.300A10 10 0 1 0 12 2zm5.800 14.200c-.2.700-1.400 1.300-2 1.400-.5.100-1.200.1-1.900-.1-.4-.1-1-.3-1.800-.7-3.100-1.300-5.100-4.400-5.300-4.600-.2-.2-1.300-1.700-1.300-3.200s.8-2.300 1.100-2.600c.3-.3.600-.4.800-.4h.6c.2 0 .4 0 .6.500l.9 2.100c.1.200.1.300 0 .5l-.3.500-.4.500c-.1.100-.3.300-.1.600.2.300.8 1.300 1.700 2.100 1.200 1 2.100 1.400 2.400 1.500.3.100.5.100.7-.1l.9-1.100c.2-.3.400-.2.700-.1l2 1c.3.100.5.200.5.300.100.100.100.700-.1 1.400z"/></svg>'

med = [s for s in SERVICES if s["group"] == "med"]
oth = [s for s in SERVICES if s["group"] == "other"]

def head(title, desc, slug, schema, noindex=False):
    canon = f'<link rel="canonical" href="{SITE_URL}/{"" if slug=="index" else slug+".html"}">\n<meta property="og:url" content="{SITE_URL}/{"" if slug=="index" else slug+".html"}">' if SITE_URL else ""
    img = f'<meta property="og:image" content="{SITE_URL}/assets/hero.webp">' if SITE_URL else ""
    g = ''
    return f'''<!doctype html>
<html lang="he" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="robots" content="{"noindex" if noindex else "index, follow, max-image-preview:large"}">
<meta property="og:type" content="website"><meta property="og:locale" content="he_IL">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}">
{canon}{img}
<meta name="theme-color" content="#ffffff">
<link rel="icon" href="favicon.svg" type="image/svg+xml"><link rel="icon" href="favicon-48.png" sizes="48x48" type="image/png"><link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Heebo:wght@300;400;500;700;800&display=swap">
<link rel="stylesheet" href="style.css">
{g}
<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>
</head>
<body>
<a class="skip" href="#main">דלגו לתוכן</a>
'''

def links(lst): return "".join(f'<li><a href="{s["slug"]}.html">{e(s["menu"])}</a></li>' for s in lst)

def nav():
    return f'''<div class="util"><div class="wrap util-in"><span>{ADDR}</span><span>בדיקה ראשונית ללא עלות</span></div></div>
<header class="site-head"><div class="wrap bar">
<a class="logo" href="./"><span class="logo-t"><strong>טל אשכנזי</strong><span>משרד עורכי דין</span></span></a>
<button class="menu-btn" aria-expanded="false" aria-controls="nav">תפריט</button>
<nav id="nav" aria-label="ראשי"><ul class="top">
<li class="has"><a href="medical-malpractice.html">רשלנות רפואית</a><ul class="drop">{links(med)}</ul></li>
<li class="has"><a href="personal-injury.html">נזקי גוף וביטוח</a><ul class="drop">{links(oth)}</ul></li>
<li class="has"><a href="guides.html">מדריכים</a><ul class="drop">{links(GUIDES)}</ul></li>
<li><a href="about.html">אודות</a></li><li><a href="faq.html">שאלות ותשובות</a></li><li><a href="contact.html">צרו קשר</a></li>
</ul></nav>
<a class="head-call" href="tel:{PHONE_INTL}" data-ev="call">{ICON_PHONE}<span dir="ltr">{PHONE}</span></a>
</div></header>
<main id="main">
'''

def topics():
    o = "".join(f"<option>{t}</option>" for t in ["רשלנות רפואית","רשלנות בלידה או בהיריון","רשלנות בניתוח","טיפולי שיניים","תאונת דרכים","תאונת עבודה","ביטוח לאומי","אובדן כושר עבודה","תביעת ביטוח","אחר"])
    return o

fid = [0]
def form(title="בדיקת התיק ללא עלות", sub="השאירו פרטים ועו\"ד טל אשכנזי תחזור אליכם.", topic=None):
    fid[0] += 1; i = fid[0]
    opts = topics()
    field=f'<label for="t{i}">במה מדובר?</label><select id="t{i}" name="topic">{opts}</select>'
    if topic: field=f'<input type="hidden" name="topic" value="{e(topic)}">'
    return f'''<form class="lead" data-lead novalidate>
<h2 class="lead-h">{title}</h2><p class="lead-sub">{sub}</p>
<label for="n{i}">שם מלא</label><input id="n{i}" name="name" autocomplete="name" required>
<label for="p{i}">טלפון</label><input id="p{i}" name="phone" type="tel" inputmode="tel" autocomplete="tel" dir="ltr" required>
{field}
<p class="err" role="alert" hidden></p>
<button class="btn gold" type="submit">לבדיקת התיק</button>
<p class="fine">הפרטים נמסרים לעו"ד טל אשכנזי כדי לחזור אליכם ולבדוק את פנייתכם, ונשלחים באמצעות וואטסאפ. מסירתם אינה חובה לפי חוק, אך בלעדיהם לא נוכל לחזור אליכם. זכותכם לעיין במידע ולבקש לתקנו. <a href="privacy.html">מדיניות פרטיות</a></p>
</form>'''

def foot():
    return f'''</main>
<section class="final"><div class="wrap final-in"><div><p class="f-k">שיחת ייעוץ ראשונית ללא עלות</p><h2>דברו ישירות עם עו"ד טל אשכנזי</h2></div>
<div class="f-act"><a class="f-phone" href="tel:{PHONE_INTL}" data-ev="call" dir="ltr">{PHONE}</a><a class="btn gold" href="https://wa.me/{WA}" target="_blank" rel="noopener" data-ev="whatsapp">{ICON_WA}כתבו בוואטסאפ</a></div></div></section>
<footer class="foot"><div class="wrap cols">
<div><p class="f-name">עו"ד טל וולק אשכנזי</p><p>מספר רישיון: 90780</p><p>{ADDR}</p><p>טלפון: <a href="tel:{PHONE_INTL}" dir="ltr">{PHONE}</a></p></div>
<div><h3>רשלנות רפואית</h3><ul>{links(med)}</ul></div>
<div><h3>נזקי גוף וביטוח</h3><ul>{links(oth)}</ul></div>
<div><h3>המשרד</h3><ul><li><a href="about.html">אודות</a></li><li><a href="personal-injury.html">נזקי גוף</a></li><li><a href="guides.html">מדריכים</a></li>{links(GUIDES)}<li><a href="faq.html">שאלות ותשובות</a></li><li><a href="contact.html">צרו קשר</a></li><li><a href="accessibility.html">הצהרת נגישות</a></li><li><a href="privacy.html">מדיניות פרטיות</a></li></ul></div>
</div><p class="wrap legal">המידע באתר הוא מידע כללי ואינו מהווה ייעוץ משפטי או תחליף לבדיקת המקרה הפרטני. פרסום זה אינו מבטיח תוצאה.</p></footer>
<div class="mobile-bar"><a href="tel:{PHONE_INTL}" data-ev="call">{ICON_PHONE}חייגו עכשיו</a><a class="wa" href="https://wa.me/{WA}" target="_blank" rel="noopener" data-ev="whatsapp">{ICON_WA}וואטסאפ</a></div>
<div class="float" aria-label="יצירת קשר מהירה"><a class="fl wa" href="https://wa.me/{WA}" target="_blank" rel="noopener" data-ev="whatsapp" aria-label="שליחת הודעה בוואטסאפ">{ICON_WA}</a><a class="fl call" href="tel:{PHONE_INTL}" data-ev="call" aria-label="חיוג ל-{PHONE}">{ICON_PHONE}</a></div>
<button class="a11y-btn" type="button" aria-expanded="false" aria-controls="a11y" aria-label="פתיחת תפריט נגישות"><svg aria-hidden="true" viewBox="0 0 24 24" width="26" height="26" fill="currentColor"><circle cx="12" cy="4.500" r="2.200"/><path d="M4 8.200l.6-1.800c4.900 1.300 9.900 1.300 14.800 0l.6 1.800c-2 .6-4 1-6 1.200v3.300l2.500 7.500-1.800.6L12.300 14h-.6l-2.400 6.800-1.800-.6 2.500-7.500V9.400c-2-.2-4-.6-6-1.200z"/></svg></button>
<div class="a11y" id="a11y" role="group" aria-label="הגדרות נגישות" hidden><h2>נגישות</h2><button type="button" data-a="bigger">הגדלת טקסט</button><button type="button" data-a="smaller">הקטנת טקסט</button><button type="button" data-a="contrast" aria-pressed="false">ניגודיות גבוהה</button><button type="button" data-a="links" aria-pressed="false">הדגשת קישורים</button><button type="button" data-a="still" aria-pressed="false">עצירת הנפשות</button><button type="button" data-a="reset">איפוס</button><a href="accessibility.html">הצהרת נגישות</a></div>
<div class="consent" data-consent hidden><p>אנו משתמשים בעוגיות של גוגל למדידה ופרסום, רק אם תאשרו. <a href="privacy.html#cookies">פרטים נוספים</a></p><div class="consent-b"><button type="button" class="btn dark" data-c="y">אישור</button><button type="button" class="btn line" data-c="n">דחייה</button></div></div>
<script>window.SITE_GTAG="{GTAG}";</script>
<script src="main.js"></script>
</body></html>'''

OFFICE_ID=(SITE_URL+"/#office") if SITE_URL else "#office"
TAL_ID=(SITE_URL+"/#tal") if SITE_URL else "#tal"
BIZ = {"@type":"LegalService","@id":OFFICE_ID,"name":NAME,"alternateName":["עו\"ד טל וולק אשכנזי","טל אשכנזי משרד עורכי דין"],"telephone":PHONE_INTL,
 "address":{"@type":"PostalAddress","streetAddress":"כצנלסון 97","addressLocality":"גבעתיים","addressCountry":"IL"},
 "areaServed":{"@type":"Country","name":"ישראל"},"knowsLanguage":"he",
 "employee":{"@type":"Person","@id":TAL_ID,"name":"טל אשכנזי","alternateName":"טל וולק אשכנזי","jobTitle":"עורכת דין","identifier":{"@type":"PropertyValue","name":"מספר רישיון בלשכת עורכי הדין","value":"90780"},"worksFor":{"@id":OFFICE_ID},"knowsAbout":["רשלנות רפואית","נזקי גוף"]},
 "knowsAbout":["רשלנות רפואית","נזקי גוף","תאונות דרכים","תאונות עבודה","ביטוח לאומי","אובדן כושר עבודה","תביעות ביטוח"]}
if SITE_URL: BIZ["url"] = SITE_URL + "/"

def crumbs_ld(trail):
    items = [{"@type":"ListItem","position":i+1,"name":n} | ({"item":f"{SITE_URL}/{'' if u=='./' else u}"} if SITE_URL and u else {}) for i,(n,u) in enumerate(trail)]
    return {"@type":"BreadcrumbList","itemListElement":items}
def faq_ld(faqs):
    return {"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faqs]}
def graph(*x): return {"@context":"https://schema.org","@graph":list(x)}

def render_items(items):
    o = ""
    for it in items:
        if isinstance(it,dict):
            o+="<div class='tbl'><table><thead><tr>"+"".join(f"<th scope='col'>{e(c)}</th>" for c in it["t"])+"</tr></thead><tbody>"+"".join("<tr>"+"".join(f"<td>{e(c)}</td>" for c in r)+"</tr>" for r in it["r"])+"</tbody></table></div>"; continue
        o += "<ul class='ticks'>"+"".join(f"<li>{e(i)}</li>" for i in it)+"</ul>" if isinstance(it,list) else f"<p>{e(it)}</p>"
    return o
def faq_html(faqs):
    return "".join(f"<details class='q'><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q,a in faqs)

STEPS = [("בדיקה ראשונית","שיחה קצרה על מה שקרה ועל המועדים, ללא עלות."),("איסוף התיק הרפואי","אנחנו מסדרים יחד את כל המסמכים הרלוונטיים."),("חוות דעת רפואית","במקרה המתאים פונים למומחה בתחום."),("דרישה ותביעה","פנייה לנתבעים והגשה לבית המשפט לפי הצורך."),("פשרה או פסק דין","ליווי אישי עד סיום ההליך.")]
def steps(): return "<ol class='steps'>"+"".join(f"<li><strong>{a}</strong><span>{b}</span></li>" for a,b in STEPS)+"</ol>"

def calc():
    return '''<section class="calc" id="calc" aria-labelledby="ch"><h2 id="ch">מחשבון מועד אחרון לתביעת רשלנות רפואית</h2>
<p>הערכה כללית לפי הכללים הרגילים. אינה ייעוץ משפטי.</p>
<form data-calc novalidate><div class="calc-g">
<div><label for="c1">תאריך הטיפול</label><input id="c1" type="date" required></div>
<div><label for="c2">הנזק התגלה מאוחר יותר? <span>לא חובה</span></label><input id="c2" type="date"></div>
<div><label for="c3">תאריך לידה של הנפגע/ת <span>לא חובה</span></label><input id="c3" type="date"></div>
</div><button class="btn dark" type="submit">חשבו מועד</button></form>
<div class="calc-out" data-out aria-live="polite" hidden></div></section>'''

def service_page(s, kind):
    parent = ("רשלנות רפואית","medical-malpractice.html") if s.get("group")=="med" else (("נזקי גוף וביטוח","personal-injury.html") if kind=="service" else ("מדריכים","guides.html"))
    trail=[("ראשי","./")]
    if s["slug"]!="medical-malpractice": trail.append(parent)
    trail.append((s["h1"],""))
    ld = graph(BIZ, crumbs_ld(trail), faq_ld(s["faqs"]),
      ({"@type":"Article","headline":s["h1"],"description":s["desc"],"author":{"@id":TAL_ID},"publisher":{"@id":OFFICE_ID},"datePublished":"2026-11-09","dateModified":"2026-11-10","inLanguage":"he"} if kind=="guide" else {"@type":"Service","name":s["h1"],"serviceType":s["kw"],"provider":{"@id":OFFICE_ID},"areaServed":"ישראל"}))
    bc = "".join((f'<a href="{u}">{e(n)}</a><span>/</span>' if u else f'<span aria-current="page">{e(n)}</span>') for n,u in trail)
    mid=f'<aside class="mid"><p><strong>רוצים לדעת איך זה נוגע למקרה שלכם?</strong> שיחה קצרה יכולה להבהיר מה כדאי לבדוק.</p><a class="btn dark" href="tel:{PHONE_INTL}" data-ev="call">{ICON_PHONE}<span dir="ltr">{PHONE}</span></a></aside>'
    parts=[f"<section><h2>{e(x['h'])}</h2>{render_items(x['items'])}</section>" for x in s["sections"]]
    parts.insert(min(2,len(parts)),mid)
    secs="".join(parts)
    lawkey=LAW_OF.get(s["slug"],"med")
    laws="<section><h2>הבסיס המשפטי</h2><ul class='ticks'>"+"".join(f"<li>{e(l)}</li>" for l in LAWS[lawkey])+"</ul>"
    if SOURCES.get(s["slug"]): laws+="<h3 class='src-h'>מקורות לקריאה נוספת</h3><ul class='ticks'>"+"".join(f'<li><a href="{u}" target="_blank" rel="noopener">{e(t)}</a></li>' for t,u in SOURCES[s["slug"]])+"</ul>"
    laws+="</section>"
    more=""
    if s["slug"]=="medical-malpractice":
        more="<section><h2>רשלנות רפואית לפי תחום</h2><ul class='ticks'>"+"".join(f'<li><a href="{x["slug"]}.html">{e(x["h1"])}</a>: {e(x["card"])}</li>' for x in med[1:])+"</ul></section>"
    elif s.get("group")=="med":
        extra=[("national-insurance.html","זכויות בביטוח הלאומי")] if s["slug"] in ("eye","birth-injury","cancer-diagnosis") else []
        more="<section><h2>מדריכים שיעזרו לכם</h2><ul class='ticks'>"+"".join(f'<li><a href="{x["slug"]}.html">{e(x["h1"])}</a></li>' for x in GUIDES)+"".join(f'<li><a href="{h}">{t}</a></li>' for h,t in extra)+'<li><a href="medical-malpractice.html">רשלנות רפואית: מה צריך להוכיח</a></li></ul></section>'
    elif s.get("group")=="other":
        more='<section><h2>לפי סוג הפגיעה</h2><p>הדרך לפיצוי תלויה במקור הפגיעה. <a href="personal-injury.html">סקירה של כל המסלולים לנפגעי גוף</a>.</p></section>'
    first='<section class="first"><h2>מה מקבלים בשיחה הראשונה</h2><ul class="ticks"><li>הבנה ראשונית אם כדאי להמשיך לבדוק את המקרה</li><li>הערכה של המועד האחרון להגשת תביעה</li><li>רשימה של המסמכים שכדאי לאסוף</li></ul></section>'
    pool = (med if s.get("group")=="med" else oth if s.get("group") else GUIDES)
    k=[x["slug"] for x in pool].index(s["slug"])
    rel=[pool[(k+1)%len(pool)],pool[(k+2)%len(pool)]]
    if pool is GUIDES: rel=[x for x in GUIDES if x is not s]+[SERVICES[0]]
    elif pool is med: rel.append(GUIDES[0])
    else: rel.append(pool[(k+3)%len(pool)])
    relh = "".join(f'<a class="rel" href="{x["slug"]}.html">{icon(x["slug"])}<strong>{e(x["menu"])}</strong><span>{e(x["card"])}</span></a>' for x in rel)
    body = head(s["title"],s["desc"],s["slug"],ld)+nav()+f'''<div class="page-hero"{f""" style="--img:url({url(s['img'])})" """ if has(s["img"]) else ""}>{"" if has(s["img"]) else icon(s["slug"],"ph-icon")}<div class="wrap ph">
<nav class="crumbs" aria-label="מיקום">{bc}</nav><p class="eyebrow">{e(s["eyebrow"])}</p><h1>{e(s["h1"])}</h1>
<div class="actions"><a class="btn gold" href="tel:{PHONE_INTL}" data-ev="call">{ICON_PHONE}<span dir="ltr">{PHONE}</span></a><a class="btn line" href="https://wa.me/{WA}" target="_blank" rel="noopener" data-ev="whatsapp">{ICON_WA}וואטסאפ</a></div>
<p class="trust">בדיקה ראשונית ללא עלות · שכר טרחה רק אם מתקבל פיצוי</p></div></div>
<div class="wrap layout"><article class="prose">
<div class="answer"><h2>בקצרה</h2><p>{e(s["short"])}</p></div>{first}{calc() if s.get("calc") else ""}{secs}{more}{laws}
<section><h2>איך התהליך עובד</h2>{steps()}</section>
<section><h2>שאלות נפוצות</h2>{faq_html(s["faqs"])}</section>
<p class="byline">נכתב על ידי <a href="about.html">{NAME}</a>. עודכן בנובמבר 2026. מידע כללי שאינו מחליף ייעוץ משפטי.</p>
</article><aside class="side">{form(topic=s["eyebrow"])}</aside></div>
<section class="wrap related"><h2>נושאים קשורים</h2><div class="rel-g">{relh}</div></section>
'''+foot()
    open(f'{OUT}/{s["slug"]}.html','w',encoding='utf-8').write(body)

def simple(slug,title,desc,h1,content,noindex=False,ld=None,with_form=False):
    b=head(title,desc,slug,ld or graph(BIZ,crumbs_ld([("ראשי","./"),(h1,"")])),noindex)+nav()
    aside=f'<aside class="side">{form()}</aside>' if with_form else ''
    b+=f'<div class="plain-head">{icon("contact" if slug=="contact" else "insurance-claims","ph-icon")}<div class="wrap"><h1>{e(h1)}</h1></div></div><div class="wrap {"layout" if with_form else "narrow"}"><article class="prose">{content}</article>{aside}</div>'+foot()
    open(f'{OUT}/{slug}.html','w',encoding='utf-8').write(b)

for s in SERVICES+GUIDES:
    x=EXTRA.get(s["slug"],{})
    s["sections"]=s["sections"]+x.get("s",[])+TABLES_ADD.get(s["slug"],[]); s["faqs"]=s["faqs"]+x.get("f",[])
    s["faqs"]=[(q,FAQ_FIX.get(q,a)) for q,a in s["faqs"] if not (s["slug"] in FAQ_DROP and q.startswith("כמה עולה עורכת דין"))]+FAQ_ADD.get(s["slug"],[])
    if s["slug"] in TITLES: s["title"]=TITLES[s["slug"]]
    if s["slug"] in SHORTS: s["short"]=SHORTS[s["slug"]]
for s in SERVICES: service_page(s,"service")
for g in GUIDES: service_page(g,"guide")

def columns():
    o='<svg class="cols-art" aria-hidden="true" viewBox="0 0 520 620" fill="none" stroke="currentColor" stroke-width="1">'
    o+='<path d="M10 40H510M10 54H510M24 78H496M24 66H496"/>'
    for x in range(44,520,108):
        o+=f'<path d="M{x-24} 78h48l-6 18h-36zM{x-18} 96V570M{x+18} 96V570M{x-26} 570h52v18h-52z"/>'
        for d in (-9,0,9): o+=f'<path d="M{x+d} 100V566"/>'
    return o+'<path d="M0 588H520M0 606H520"/></svg>'
def tiles(items): return '<div class="tiles">'+"".join(f'<a class="tile" href="{h}.html"><img src="{url(i)}" alt="{e(a)}" width="1024" height="688" decoding="async" loading="lazy"><span>{e(t)}</span></a>' for i,h,t,a in items)+'</div>'
# דף הבית
def cells(lst): return "".join(f'<a class="cell" href="{s["slug"]}.html">{icon(s["slug"])}<h3>{e(s["menu"])}</h3><p>{e(s["card"])}</p><span class="go">קראו עוד</span></a>' for s in lst)
home_faq=GENERAL_FAQ[:5]
home=head('עו"ד טל אשכנזי | עורך דין רשלנות רפואית ונזקי גוף','עו"ד טל אשכנזי מלווה נפגעי רשלנות רפואית, תאונות וביטוח. בדיקה ראשונית ללא עלות, שכר טרחה רק אם מתקבל פיצוי. כצנלסון 97 גבעתיים. 053-619-9967.','index',graph(BIZ,faq_ld(home_faq),{"@type":"WebSite","name":NAME,"inLanguage":"he"}))+nav()
PULSE='<svg class="pulse" aria-hidden="true" viewBox="0 0 1440 130" preserveAspectRatio="none" fill="none"><path pathLength="1" vector-effect="non-scaling-stroke" d="M0 86H470l16-10 16 10h26l12 18 20-96 20 116 14-38h30l18-14 18 14H1440"/></svg>'
ruler=lambda n,lbl:f'<div class="r"><span class="r-l">{lbl}</span><div class="r-t"><i style="width:{n*10}%"></i></div><b>{n}</b></div>'
axis="".join(f'<span style="right:{k*10}%">{k}</span>' for k in range(0,11))
hero_visual=f'<img class="hero-photo" src="{url("hero")}" alt="שולחן עבודה עם תיקים משפטיים וצילום רנטגן" width="1344" height="752" decoding="async" fetchpriority="high">'
statement=('<img class="portrait" src="assets/tal.webp" alt="עו&quot;ד טל אשכנזי" loading="lazy">' if PORTRAIT else f'<div class="plate"><img src="{url("office")}" alt="חדר ישיבות עם ספרי משפט" width="1024" height="688" decoding="async" loading="lazy"></div>')
home+=f'''<section class="hero"><div class="wrap hero-g"><div class="hero-t">
<p class="kicker">{NAME}</p>
<h1>עורכת דין<br><em>רשלנות רפואית</em><br>ונזקי גוף</h1>
<p class="lede">נפגעתם מטיפול רפואי או בתאונה? אבדוק את המקרה שלכם, אסביר בשפה פשוטה מה הזכויות והאפשרויות, ואדאג שתקבלו את הליווי המשפטי המתאים.</p>
<div class="actions"><a class="btn dark" href="tel:{PHONE_INTL}" data-ev="call">{ICON_PHONE}<span dir="ltr">{PHONE}</span></a><a class="btn line" href="https://wa.me/{WA}" target="_blank" rel="noopener" data-ev="whatsapp">{ICON_WA}וואטסאפ</a></div>
<p class="note">ייעוץ ראשוני ללא עלות · שכר טרחה רק במקרה של פיצוי</p></div>
<div class="hero-f">{hero_visual}{form("בדיקת התיק ללא עלות")}</div></div></section>
<section class="commit"><div class="wrap commit-g"><div><h3>ליווי אישי</h3><p>התיק מטופל ישירות על ידי עורכת הדין, משלב הבדיקה ועד הסיום.</p></div><div><h3>5 שנות ניסיון</h3><p>עיסוק בתביעות רשלנות רפואית ונזקי גוף.</p></div><div><h3>שקיפות מלאה</h3><p>שכר הטרחה וההוצאות מוגדרים מראש בהסכם כתוב.</p></div></div></section>
<section class="wrap block"><div class="sec-h center"><h2 class="big">תחומי עיסוק ברשלנות רפואית</h2><p class="intro">בכל תחום מוסבר מה נבדק בתיק ומה חשוב לעשות כעת.</p></div>{tiles([("surgery","surgery","רשלנות בניתוח","חדר ניתוח ריק"),("birth","birth-injury","רשלנות בלידה","עריסה בחדר יולדות"),("xray","cancer-diagnosis","איחור באבחון","צילומי דימות על לוח מואר"),("dental","dental","טיפולי שיניים","כלי טיפול ברפואת שיניים")])}<div class="ledger">{cells(med)}</div></section>
<section class="clock"><div class="wrap clock-g"><div><h2 class="big">מועדי התיישנות</h2><p class="clock-sub">שנים מיום האירוע, לפי הכללים הרגילים.</p><div class="ruler">{ruler(3,"תגמולי ביטוח")}{ruler(7,"רשלנות רפואית")}{ruler(10,"נזק שהתגלה מאוחר, לכל היותר")}<div class="axis"><div>{axis}</div></div></div><a class="link" href="statute-of-limitations.html#calc">למחשבון המועד האחרון</a></div>
<aside class="minor"><b>25</b><h3>נפגעים קטינים</h3><p>מניין השנים מתחיל בגיל 18, ולכן אפשר בדרך כלל לתבוע עד גיל 25.</p></aside></div></section>
<section class="wrap block"><div class="sec-h center"><h2 class="big">נזקי גוף וזכויות רפואיות</h2></div>{tiles([("road","road-accidents","תאונות דרכים","כביש מהיר בשעת ערב"),("work","work-accidents","תאונות עבודה","קסדת מגן באתר בנייה"),("insurance","disability-insurance","אובדן כושר עבודה","מסמך ביטוח על שולחן")])}<div class="ledger">{cells(oth)}<a class="cell" href="contact.html">{icon("contact")}<h3>תחום אחר</h3><p>לא מצאתם את הנושא שלכם? פנו ונבדוק יחד.</p><span class="go">צרו קשר</span></a></div></section>
<section class="about-b"><div class="wrap about-g">{statement}<div><p class="kicker">אודות</p><h2 class="big">עו"ד טל אשכנזי</h2><p>עורכת דין העוסקת בתביעות רשלנות רפואית ונזקי גוף, עם חמש שנות ניסיון. מי שנפגע זקוק למי שתקרא את התיק לעומק, תאמר לו את האמת על הסיכויים ותעמוד לצידו מול בתי חולים וחברות ביטוח.</p><ul class="ticks"><li>בדיקה אישית של כל תיק</li><li>עבודה עם רופאים מומחים לפי תחום המקרה</li><li>עדכון שוטף לאורך ההליך</li></ul><a class="link" href="about.html">להמשך קריאה</a></div></div></section>
<section class="wrap block"><div class="sec-h center"><h2 class="big">שלבי הטיפול בתיק</h2></div>{steps()}</section>
<section class="faq-b"><div class="wrap faq-g"><div><h2 class="big">שאלות נפוצות</h2><a class="link" href="faq.html">לכל השאלות</a></div><div>{faq_html(home_faq)}</div></div></section>
'''+foot()
open(f'{OUT}/index.html','w',encoding='utf-8').write(home)

pi_rows=[["תאונת דרכים","חברת הביטוח של הרכב, ובמקרים מסוימים קרנית","road-accidents"],["תאונה בעבודה או בדרך אליה","הביטוח הלאומי, ולפעמים גם המעסיק","work-accidents"],["מחלה או תאונה שפגעו ביכולת לעבוד","הביטוח הלאומי, וחברת הביטוח או קרן הפנסיה","disability-insurance"],["נכות שמגבילה את היום יום","הביטוח הלאומי","national-insurance"],["פוליסה פרטית: תאונות אישיות, מחלות קשות, סיעוד","חברת הביטוח","insurance-claims"],["טיפול רפואי","הרופא, בית החולים, קופת החולים או המבטח שלהם","medical-malpractice"]]
pic=f'''<div class="answer"><h2>בקצרה</h2><p>נזקי גוף הם פגיעה גופנית או נפשית שנגרמה בתאונה, בעבודה או בטיפול רפואי. הדרך לפיצוי תלויה במקור הפגיעה: חברת ביטוח הרכב, הביטוח הלאומי, המעסיק, פוליסה פרטית או הגורם המטפל. לפעמים יש יותר ממסלול אחד, והסדר שבו פונים משפיע על הפיצוי.</p></div>
<section><h2>למי פונים, לפי סוג הפגיעה</h2><div class="tbl"><table><thead><tr><th scope="col">מה קרה</th><th scope="col">ממי מבקשים פיצוי</th></tr></thead><tbody>'''+"".join(f'<tr><td><a href="{r[2]}.html">{e(r[0])}</a></td><td>{e(r[1])}</td></tr>' for r in pi_rows)+'''</tbody></table></div></section>
<section><h2>מה כדאי לעשות כבר עכשיו</h2><ul class="ticks"><li>לקבל טיפול רפואי ולוודא שהאירוע מתועד</li><li>לשמור מסמכים רפואיים, קבלות ואישורים מהעבודה</li><li>לא לחתום על ויתור או הסדר לפני בדיקה</li><li>לבדוק את המועד האחרון להגשה, כי הוא שונה בין המסלולים</li></ul></section>
<section><h2>הנושאים</h2><div class="rel-g">'''+"".join(f'<a class="rel" href="{x["slug"]}.html">{icon(x["slug"])}<strong>{e(x["menu"])}</strong><span>{e(x["card"])}</span></a>' for x in oth)+'</div></section>'
simple("personal-injury",'עורך דין נזקי גוף: תאונות, ביטוח לאומי וביטוח | טל אשכנזי','נפגעתם בתאונה, בעבודה או בטיפול רפואי? כך מבינים ממי מבקשים פיצוי ומה עושים עכשיו. בדיקה ראשונית ללא עלות. 053-619-9967.','עורכת דין נזקי גוף',pic,ld=graph(BIZ,crumbs_ld([("ראשי","./"),("נזקי גוף וביטוח","")])),with_form=True)

aboutc=f'''<div class="answer"><p>עו"ד טל אשכנזי עוסקת בתביעות רשלנות רפואית ונזקי גוף, עם חמש שנות ניסיון (מספר רישיון 90780). המשרד נמצא בכצנלסון 97 בגבעתיים ומלווה לקוחות מכל הארץ.</p></div>
<section><h2>למה בחרתי בתחום</h2><p>אנשים מגיעים אליי אחרי תקופה קשה, ובדרך כלל בלי לדעת אם מה שקרה להם הוא טעות או גזירת גורל. התפקיד שלי מתחיל בלברר את זה ביושר.</p></section>
<section><h2>איך אני עובדת</h2><ul class="ticks"><li>בודקת כל תיק בעצמי ואומרת מה הסיכויים, גם כשהם נמוכים</li><li>מסבירה בשפה פשוטה את כל שלבי ההליך</li><li>מעדכנת באופן שוטף</li><li>פועלת עם רופאים מומחים לפי תחום המקרה</li><li>מגדירה מראש בכתב את שכר הטרחה ואת ההוצאות</li></ul></section>
<section><h2>תחומי עיסוק</h2><ul class="ticks"><li><a href="medical-malpractice.html">רשלנות רפואית</a></li><li><a href="road-accidents.html">תאונות דרכים</a></li><li><a href="work-accidents.html">תאונות עבודה</a></li><li><a href="national-insurance.html">ביטוח לאומי</a></li><li><a href="disability-insurance.html">אובדן כושר עבודה</a></li><li><a href="insurance-claims.html">תביעות ביטוח</a></li></ul></section>'''
simple("about",'אודות עו"ד טל אשכנזי | רשלנות רפואית ונזקי גוף בגבעתיים','עו"ד טל אשכנזי, 5 שנות ניסיון ברשלנות רפואית ונזקי גוף. יחס אישי, הסברים ברורים. כצנלסון 97, גבעתיים.','אודות עו"ד טל אשכנזי',aboutc,with_form=True)

simple("faq",'שאלות ותשובות על רשלנות רפואית ונזקי גוף | עו"ד טל אשכנזי','תשובות לשאלות נפוצות על תביעות רשלנות רפואית, שכר טרחה, התיישנות ותהליך העבודה.','שאלות ותשובות',faq_html(GENERAL_FAQ),ld=graph(BIZ,faq_ld(GENERAL_FAQ),crumbs_ld([("ראשי","./"),("שאלות ותשובות","")])),with_form=True)

gl="".join(f'<a class="rel" href="{x["slug"]}.html">{icon(x["slug"])}<strong>{e(x["h1"])}</strong><span>{e(x["card"])}</span></a>' for x in GUIDES)
simple("guides",'מדריכים לנפגעי רשלנות רפואית | עו"ד טל אשכנזי','מדריכים בשפה פשוטה לנפגעי רשלנות רפואית: התיישנות, חוות דעת רפואית, ואיך מקבלים עותק של התיק הרפואי.','מדריכים',f'<div class="rel-g">{gl}</div>')

cc=f'''<p class="big-phone"><a href="tel:{PHONE_INTL}" dir="ltr" data-ev="call">{PHONE}</a></p>
<ul class="ticks"><li>כתובת: {ADDR}</li><li>וואטסאפ: <a href="https://wa.me/{WA}" target="_blank" rel="noopener" data-ev="whatsapp">שלחו הודעה</a></li><li>פגישה במשרד בתיאום מראש</li></ul>
<p><a class="link" href="https://www.google.com/maps/search/?api=1&query=%D7%9B%D7%A6%D7%A0%D7%9C%D7%A1%D7%95%D7%9F+97+%D7%92%D7%91%D7%A2%D7%AA%D7%99%D7%99%D7%9D" target="_blank" rel="noopener">פתחו ניווט למשרד</a></p>'''
simple("contact",'צרו קשר | עו"ד טל אשכנזי, כצנלסון 97 גבעתיים','פנו לעו"ד טל אשכנזי לבדיקה ראשונית ללא עלות. טלפון 053-619-9967, כצנלסון 97, גבעתיים.','צרו קשר',cc,with_form=True)

simple("thanks",'תודה על פנייתכם | עו"ד טל אשכנזי','הפנייה שלכם לעו"ד טל אשכנזי התקבלה.','תודה על פנייתכם',f'<p>אם הוואטסאפ לא נפתח, אפשר לשלוח הודעה ישירות או להתקשר:</p><div class="actions"><a class="btn gold" href="tel:{PHONE_INTL}" data-ev="call">{ICON_PHONE}<span dir="ltr">{PHONE}</span></a><a class="btn dark" href="https://wa.me/{WA}" target="_blank" rel="noopener" data-ev="whatsapp">{ICON_WA}וואטסאפ</a></div>',noindex=True)

simple("accessibility",'הצהרת נגישות | עו"ד טל אשכנזי','הצהרת הנגישות של אתר עו"ד טל אשכנזי: התאמות, דרכי פנייה ופרטי רכזת הנגישות.','הצהרת נגישות',f'''<div class="answer"><p>אנו רואים חשיבות בהנגשת האתר לאנשים עם מוגבלות, בהתאם לחוק שוויון זכויות לאנשים עם מוגבלות, התשנ"ח-1998, ולתקנות הנגישות לשירות, התשע"ג-2013.</p></div>
<section><h2>התקן שלפיו נבנה האתר</h2><p>האתר נבנה במטרה לעמוד בדרישות תקן ישראלי 5568, המבוסס על הנחיות נגישות לתוכן אינטרנט, ברמה AA.</p></section>
<section><h2>התאמות שבוצעו</h2><ul class="ticks"><li>ניווט מלא באמצעות מקלדת וקישור דילוג לתוכן</li><li>מבנה כותרות היררכי ותוויות לשדות טופס</li><li>טקסט חלופי לתמונות בעלות תוכן</li><li>התאמה למסכי נייד ולהגדלת טקסט</li><li>תפריט נגישות: הגדלת טקסט, ניגודיות גבוהה, הדגשת קישורים ועצירת הנפשות</li></ul></section>
<section><h2>שימוש בתפריט הנגישות</h2><p>לחצו על כפתור הנגישות בפינת המסך, או הגיעו אליו באמצעות המקש Tab.</p></section>
<section><h2>נגישות המשרד</h2><p>המשרד נמצא בכצנלסון 97, גבעתיים. למידע על הסדרי נגישות לפני הגעה, ולתיאום פגישה בטלפון או מרחוק, אפשר לפנות אלינו.</p></section>
<section><h2>נתקלתם בקושי?</h2><p>נשמח לקבל פנייה ולטפל בה. כדי שנוכל לסייע, ציינו את הדף ואת הבעיה.</p><ul class="ticks"><li>רכזת נגישות: עו"ד טל אשכנזי</li><li>טלפון ווואטסאפ: <a href="tel:{PHONE_INTL}" dir="ltr">{PHONE}</a></li><li>כתובת: {ADDR}</li></ul></section>
<p class="byline">ההצהרה עודכנה בנובמבר 2026.</p>''')

simple("privacy",'מדיניות פרטיות | עו"ד טל אשכנזי','מדיניות הפרטיות של אתר עו"ד טל אשכנזי: איזה מידע נאסף, למה הוא משמש, ומהן זכויותיכם לפי חוק הגנת הפרטיות.','מדיניות פרטיות',f'''<div class="answer"><p>מדיניות זו מסבירה איזה מידע נאסף באתר, למה הוא משמש ומהן זכויותיכם לפי חוק הגנת הפרטיות, התשמ"א-1981.</p></div>
<section><h2>מי אחראית למידע</h2><p>{NAME}, {ADDR}, טלפון <a href="tel:{PHONE_INTL}" dir="ltr">{PHONE}</a>.</p></section>
<section><h2>איזה מידע נאסף</h2><ul class="ticks"><li>בטופס: שם, טלפון, והנושא שאליו אתם פונים</li><li>בשיחה או בהודעה: מה שתבחרו למסור</li><li>בעת גלישה: נתונים טכניים כגון כתובת רשת וסוג דפדפן, הנחוצים לפעולת האתר</li></ul></section>
<section><h2>למה המידע משמש</h2><ul class="ticks"><li>חזרה אליכם ובדיקת הפנייה</li><li>מתן שירות משפטי, אם תבחרו בכך</li><li>עמידה בחובות שבדין</li><li>אם תאשרו: מדידה ושיפור של האתר והפרסום</li></ul></section>
<section><h2>אין חובה למסור מידע</h2><p>אין חובה חוקית למסור מידע באתר, ומסירתו נעשית מרצונכם. בלי פרטי התקשרות לא נוכל לחזור אליכם.</p></section>
<section><h2>מידע רפואי</h2><p>מידע רפואי הוא מידע רגיש. אין צורך למסור אותו בטופס או בוואטסאפ. פרטים רפואיים נמסרים בשלב הבדיקה עצמה, ישירות לעורכת הדין, ונשמרים בסודיות מקצועית.</p></section>
<section><h2>למי המידע עשוי להימסר</h2><ul class="ticks"><li>חברת האחסון של האתר</li><li>וואטסאפ, כאשר אתם שולחים הודעה. השירות מופעל על ידי חברה מחוץ לישראל</li><li>גוגל, לגופנים באתר, ולמדידה ופרסום אם תאשרו</li><li>מומחים ונותני שירות הקשורים בטיפול בתיק, בהסכמתכם</li><li>רשויות, אם החוק מחייב זאת</li></ul><p>איננו מוכרים מידע אישי.</p></section>
<section id="cookies"><h2>עוגיות</h2><p>עוגיות למדידה ולפרסום יופעלו רק לאחר אישורכם בהודעה שתוצג באתר. אפשר למחוק או לחסום עוגיות בהגדרות הדפדפן.</p></section>
<section><h2>שמירה ואבטחה</h2><p>המידע נשמר כל עוד הוא נחוץ למטרות שלעיל ולפי חובות הדין, ואנו נוקטים אמצעים סבירים להגנה עליו. אין אפשרות להבטיח הגנה מוחלטת באינטרנט.</p></section>
<section><h2>הזכויות שלכם</h2><p>לפי חוק הגנת הפרטיות אתם זכאים לעיין במידע שנשמר עליכם ולבקש לתקנו או למחקו אם אינו נכון, שלם, ברור או מעודכן. אפשר לפנות בטלפון או בכתב לכתובת המשרד. אפשר גם לפנות לרשות להגנת הפרטיות.</p></section>
<p class="byline">עודכן בנובמבר 2026.</p>''')

for f in ("favicon.svg","favicon-48.png","apple-touch-icon.png"): shutil.copy(SRC+"/"+f,OUT)
shutil.copy(SRC+"/style.css",OUT); shutil.copy(SRC+"/main.js",OUT)
open(OUT+"/.htaccess","w").write('''AddDefaultCharset UTF-8
<IfModule mod_rewrite.c>
RewriteEngine On
RewriteCond %{HTTPS} off [OR]
RewriteCond %{HTTP_HOST} ^www\\. [NC]
RewriteRule ^ https://tallawyer.com%{REQUEST_URI} [L,R=301]
RewriteCond %{THE_REQUEST} \\s/index\\.html[\\s?] [NC]
RewriteRule ^index\\.html$ / [L,R=301]
</IfModule>
AddType text/markdown;charset=UTF-8 .md
<IfModule mod_headers.c>
<FilesMatch "\\.(md|txt)$">
Header set X-Robots-Tag "noindex"
</FilesMatch>
</IfModule>
<IfModule mod_deflate.c>
AddOutputFilterByType DEFLATE text/html text/css application/javascript application/json
</IfModule>
<IfModule mod_expires.c>
ExpiresActive On
ExpiresByType image/webp "access plus 1 year"
ExpiresByType text/css "access plus 1 month"
ExpiresByType application/javascript "access plus 1 month"
</IfModule>
''')
def md(p):
    o=[f"# {p['h1']}","",p["short"],""]
    for x in p["sections"]:
        o+=[f"## {x['h']}",""]
        for it in x["items"]:
            if isinstance(it,dict):
                o+=["| "+" | ".join(it["t"])+" |","|"+"---|"*len(it["t"])]+["| "+" | ".join(r)+" |" for r in it["r"]]+[""]
            elif isinstance(it,list): o+=[f"- {i}" for i in it]+[""]
            else: o+=[it,""]
    o+=["## שאלות נפוצות",""]
    for q,a in p["faqs"]: o+=[f"### {q}","",a,""]
    o+=["## הבסיס המשפטי",""]+[f"- {l}" for l in LAWS[LAW_OF.get(p["slug"],"med")]]+[""]
    if SOURCES.get(p["slug"]): o+=["### מקורות",""]+[f"- [{t}]({u})" for t,u in SOURCES[p["slug"]]]+[""]
    o+=["## שאלות נפוצות",""] if False else []
    o+=[f"נכתב על ידי עו\"ד טל אשכנזי (טל וולק אשכנזי). עודכן ב-10 בנובמבר 2026.",f"{NAME}, {ADDR}, טלפון {PHONE}. מידע כללי שאינו ייעוץ משפטי.",""]
    open(f"{OUT}/{p['slug']}.md","w",encoding="utf-8").write("\n".join(o))
for p in SERVICES+GUIDES: md(p)
def html2md(slug,title):
    h=open(f"{OUT}/{slug}.html",encoding="utf-8").read()
    m=re.search(r'<article class="prose">(.*?)</article>',h,re.S).group(1)
    m=re.sub(r"<details class='q'><summary>(.*?)</summary><p>(.*?)</p></details>",r"\n## \1\n\n\2\n",m,flags=re.S)
    m=re.sub(r"<h2[^>]*>(.*?)</h2>",r"\n## \1\n\n",m);m=re.sub(r"<li>(.*?)</li>",r"- \1\n",m,flags=re.S);m=re.sub(r"</p>","\n\n",m)
    m=re.sub(r'<a [^>]*href="([^"]+)"[^>]*>(.*?)</a>',lambda g:f"[{g.group(2)}]({g.group(1).replace('.html','.md')})" if g.group(1).endswith('.html') else g.group(2),m)
    m=html.unescape(re.sub(r"<[^>]+>","",m));m=re.sub(r"\n{3,}","\n\n",m).strip()
    open(f"{OUT}/{slug}.md","w",encoding="utf-8").write(f"# {title}\n\n{m}\n")
for sl,ti in [("personal-injury","עורכת דין נזקי גוף"),("about",'אודות עו"ד טל אשכנזי'),("faq","שאלות ותשובות"),("contact","צרו קשר"),("accessibility","הצהרת נגישות"),("privacy","מדיניות פרטיות")]: html2md(sl,ti)
open(OUT+"/index.md","w",encoding="utf-8").write(f"# {NAME}\n\nעו\"ד טל אשכנזי (טל וולק אשכנזי) עוסקת ברשלנות רפואית ונזקי גוף, עם 5 שנות ניסיון. {ADDR}. טלפון {PHONE}. בדיקה ראשונית ללא עלות, ושכר טרחה רק במקרה של פיצוי. מלווה לקוחות מכל הארץ.\n\n## תחומי עיסוק\n\n"+"\n".join(f"- [{p['h1']}]({p['slug']}.md)" for p in SERVICES)+"\n\n## שאלות נפוצות\n\n"+"\n\n".join(f"### {q}\n\n{a}" for q,a in GENERAL_FAQ[:5])+"\n\nמפת התוכן: [sitemap.md](sitemap.md)\n")
def lst(a): return [f"- [{p['h1']}]({p['slug']}.md)" for p in a]
open(OUT+"/sitemap.md","w",encoding="utf-8").write("\n".join([f"# מפת תוכן: {NAME}","","- [דף הבית](index.md)","- [אודות](about.md)","- [שאלות ותשובות](faq.md)","- [צרו קשר](contact.md)","","## רשלנות רפואית",""]+lst(med)+["","## נזקי גוף וביטוח","","- [עורכת דין נזקי גוף: סקירה](personal-injury.md)"]+lst(oth)+["","## מדריכים",""]+lst(GUIDES)+["","## מדיניות","","- [הצהרת נגישות](accessibility.md)","- [מדיניות פרטיות](privacy.md)",""]))
U=SITE_URL+"/" if SITE_URL else ""
llm=[f"# {NAME}","",f"> עו\"ד טל אשכנזי (טל וולק אשכנזי), עורכת דין העוסקת ברשלנות רפואית ונזקי גוף, עם 5 שנות ניסיון, מספר רישיון 90780. {ADDR}. טלפון {PHONE}. מלווה לקוחות מכל הארץ.","","## רשלנות רפואית"]+[f"- [{s['h1']}]({U}{s['slug']}.md): {s['short']}" for s in med]+["","## נזקי גוף וביטוח",f"- [עורכת דין נזקי גוף]({U}personal-injury.md): ממי מבקשים פיצוי לפי סוג הפגיעה."]+[f"- [{s['h1']}]({U}{s['slug']}.md): {s['short']}" for s in oth]+["","## מדריכים"]+[f"- [{s['h1']}]({U}{s['slug']}.md): {s['short']}" for s in GUIDES]+["","## המשרד",f"- [אודות]({U}about.md)",f"- [שאלות ותשובות]({U}faq.md)",f"- [צרו קשר]({U}contact.md)","",f"מפת התוכן המלאה: [sitemap.md]({U}sitemap.md). לכל דף באתר יש גרסת HTML באותו שם עם הסיומת html."]
open(OUT+"/llms.txt","w",encoding="utf-8").write("\n".join(llm))
if SITE_URL:
    pg=[f[:-5] for f in sorted(os.listdir(OUT)) if f.endswith(".html") and f!="thanks.html"]
    open(OUT+"/sitemap.xml","w").write('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+"".join(f"<url><loc>{SITE_URL}/{'' if p=='index' else p+'.html'}</loc></url>" for p in pg)+"</urlset>")
    open(OUT+"/robots.txt","w").write(f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n# גרסאות טקסט ומפת תוכן: {SITE_URL}/sitemap.md\n")
else:
    open(OUT+"/robots.txt","w").write("# גרסאות טקסט ומפת תוכן: /sitemap.md, /llms.txt\nUser-agent: *\nAllow: /\n")
print(len([f for f in os.listdir(OUT) if f.endswith('.html')]),"pages")
