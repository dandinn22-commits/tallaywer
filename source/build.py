# -*- coding: utf-8 -*-
import json, os, shutil, html, re, zipfile
from PIL import Image
from content import SERVICES, GUIDES, GENERAL_FAQ, S
from icons import icon

SITE_URL = ""  # למלא כשקונים דומיין, למשל https://www.example.co.il
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
IMG={'hero': 'https://d8j0ntlcm91z4.cloudfront.net/user_3H6cRkwQ6uQLwjaqbyllL7c66jQ/hf_20261108_220658_579aa66f-ca85-48eb-b65b-7d10efd397d1.png', 'surgery': 'https://d8j0ntlcm91z4.cloudfront.net/user_3H6cRkwQ6uQLwjaqbyllL7c66jQ/hf_20261108_220657_2a9c48b2-3330-4bde-b8f0-54946a11968c.png', 'birth': 'https://d8j0ntlcm91z4.cloudfront.net/user_3H6cRkwQ6uQLwjaqbyllL7c66jQ/hf_20261108_220657_eb4efde8-f206-4258-98db-0bf87e3d7960.png', 'dental': 'https://d8j0ntlcm91z4.cloudfront.net/user_3H6cRkwQ6uQLwjaqbyllL7c66jQ/hf_20261108_220658_b0b6d77f-8a61-47c2-9d02-3e4a4e5c4857.png', 'eye': 'https://d8j0ntlcm91z4.cloudfront.net/user_3H6cRkwQ6uQLwjaqbyllL7c66jQ/hf_20261108_220656_7ba49e89-9882-4cd8-b87e-a7b93c99ed71.png', 'xray': 'https://d8j0ntlcm91z4.cloudfront.net/user_3H6cRkwQ6uQLwjaqbyllL7c66jQ/hf_20261108_220659_15d106b9-0ded-4702-b0b8-793108179164.png', 'road': 'https://d8j0ntlcm91z4.cloudfront.net/user_3H6cRkwQ6uQLwjaqbyllL7c66jQ/hf_20261108_220659_7e0eb5b5-3b9b-46d1-8dd4-c3433c49cd89.png', 'work': 'https://d8j0ntlcm91z4.cloudfront.net/user_3H6cRkwQ6uQLwjaqbyllL7c66jQ/hf_20261108_220658_08d409c5-e5c1-4626-a0e2-73da3a581889.png', 'insurance': 'https://d8j0ntlcm91z4.cloudfront.net/user_3H6cRkwQ6uQLwjaqbyllL7c66jQ/hf_20261108_220659_d67ca733-303c-4c5d-af9f-0e1e366ffbfb.png', 'office': 'https://d8j0ntlcm91z4.cloudfront.net/user_3H6cRkwQ6uQLwjaqbyllL7c66jQ/hf_20261108_220659_c3e62258-5c4c-40e9-be9f-685bcb2e969e.png'}
def has(n): return n in IMG
def url(n): return IMG[n]

ICON_PHONE = '<svg aria-hidden="true" viewBox="0 0 24 24" width="18" height="18" fill="currentColor"><path d="M6.6 10.8a15 15 0 0 0 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.100.4 2.300.6 3.600.6.600 0 1 .4 1 1V20c0 .6-.4 1-1 1C10.600 21 3 13.400 3 4c0-.6.400-1 1-1h3.500c.6 0 1 .4 1 1 0 1.300.2 2.500.6 3.600.1.300 0 .7-.2 1z"/></svg>'
ICON_WA = '<svg aria-hidden="true" viewBox="0 0 24 24" width="18" height="18" fill="currentColor"><path d="M12 2a10 10 0 0 0-8.600 15l-1.300 4.800 4.900-1.300A10 10 0 1 0 12 2zm5.800 14.200c-.2.700-1.400 1.300-2 1.400-.5.100-1.200.1-1.900-.1-.4-.1-1-.3-1.800-.7-3.100-1.300-5.100-4.400-5.300-4.600-.2-.2-1.300-1.700-1.300-3.200s.8-2.300 1.100-2.600c.3-.3.600-.4.800-.4h.6c.2 0 .4 0 .6.500l.9 2.100c.1.200.1.300 0 .5l-.3.500-.4.500c-.1.100-.3.300-.1.600.2.300.8 1.300 1.700 2.100 1.200 1 2.100 1.400 2.400 1.500.3.100.5.100.7-.1l.9-1.100c.2-.3.400-.2.700-.1l2 1c.3.100.5.200.5.300.100.100.100.700-.1 1.400z"/></svg>'

