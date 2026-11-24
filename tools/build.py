#!/usr/bin/env python3
"""Builds the static obsessionmarketing.com site into OUT (plain HTML, relative links)."""
import html, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(HERE)
SITE = 'https://obsessionmarketing.com'
AUDIT = 'https://audit.obsessionmarketing.com/start'
LOGIN = 'https://app.obsessionmarketing.com/'
PHONE = '(833) 656-1801'
TEL = 'tel:+18336561801'
EMAIL = 'info@obsessionmarketing.com'
FB = 'https://www.facebook.com/obsessionmarketing/'
IG = 'https://instagram.com/obsessionmarketing'
FORM_ID = '8G4rHL1jZbVlZopkzWQj'  # GoHighLevel "Book A Call with Obsession Marketing"
CHAT_LOCATION_ID = 'aLQPWyAgpzpWVsa0xm9D'  # GoHighLevel location whose chat widget shows (the account on chris@obsessionmarketing.com); empty hides it
VER = '2'


def head(title, desc, path, root, noindex=False, extra=''):
    canon = f'{SITE}/{path}'
    robots = '<meta name="robots" content="noindex">' if noindex else ''
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{canon}">{robots}
<meta property="og:type" content="website"><meta property="og:site_name" content="Obsession Marketing">
<meta property="og:title" content="{html.escape(title)}"><meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{canon}"><meta property="og:image" content="{SITE}/assets/img/og.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#FAFAF7" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0B0B0A" media="(prefers-color-scheme: dark)">
<link rel="icon" href="{root}assets/img/favicon-32.png" sizes="32x32">
<link rel="apple-touch-icon" href="{root}assets/img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&family=Inter:wght@400;500;600&display=swap">
<link rel="stylesheet" href="{root}assets/site.css?v={VER}">
{extra}</head>
<body>
<a class="skip" href="#top">Skip to content</a>
'''


def logo(root, h=121):
    return (f'<img class="logo-l" src="{root}assets/img/logo-dark.png" alt="Obsession Marketing" width="520" height="{h}">'
            f'<img class="logo-d" src="{root}assets/img/logo-light.png" alt="Obsession Marketing" width="520" height="{h}">')


def header(root, home=False):
    a = '' if home else root
    return f'''<header>
  <div class="wrap nav">
    <a class="brand" href="{root}" aria-label="Obsession Marketing home">{logo(root)}</a>
    <ul>
      <li><a href="{a}#work">Work</a></li>
      <li><a href="{a}#services">Services</a></li>
      <li><a href="{a}#how">How it works</a></li>
      <li><a href="{LOGIN}">Client login</a></li>
    </ul>
    <a class="btn btn-gold" href="{AUDIT}">Free audit</a>
  </div>
</header>
'''


def footer(root):
    chat = ''
    if CHAT_LOCATION_ID:
        chat = (f'<chat-widget location-id="{CHAT_LOCATION_ID}" prompt-msg="Let\'s connect. Text us here." '
                f'revisit-prompt-msg="Welcome back, {{{{name}}}}. How can we help you today" use-email-field="true" '
                f'show-consent-checkbox="true" agency-name="Obsession Marketing" agency-website="https://obsessionmarketing.com"></chat-widget>\n'
                f'<script src="https://widgets.leadconnectorhq.com/loader.js" '
                f'data-resources-url="https://widgets.leadconnectorhq.com/chat-widget/loader.js" defer></script>\n')
    return f'''<footer>
  <div class="wrap foot">
    <a class="brand" href="{root}" aria-label="Obsession Marketing home">{logo(root)}</a>
    <a class="phone" href="{TEL}">{PHONE}</a>
    <div class="row"><a href="mailto:{EMAIL}">{EMAIL}</a><span>St. George, Utah</span></div>
    <div class="row"><a href="{LOGIN}">Client login</a><a href="{root}book-a-marketing-call/">Book a call</a><a href="{FB}" rel="noopener">Facebook</a><a href="{IG}" rel="noopener">Instagram</a></div>
    <div class="row"><a href="{root}wpautoterms/privacy-policy/">Privacy Policy</a><a href="{root}wpautoterms/terms-and-conditions/">Terms &amp; Conditions</a></div>
    <small>&copy; 2026 Obsession Marketing</small>
  </div>