med = [s for s in SERVICES if s["group"] == "med"]
oth = [s for s in SERVICES if s["group"] == "other"]

def head(title, desc, slug, schema, noindex=False):
    canon = f'<link rel="canonical" href="{SITE_URL}/{"" if slug=="index" else slug+".html"}">\n<meta property="og:url" content="{SITE_URL}/{"" if slug=="index" else slug+".html"}">' if SITE_URL else ""
    img = f'<meta property="og:image" content="{SITE_URL}/assets/hero.webp">' if SITE_URL else ""
    g = f'<script async src="https://www.googletagmanager.com/gtag/js?id={GTAG}"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag("js",new Date());gtag("config","{GTAG}");</script>' if GTAG else ""
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
<a class="logo" href="index.html"><span class="logo-t"><strong>טל אשכנזי</strong><span>משרד עורכי דין</span></span></a>
<button class="menu-btn" aria-expanded="false" aria-controls="nav">תפריט</button>
<nav id="nav" aria-label="ראשי"><ul class="top">
<li class="has"><a href="medical-malpractice.html">רשלנות רפואית</a><ul class="drop">{links(med)}</ul></li>
<li class="has"><a href="road-accidents.html">נזקי גוף וביטוח</a><ul class="drop">{links(oth)}</ul></li>
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
    if topic: opts = f'<option selected>{e(topic)}</option>' + opts
    return f'''<form class="lead" data-lead novalidate>
<h2 class="lead-h">{title}</h2><p class="lead-sub">{sub}</p>
<label for="n{i}">שם מלא</label><input id="n{i}" name="name" autocomplete="name" required>
<label for="p{i}">טלפון</label><input id="p{i}" name="phone" type="tel" inputmode="tel" autocomplete="tel" dir="ltr" required>
<label for="t{i}">במה מדובר?</label><select id="t{i}" name="topic">{opts}</select>
<p class="err" role="alert" hidden></p>
<button class="btn gold" type="submit">לבדיקת התיק</button>
<p class="fine">הפרטים נשלחים בוואטסאפ לעו"ד טל אשכנזי. אין צורך לפרט מידע רפואי בשלב זה. <a href="privacy.html">מדיניות פרטיות</a></p>
</form>'''

def foot():
    return f'''</main>
<section class="final"><div class="wrap final-in"><div><p class="f-k">שיחת ייעוץ ראשונית ללא עלות</p><h2>דברו ישירות עם עו"ד טל אשכנזי</h2></div>
<div class="f-act"><a class="f-phone" href="tel:{PHONE_INTL}" data-ev="call" dir="ltr">{PHONE}</a><a class="btn gold" href="https://wa.me/{WA}" target="_blank" rel="noopener" data-ev="whatsapp">{ICON_WA}כתבו בוואטסאפ</a></div></div></section>
<footer class="foot"><div class="wrap cols">
<div><p class="f-name">{NAME}</p><p>{ADDR}</p><p>טלפון: <a href="tel:{PHONE_INTL}" dir="ltr">{PHONE}</a></p></div>
<div><h3>רשלנות רפואית</h3><ul>{links(med[:6])}</ul></div>
<div><h3>נזקי גוף וביטוח</h3><ul>{links(oth)}</ul></div>
<div><h3>המשרד</h3><ul><li><a href="about.html">אודות</a></li><li><a href="guides.html">מדריכים</a></li><li><a href="faq.html">שאלות ותשובות</a></li><li><a href="contact.html">צרו קשר</a></li><li><a href="accessibility.html">הצהרת נגישות</a></li><li><a href="privacy.html">מדיניות פרטיות</a></li></ul></div>
</div><p class="wrap legal">המידע באתר הוא מידע כללי ואינו מהווה ייעוץ משפטי או תחליף לבדיקת המקרה הפרטני. פרסום זה אינו מבטיח תוצאה.</p></footer>
<div class="mobile-bar"><a href="tel:{PHONE_INTL}" data-ev="call">{ICON_PHONE}חייגו עכשיו</a><a class="wa" href="https://wa.me/{WA}" target="_blank" rel="noopener" data-ev="whatsapp">{ICON_WA}וואטסאפ</a></div>
<script src="main.js"></script>
</body></html>'''