</footer>
<div class="mbar"><a class="btn btn-gold" href="{AUDIT}">Run my free AI audit</a></div>
{chat}</body>
</html>
'''


def shot(root, name, alt, cls='', eager=False, sizes='(max-width: 720px) 100vw, 900px'):
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return (f'<img src="{root}assets/img/{name}-1373.webp" '
            f'srcset="{root}assets/img/{name}-700.webp 700w, {root}assets/img/{name}-1373.webp 1373w" '
            f'sizes="{sizes}" width="1373" height="868" alt="{alt}" {load} decoding="async">')


def frame(root, name, label, alt, cls='', eager=False, sizes='(max-width: 720px) 100vw, 900px'):
    return (f'<div class="frame{(" " + cls) if cls else ""}"><div class="bar"><i></i><i></i><i></i><b>{label}</b></div>'
            f'{shot(root, name, alt, eager=eager, sizes=sizes)}</div>')


FAQ = [
    ('What does the free AI audit check?',
     'How ChatGPT, Gemini, Claude and Google see your business, including your Google reviews. You get a plain report with what to fix, emailed in about 10 to 15 minutes.'),
    ('Is the audit really free?', 'Yes. No card, and no call required. Read the report and decide from there.'),
    ('Is there a long-term contract?', 'No. Everything is month to month, so we keep earning your business.'),
    ('What kinds of businesses do you work with?',
     'Local businesses that want more customers, from gyms and training facilities to moving companies.'),
    ('Where are you located?', 'St. George, Utah. You work with a local team you can call.'),
]


def home():
    r = './'
    ld_org = {
        '@context': 'https://schema.org', '@type': 'ProfessionalService', '@id': SITE + '/#business',
        'name': 'Obsession Marketing', 'legalName': 'Elite Ventures DBA Obsession Marketing',
        'url': SITE + '/', 'logo': SITE + '/assets/img/icon-512.png', 'image': SITE + '/assets/img/og.jpg',
        'telephone': '+1-833-656-1801', 'email': EMAIL,
        'address': {'@type': 'PostalAddress', 'addressLocality': 'St. George', 'addressRegion': 'UT', 'addressCountry': 'US'},
        'areaServed': 'Southern Utah', 'sameAs': [FB, IG],
        'description': 'Websites, CRM, ads, SEO, AI search and reviews for local businesses, built and run as one system. Month to month.',
    }
    ld_faq = {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
        {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in FAQ]}
    extra = (f'<link rel="preload" as="image" href="assets/img/summit-1373.webp" '
             f'imagesrcset="assets/img/summit-700.webp 700w, assets/img/summit-1373.webp 1373w" imagesizes="(max-width: 720px) 100vw, 840px">\n'
             f'<script type="application/ld+json">{json.dumps(ld_org)}</script>\n'
             f'<script type="application/ld+json">{json.dumps(ld_faq)}</script>\n')
    faq = '\n'.join(f'        <details{" open" if i == 0 else ""}><summary>{q}</summary><p>{a}</p></details>'
                    for i, (q, a) in enumerate(FAQ))
    body = f'''<main id="top">
  <section class="hero center">
    <div class="wrap">
      <h1>More customers. <span>Less marketing</span> to manage.</h1>
      <p class="sub">Your website, CRM, ads, SEO and reviews, built and run as one system by a local team. Month to month.</p>
      <div class="ctas">
        <a class="btn btn-gold" href="{AUDIT}">Run my free AI audit</a>
        <a class="btn btn-ghost" href="{TEL}">Call {PHONE}</a>
      </div>
      <p class="micro">Free &middot; No card &middot; Report in about 15 minutes</p>
      <div class="proof">
        <div class="stars" aria-label="5 stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
        <q>Total gamechanger for any business.</q>
        <span>Taylor H., real estate</span>
      </div>
      <div class="stage">
        {frame(r, 'stg', 'stgsoccerskills.com', 'STG Soccer Skills website', 'side l', sizes='(max-width: 720px) 0px, 460px')}
        {frame(r, 'moves', 'Simple Moves', 'Simple Moves website', 'side r', sizes='(max-width: 720px) 0px, 460px')}
        {frame(r, 'summit', 'Summit Athletic Club', 'Summit Athletic Club website, built by Obsession Marketing', 'main', eager=True, sizes='(max-width: 720px) 100vw, 840px')}
      </div>
    </div>
  </section>

  <section class="trust center">
    <div class="wrap">
      <p>Trusted by local businesses across Southern Utah</p>
      <div class="names">
        <span>Summit Athletic Club</span><span>Simple Moves</span><span>STG Soccer Skills</span><span>Dixie Business Network</span><span>Bosso</span>
      </div>
    </div>
  </section>

  <section class="band center" id="audit">
    <div class="wrap">
      <div class="eyebrow">Free AI visibility audit</div>
      <h2>Your customers are asking AI who to hire. <span>Is it naming you?</span></h2>
      <p class="lede">We check how ChatGPT, Gemini, Claude and Google see your business, then send you a plain report on what to fix.</p>
      <div class="ai" role="img" aria-label="Example: someone asks an AI assistant who the best gym in St. George is">
        <div class="q"><span>Who's the best gym in St. George?</span></div>
        <div class="a"><strong>A few popular options in St. George are&hellip;</strong><br>
          <span class="you">Is your business on this list?</span>
        </div>
        <span class="ex">Example</span>
      </div>
      <div class="checks">
        <span class="pill">ChatGPT</span><span class="pill">Gemini</span><span class="pill">Claude</span><span class="pill">Google reviews</span>
      </div>
      <div class="ctas">
        <a class="btn btn-gold" href="{AUDIT}">Run my free AI audit</a>
      </div>
      <p class="micro">100% free &middot; No card, no call &middot; Emailed in 10 to 15 minutes</p>
    </div>
  </section>

  <section class="block" id="work">
    <div class="wrap">
      <div class="head center">
        <div class="eyebrow">Our work</div>
        <h2>Real businesses. Real sites.</h2>
        <p>Every site here was built by our team for a local client.</p>
      </div>
      <div class="work">
        <div class="tile wide">
          <div class="meta"><h3>Summit Athletic Club</h3><p>Gym &middot; Website, CRM and booking</p></div>
          {frame(r, 'summit', 'Summit Athletic Club', 'Summit Athletic Club website', sizes='(max-width: 760px) 100vw, 920px')}
        </div>
        <div class="tile">
          <div class="meta"><h3>STG Soccer Skills</h3><p>Indoor soccer training</p></div>
          {frame(r, 'stg', 'stgsoccerskills.com', 'STG Soccer Skills website', sizes='(max-width: 760px) 100vw, 500px')}
        </div>
        <div class="tile">
          <div class="meta"><h3>Simple Moves</h3><p>Moving company &middot; St. George</p></div>
          {frame(r, 'moves', 'Simple Moves', 'Simple Moves website', sizes='(max-width: 760px) 100vw, 500px')}
        </div>
      </div>
    </div>
  </section>

  <!--
    CLIENT RESULT: add one real, checked client result here, then delete the two comment lines around it.
    Use only numbers the client agreed to share. Example shape:

  <section class="block center" id="results" style="padding-top:0">
    <div class="wrap">
      <div class="eyebrow">Results</div>
      <h2 style="font-size:clamp(56px,9vw,112px);font-weight:800;margin-top:12px">+00%</h2>
      <p style="font-size:20px;color:var(--ink-2);margin-top:8px">What changed, in one line. <b style="color:var(--ink)">Client name</b>, business type</p>
    </div>
  </section>
  -->

  <section class="block" id="services" style="padding-top:0">
    <div class="wrap">
      <div class="head center">
        <div class="eyebrow">What we do</div>
        <h2>Everything that brings in customers. One team.</h2>
      </div>
      <div class="svc">
        <div class="card"><div class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="4" width="18" height="14" rx="2"/><path d="M3 8h18M8 21h8"/></svg></div><h3>Websites</h3><p>Fast, beautiful sites built to turn visitors into calls.</p></div>
        <div class="card"><div class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 12a8 8 0 0 1 14-5.3M20 12a8 8 0 0 1-14 5.3"/><path d="M18 3v4h-4M6 21v-4h4"/></svg></div><h3>CRM &amp; automation</h3><p>Every lead captured, followed up and booked for you.</p></div>
        <div class="card"><div class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg></div><h3>Ads, SEO &amp; AI search</h3><p>Found on Google, Meta and the AI tools people ask.</p></div>
        <div class="card"><div class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m12 3 2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1L3.2 9.5l6.1-.9z"/></svg></div><h3>Reviews &amp; social</h3><p>More five-star reviews and a feed that stays fresh.</p></div>
      </div>
      <p class="also">Plus photography, video and monthly reporting.</p>
    </div>
  </section>

  <section class="block" id="how" style="padding-top:0">
    <span id="process"></span>
    <div class="wrap">
      <div class="head center">
        <div class="eyebrow">How it works</div>
        <h2>Three steps. No guesswork.</h2>
      </div>
      <div class="steps">
        <div class="step"><div class="n">1</div><h3>Free audit</h3><p>See where you show up today and where customers slip away.</p></div>
        <div class="step"><div class="n">2</div><h3>We build your system</h3><p>Site, CRM, ads and reviews, connected and set up for you.</p></div>
        <div class="step"><div class="n">3</div><h3>More customers</h3><p>We run it month to month and keep improving what works.</p></div>
      </div>
    </div>
  </section>

  <section class="block quotes">
    <div class="wrap">
      <div class="bigq">
        <div class="stars" aria-label="5 stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
        <blockquote>&ldquo;They're saving me time on stuff I didn't want to deal with and making me more money at the same time.&rdquo;</blockquote>
        <p class="who"><b>Taylor H.</b> &middot; Real estate</p>
      </div>
      <div class="smallq">
        <figure><blockquote>&ldquo;They built my website and connected it to a CRM, and now my business is growing and running smoothly.&rdquo;</blockquote><p class="who"><b>Jeanette M.</b></p></figure>
        <figure><blockquote>&ldquo;They understood my business needs and helped with lead generation and precision process set-up.&rdquo;</blockquote><p class="who"><b>Jacob M.</b></p></figure>
      </div>
    </div>
  </section>

  <section class="block" id="faq">
    <div class="wrap">
      <div class="head center">
        <div class="eyebrow">Good to know</div>
        <h2>Questions, answered.</h2>
      </div>
      <div class="faq">
{faq}
      </div>
    </div>
  </section>

  <section class="final center">
    <div class="wrap">
      <img class="mark" src="assets/img/mark.png" alt="" width="192" height="192" loading="lazy">
      <h2>See what AI says about your business.</h2>
      <div class="ctas">
        <a class="btn btn-gold" href="{AUDIT}">Run my free AI audit</a>
      </div>
      <p class="micro">Month to month. No contracts. Prefer to talk? Call <a href="{TEL}">{PHONE}</a>.</p>
    </div>
  </section>
</main>
'''
    return (head('Obsession Marketing | More customers, less marketing to manage',
                 'Websites, CRM, ads, SEO, AI search and reviews for local businesses, built and run as one system by a St. George, Utah team. Month to month. Start with a free AI visibility audit.',
                 '', r, extra=extra) + header(r, home=True) + body + footer(r))


def book():
    r = '../'
    body = f'''<main id="top" class="page">
  <div class="wrap">
    <div class="head center">
      <div class="eyebrow">Book a call</div>
      <h1>Let's talk about your business.</h1>
      <p>Leave your details and our team will reach out to set a time.</p>
    </div>
    <div class="formcard">
      <iframe src="https://api.leadconnectorhq.com/widget/form/{FORM_ID}" id="inline-{FORM_ID}"
        data-layout="{{'id':'INLINE'}}" data-trigger-type="alwaysShow" data-trigger-value="" data-activation-type="alwaysActivated"
        data-activation-value="" data-deactivation-type="neverDeactivate" data-deactivation-value=""
        data-form-name="Book A Call with Obsession Marketing" data-height="760" data-layout-iframe-id="inline-{FORM_ID}"
        data-form-id="{FORM_ID}" title="Book A Call with Obsession Marketing"></iframe>
    </div>
    <p class="alt">Rather see where you stand first? <a href="{AUDIT}">Run the free AI audit</a></p>
    <p class="alt">Or call <a href="{TEL}">{PHONE}</a></p>
  </div>