BIZ = {"@type":"LegalService","@id":"#office","name":NAME,"telephone":PHONE_INTL,
 "address":{"@type":"PostalAddress","streetAddress":"כצנלסון 97","addressLocality":"גבעתיים","addressCountry":"IL"},
 "areaServed":{"@type":"Country","name":"ישראל"},"knowsLanguage":"he",
 "employee":{"@type":"Person","name":"טל אשכנזי","jobTitle":"עורכת דין"},
 "knowsAbout":["רשלנות רפואית","נזקי גוף","תאונות דרכים","תאונות עבודה","ביטוח לאומי","אובדן כושר עבודה","תביעות ביטוח"]}
if SITE_URL: BIZ["url"] = SITE_URL + "/"

def crumbs_ld(trail):
    items = [{"@type":"ListItem","position":i+1,"name":n} | ({"item":f"{SITE_URL}/{u}"} if SITE_URL and u else {}) for i,(n,u) in enumerate(trail)]
    return {"@type":"BreadcrumbList","itemListElement":items}
def faq_ld(faqs):
    return {"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faqs]}
def graph(*x): return {"@context":"https://schema.org","@graph":list(x)}

def render_items(items):
    o = ""
    for it in items:
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
    parent = ("רשלנות רפואית","medical-malpractice.html") if s.get("group")=="med" else (("נזקי גוף וביטוח","road-accidents.html") if kind=="service" else ("מדריכים","guides.html"))
    trail=[("ראשי","index.html")]
    if s["slug"]!="medical-malpractice": trail.append(parent)
    trail.append((s["h1"],""))
    ld = graph(BIZ, crumbs_ld(trail), faq_ld(s["faqs"]),
      ({"@type":"Article","headline":s["h1"],"description":s["desc"],"author":{"@type":"Person","name":"טל אשכנזי"},"dateModified":"2026-11-09","inLanguage":"he"} if kind=="guide" else {"@type":"Service","name":s["h1"],"serviceType":s["kw"],"provider":{"@id":"#office"},"areaServed":"ישראל"}))
    bc = "".join((f'<a href="{u}">{e(n)}</a><span>/</span>' if u else f'<span aria-current="page">{e(n)}</span>') for n,u in trail)
    secs = "".join(f"<section><h2>{e(x['h'])}</h2>{render_items(x['items'])}</section>" for x in s["sections"])
    pool = (med if s.get("group")=="med" else oth if s.get("group") else GUIDES)
    rel = [x for x in pool if x["slug"]!=s["slug"]][:3]
    relh = "".join(f'<a class="rel" href="{x["slug"]}.html">{icon(x["slug"])}<strong>{e(x["menu"])}</strong><span>{e(x["card"])}</span></a>' for x in rel)
    body = head(s["title"],s["desc"],s["slug"],ld)+nav()+f'''<div class="page-hero"{f""" style="--img:url({url(s['img'])})" """ if has(s["img"]) else ""}>{"" if has(s["img"]) else icon(s["slug"],"ph-icon")}<div class="wrap ph">
<nav class="crumbs" aria-label="מיקום">{bc}</nav><p class="eyebrow">{e(s["eyebrow"])}</p><h1>{e(s["h1"])}</h1>
<div class="actions"><a class="btn gold" href="tel:{PHONE_INTL}" data-ev="call">{ICON_PHONE}<span dir="ltr">{PHONE}</span></a><a class="btn line" href="https://wa.me/{WA}" target="_blank" rel="noopener" data-ev="whatsapp">{ICON_WA}וואטסאפ</a></div>
<p class="trust">בדיקה ראשונית ללא עלות · שכר טרחה רק אם מתקבל פיצוי</p></div></div>
<div class="wrap layout"><article class="prose">
<div class="answer"><h2>בקצרה</h2><p>{e(s["short"])}</p></div>{calc() if s.get("calc") else ""}{secs}
<section><h2>איך התהליך עובד</h2>{steps()}</section>
<section><h2>שאלות נפוצות</h2>{faq_html(s["faqs"])}</section>
<p class="byline">נכתב על ידי {NAME}. עודכן בנובמבר 2026.</p>
</article><aside class="side">{form(topic=s["eyebrow"])}</aside></div>
<section class="wrap related"><h2>נושאים קשורים</h2><div class="rel-g">{relh}</div></section>
'''+foot()
    open(f'{OUT}/{s["slug"]}.html','w',encoding='utf-8').write(body)

def simple(slug,title,desc,h1,content,noindex=False,ld=None,with_form=False):
    b=head(title,desc,slug,ld or graph(BIZ,crumbs_ld([("ראשי","index.html"),(h1,"")])),noindex)+nav()
    aside=f'<aside class="side">{form()}</aside>' if with_form else ''
    b+=f'<div class="plain-head">{icon("contact" if slug=="contact" else "insurance-claims","ph-icon")}<div class="wrap"><h1>{e(h1)}</h1></div></div><div class="wrap {"layout" if with_form else "narrow"}"><article class="prose">{content}</article>{aside}</div>'+foot()
    open(f'{OUT}/{slug}.html','w',encoding='utf-8').write(b)

for s in SERVICES: service_page(s,"service")
for g in GUIDES: service_page(g,"guide")

def columns():
    o='<svg class="cols-art" aria-hidden="true" viewBox="0 0 520 620" fill="none" stroke="currentColor" stroke-width="1">'
    o+='<path d="M10 40H510M10 54H510M24 78H496M24 66H496"/>'
    for x in range(44,520,108):
        o+=f'<path d="M{x-24} 78h48l-6 18h-36zM{x-18} 96V570M{x+18} 96V570M{x-26} 570h52v18h-52z"/>'
        for d in (-9,0,9): o+=f'<path d="M{x+d} 100V566"/>'
    return o+'<path d="M0 588H520M0 606H520"/></svg>'
def tiles(items): return '<div class="tiles">'+"".join(f'<a class="tile" href="{h}.html"><img src="{url(i)}" alt="{e(a)}" loading="lazy"><span>{e(t)}</span></a>' for i,h,t,a in items)+'</div>'
# דף הבית
def cells(lst): return "".join(f'<a class="cell" href="{s["slug"]}.html">{icon(s["slug"])}<h3>{e(s["menu"])}</h3><p>{e(s["card"])}</p><span class="go">קראו עוד</span></a>' for s in lst)
home_faq=GENERAL_FAQ[:5]
home=head('עורכת דין רשלנות רפואית ונזקי גוף | עו"ד טל אשכנזי, גבעתיים','עו"ד טל אשכנזי מלווה נפגעי רשלנות רפואית, תאונות וביטוח. בדיקה ראשונית ללא עלות, שכר טרחה רק אם מתקבל פיצוי. כצנלסון 97 גבעתיים. 053-619-9967.','index',graph(BIZ,faq_ld(home_faq),{"@type":"WebSite","name":NAME,"inLanguage":"he"}))+nav()
PULSE='<svg class="pulse" aria-hidden="true" viewBox="0 0 1440 130" preserveAspectRatio="none" fill="none"><path pathLength="1" vector-effect="non-scaling-stroke" d="M0 86H470l16-10 16 10h26l12 18 20-96 20 116 14-38h30l18-14 18 14H1440"/></svg>'
ruler=lambda n,lbl:f'<div class="r"><span class="r-l">{lbl}</span><div class="r-t"><i style="width:{n*10}%"></i></div><b>{n}</b></div>'
axis="".join(f'<span style="right:{k*10}%">{k}</span>' for k in range(0,11))
hero_visual=f'<img class="hero-photo" src="{url("hero")}" alt="שולחן עבודה עם תיקים משפטיים וצילום רנטגן" fetchpriority="high">'
statement=('<img class="portrait" src="assets/tal.webp" alt="עו&quot;ד טל אשכנזי" loading="lazy">' if PORTRAIT else f'<div class="plate"><img src="{url("office")}" alt="חדר ישיבות עם ספרי משפט" loading="lazy"></div>')
home+=f'''<section class="hero"><div class="wrap hero-g"><div class="hero-t">
<p class="kicker">{NAME} · גבעתיים</p>
<h1>עורכת דין<br><em>רשלנות רפואית</em><br>ונזקי גוף</h1>
<p class="lede">נפגעתם מטיפול רפואי או בתאונה? אבדוק את התיק באופן אישי, אסביר מה האפשרויות ואלווה אתכם עד סיום ההליך.</p>
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

aboutc=f'''<div class="answer"><p>עו"ד טל אשכנזי עוסקת בתביעות רשלנות רפואית ונזקי גוף, עם חמש שנות ניסיון. המשרד נמצא בכצנלסון 97 בגבעתיים ומלווה לקוחות מכל הארץ.</p></div>
<section><h2>למה בחרתי בתחום</h2><p>אנשים מגיעים אליי אחרי תקופה קשה, ובדרך כלל בלי לדעת אם מה שקרה להם הוא טעות או גזירת גורל. התפקיד שלי מתחיל בלברר את זה ביושר.</p></section>
<section><h2>איך אני עובדת</h2><ul class="ticks"><li>בודקת כל תיק בעצמי ואומרת מה הסיכויים, גם כשהם נמוכים</li><li>מסבירה בשפה פשוטה את כל שלבי ההליך</li><li>מעדכנת באופן שוטף</li><li>פועלת עם רופאים מומחים לפי תחום המקרה</li><li>מגדירה מראש בכתב את שכר הטרחה ואת ההוצאות</li></ul></section>
<section><h2>תחומי עיסוק</h2><ul class="ticks"><li><a href="medical-malpractice.html">רשלנות רפואית</a></li><li><a href="road-accidents.html">תאונות דרכים</a></li><li><a href="work-accidents.html">תאונות עבודה</a></li><li><a href="national-insurance.html">ביטוח לאומי</a></li><li><a href="disability-insurance.html">אובדן כושר עבודה</a></li><li><a href="insurance-claims.html">תביעות ביטוח</a></li></ul></section>'''
simple("about",'אודות עו"ד טל אשכנזי | רשלנות רפואית ונזקי גוף','עו"ד טל אשכנזי, 5 שנות ניסיון ברשלנות רפואית ונזקי גוף. יחס אישי, הסברים ברורים. כצנלסון 97, גבעתיים.','אודות עו"ד טל אשכנזי',aboutc,with_form=True)

simple("faq",'שאלות ותשובות על רשלנות רפואית ונזקי גוף | עו"ד טל אשכנזי','תשובות לשאלות נפוצות על תביעות רשלנות רפואית, שכר טרחה, התיישנות ותהליך העבודה.','שאלות ותשובות',faq_html(GENERAL_FAQ),ld=graph(BIZ,faq_ld(GENERAL_FAQ)),with_form=True)

gl="".join(f'<a class="rel" href="{x["slug"]}.html">{icon(x["slug"])}<strong>{e(x["h1"])}</strong><span>{e(x["card"])}</span></a>' for x in GUIDES)
simple("guides",'מדריכים לנפגעי רשלנות רפואית | עו"ד טל אשכנזי','מדריכים בשפה פשוטה: התיישנות, חוות דעת רפואית ואיך מקבלים תיק רפואי.','מדריכים',f'<div class="rel-g">{gl}</div>')

cc=f'''<p class="big-phone"><a href="tel:{PHONE_INTL}" dir="ltr" data-ev="call">{PHONE}</a></p>
<ul class="ticks"><li>כתובת: {ADDR}</li><li>וואטסאפ: <a href="https://wa.me/{WA}" target="_blank" rel="noopener" data-ev="whatsapp">שלחו הודעה</a></li><li>פגישה במשרד בתיאום מראש</li></ul>
<p><a class="link" href="https://www.google.com/maps/search/?api=1&query=%D7%9B%D7%A6%D7%A0%D7%9C%D7%A1%D7%95%D7%9F+97+%D7%92%D7%91%D7%A2%D7%AA%D7%99%D7%99%D7%9D" target="_blank" rel="noopener">פתחו ניווט למשרד</a></p>'''
simple("contact",'צרו קשר | עו"ד טל אשכנזי, כצנלסון 97 גבעתיים','פנו לעו"ד טל אשכנזי לבדיקה ראשונית ללא עלות. טלפון 053-619-9967, כצנלסון 97, גבעתיים.','צרו קשר',cc,with_form=True)

simple("thanks",'תודה על פנייתכם | עו"ד טל אשכנזי','','תודה על פנייתכם',f'<p>אם הוואטסאפ לא נפתח, אפשר לשלוח הודעה ישירות או להתקשר:</p><div class="actions"><a class="btn gold" href="tel:{PHONE_INTL}" data-ev="call">{ICON_PHONE}<span dir="ltr">{PHONE}</span></a><a class="btn dark" href="https://wa.me/{WA}" target="_blank" rel="noopener" data-ev="whatsapp">{ICON_WA}וואטסאפ</a></div>',noindex=True)

simple("accessibility",'הצהרת נגישות | עו"ד טל אשכנזי','הצהרת נגישות של אתר עו"ד טל אשכנזי.','הצהרת נגישות',f'''<p>אנו פועלים כדי שהאתר יהיה נגיש לכלל הציבור, כולל אנשים עם מוגבלות.</p><section><h2>מה נעשה באתר</h2><ul class="ticks"><li>ניווט מלא במקלדת ודילוג לתוכן</li><li>מבנה כותרות מסודר</li><li>טקסט חלופי לתמונות בעלות תוכן</li><li>ניגודיות צבעים והתאמה לנייד</li></ul></section><section><h2>נתקלתם בקושי?</h2><p>אפשר לפנות אלינו בטלפון <a href="tel:{PHONE_INTL}" dir="ltr">{PHONE}</a> ונטפל בכך.</p><p>כתובת: {ADDR}.</p></section><p class="byline">עודכן בנובמבר 2026.</p>''')

simple("privacy",'מדיניות פרטיות | עו"ד טל אשכנזי','מדיניות הפרטיות של אתר עו"ד טל אשכנזי.','מדיניות פרטיות',f'''<section><h2>איזה מידע נאסף</h2><p>כשאתם ממלאים טופס נאספים שמכם, הטלפון שלכם והנושא שבחרתם. הטופס פותח הודעת וואטסאפ שאתם שולחים בעצמכם.</p></section><section><h2>למה המידע משמש</h2><p>כדי לחזור אליכם ולבדוק את פנייתכם. המידע נשמר בסודיות ולא נמכר לאחרים.</p></section><section><h2>מידע רפואי</h2><p>אין צורך למסור מידע רפואי דרך הטופס. פרטים רפואיים יימסרו בשיחה ישירה עם עורכת הדין.</p></section><section><h2>עוגיות ופרסום</h2><p>האתר עשוי להשתמש בכלים של גוגל למדידת ביצועים ופרסום. אפשר לחסום עוגיות בהגדרות הדפדפן.</p></section><section><h2>זכויותיכם</h2><p>אפשר לבקש לעיין במידע, לתקנו או למחקו בפנייה לטלפון <a href="tel:{PHONE_INTL}" dir="ltr">{PHONE}</a>.</p></section><p class="byline">עודכן בנובמבר 2026.</p>''')

shutil.copy(SRC+"/style.css",OUT); shutil.copy(SRC+"/main.js",OUT)
open(OUT+"/.htaccess","w").write('''AddDefaultCharset UTF-8
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
llm=[f"# {NAME}","",f"> עורכת דין העוסקת ברשלנות רפואית ונזקי גוף. {ADDR}. טלפון {PHONE}. 5 שנות ניסיון.","","## רשלנות רפואית"]+[f"- [{s['h1']}]({s['slug']}.html): {s['short']}" for s in med]+["","## נזקי גוף וביטוח"]+[f"- [{s['h1']}]({s['slug']}.html): {s['short']}" for s in oth]+["","## מדריכים"]+[f"- [{s['h1']}]({s['slug']}.html): {s['short']}" for s in GUIDES]
open(OUT+"/llms.txt","w",encoding="utf-8").write("\n".join(llm))
if SITE_URL:
    pg=[f[:-5] for f in sorted(os.listdir(OUT)) if f.endswith(".html") and f!="thanks.html"]
    open(OUT+"/sitemap.xml","w").write('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+"".join(f"<url><loc>{SITE_URL}/{'' if p=='index' else p+'.html'}</loc></url>" for p in pg)+"</urlset>")
    open(OUT+"/robots.txt","w").write(f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n")
else:
    open(OUT+"/robots.txt","w").write("User-agent: *\nAllow: /\n")
print(len([f for f in os.listdir(OUT) if f.endswith('.html')]),"pages")