</main>
<script src="https://link.msgsndr.com/js/form_embed.js"></script>
'''
    return (head('Book a call | Obsession Marketing',
                 'Book a call with Obsession Marketing, a local St. George, Utah team for websites, CRM, ads, SEO and reviews.',
                 'book-a-marketing-call/', r) + header(r) + body + footer(r))


def legal(title, src, path):
    r = '../../'
    out, in_list = [], False
    for line in open(os.path.join(HERE, src), encoding='utf-8').read().splitlines():
        if not line.strip():
            continue
        kind, text = line.split('|', 1)
        if kind != 'L' and in_list:
            out.append('</ul>'); in_list = False
        if kind == 'P':
            if text.startswith('Last updated:'):
                out.append(f'<p class="updated">{text}</p>')
            else:
                out.append(f'<p>{text}</p>')
        elif kind == 'H':
            out.append(f'<h2>{text}</h2>')
        elif kind == 'S':
            out.append(f'<h2 style="font-size:20px">{text}</h2>')
        elif kind == 'L':
            if not in_list:
                out.append('<ul>'); in_list = True
            out.append(f'<li>{text}</li>')
    if in_list:
        out.append('</ul>')
    # the first "updated" line sits under the title
    body_html = '\n'.join(out)
    body = f'''<main id="top" class="page">
  <div class="wrap legal">
    <h1>{title}</h1>
{body_html}
  </div>
</main>
'''
    return (head(f'{title} | Obsession Marketing', f'{title} for obsessionmarketing.com.', path, r)
            + header(r) + body + footer(r))


def legal_index():
    r = '../'
    body = f'''<main id="top" class="page">
  <div class="wrap">
    <div class="head center"><h1>Legal</h1></div>
    <div class="links">
      <a href="terms-and-conditions/">Terms and Conditions</a>
      <a href="privacy-policy/">Privacy Policy</a>
    </div>
  </div>
</main>
'''
    return head('Legal | Obsession Marketing', 'Terms and Conditions and Privacy Policy for obsessionmarketing.com.',
                'wpautoterms/', r) + header(r) + body + footer(r)


def redirect(target_rel, target_abs):
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Redirecting&hellip;</title>'
            f'<link rel="canonical" href="{SITE}/{target_abs}"><meta name="robots" content="noindex">'
            f'<meta http-equiv="refresh" content="0; url={target_rel}"></head>'
            f'<body><p><a href="{target_rel}">Continue</a></p>'
            f'<script>location.replace("{target_rel}")</script></body></html>\n')


def notfound():
    r = '/'
    body = f'''<main id="top" class="page nf">
  <div class="wrap center">
    <h1>404</h1>
    <div class="head"><h1 style="color:var(--ink);font-size:clamp(32px,4.4vw,48px);margin-top:8px">This page moved.</h1>
    <p>The page you're looking for isn't here anymore.</p></div>
    <div class="ctas"><a class="btn btn-gold" href="{AUDIT}">Run my free AI audit</a><a class="btn btn-ghost" href="/">Home</a></div>
  </div>
</main>
'''
    return head('Page not found | Obsession Marketing', 'Page not found.', '404.html', r, noindex=True) + header(r) + body + footer(r)


def write(rel, text):
    p = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, 'w', encoding='utf-8') as f:
        f.write(text)


write('index.html', home())
write('book-a-marketing-call/index.html', book())
write('wpautoterms/index.html', legal_index())
write('wpautoterms/privacy-policy/index.html', legal('Privacy Policy', 'privacy.txt', 'wpautoterms/privacy-policy/'))
write('wpautoterms/terms-and-conditions/index.html', legal('Terms and Conditions', 'terms.txt', 'wpautoterms/terms-and-conditions/'))
for slug, rel, ab in [('faqs', '../#faq', '#faq'), ('services', '../#services', '#services'),
                      ('about', '../', ''), ('new', '../', ''), ('sample-page', '../', ''),
                      ('payment-confirmation', '../', ''), ('payment-failed', '../', '')]:
    write(f'{slug}/index.html', redirect(rel, ab))
write('404.html', notfound())
write('.nojekyll', '')
# Preview stays out of search until launch: switch to "Allow: /" plus the Sitemap line at go-live.
write('robots.txt', 'User-agent: *\nAllow: /\n\nSitemap: https://obsessionmarketing.com/sitemap.xml\n')
write('CNAME', 'obsessionmarketing.com\n')
urls = ['', 'book-a-marketing-call/', 'wpautoterms/privacy-policy/', 'wpautoterms/terms-and-conditions/']
write('sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
      + ''.join(f'  <url><loc>{SITE}/{u}</loc><lastmod>2026-11-24</lastmod></url>\n' for u in urls) + '</urlset>\n')
print('built', OUT)
