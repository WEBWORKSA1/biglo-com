"""Build every Biglo page into the repo root. Usage: python3 _build/build.py"""
import os, sys, json, datetime
sys.path.insert(0, os.path.dirname(__file__))
from layout import page, ad, newsletter_band, page_hero, SITE
from guides import GUIDES

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TODAY = datetime.date.today().isoformat()
PAGES = {}


def out(name, html):
    PAGES[name] = html
    with open(os.path.join(ROOT, name), "w", encoding="utf-8") as f:
        f.write(html)


def form_hidden():
    return '<input class="hp" name="_honey" tabindex="-1" autocomplete="off">'


def faq_html(faq):
    return "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in faq)


def faq_schema(faq):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}


CATS = [("insurance", "🛡️", "Insurance"), ("internet", "📡", "Internet"), ("energy", "⚡", "Energy & Solar"),
        ("loans", "🏦", "Loans"), ("phone", "📱", "Phone"), ("moving", "🚚", "Moving")]


def quick_quote(title="What bill do you want to lower?"):
    pills = "".join(
        f'<button type="button" class="pill" data-type="{k}" aria-pressed="{"true" if k == "insurance" else "false"}"><span class="e">{e}</span>{l}</button>'
        for k, e, l in CATS)
    return f"""<form class="quote-box" data-quickquote aria-label="Start a free quote">
  <h2>{title}</h2><p class="muted mb0">Pick one. Free, no obligation, about 2 minutes.</p>
  <div class="pill-group">{pills}</div>
  <div class="field"><label for="hq-zip">ZIP / postal code</label><input id="hq-zip" name="zip" placeholder="e.g. 10001" autocomplete="postal-code" maxlength="10"></div>
  <button class="btn btn-primary btn-lg btn-block" type="submit">Get my free quotes →</button>
  <div class="secure"><span>🔒 Secure</span><span>🚫 No spam calls</span><span>🙅 Never sold</span></div>
</form>"""


# ------------------------------------------------------------------ HOME
guide_cards = "".join(
    f'<a class="card card-link reveal" href="guide-{g["slug"]}.html"><div class="ico">{g["emoji"]}</div><span class="badge">{g["cat"]} · {g["mins"]} min</span><h3 style="margin-top:10px">{g["title"]}</h3><p>{g["desc"]}</p></a>'
    for g in GUIDES[:3])
TOOLS = [("bills", "🧾", "Bill Savings Estimator", "See how much you could cut across 5 bills."),
         ("subs", "🔁", "Subscription Audit", "Find the zombie subscriptions draining you."),
         ("debt", "💳", "Debt Payoff", "Payoff date + what extra payments save."),
         ("loan", "🏦", "Loan & Refinance", "Monthly payment, total interest, refi savings."),
         ("solar", "☀️", "Solar Payback", "Years to break even and 25-year savings."),
         ("savings", "🎯", "Savings Goal", "What to save monthly to hit any goal."),
         ("budget", "📊", "50/30/20 Budget", "Split your income the smart way."),
         ("unit", "⚖️", "Unit Price Compare", "Which pack is actually cheaper?")]
tool_cards = "".join(
    f'<a class="card card-link reveal" href="tools.html#{k}"><div class="ico">{e}</div><h3>{t}</h3><p>{d}</p></a>' for k, e, t, d in TOOLS)

home = f"""
<section class="hero"><div class="container hero-grid">
  <div class="reveal">
    <span class="eyebrow">Big savings · Low bills</span>
    <h1>Pay less for <span class="hl">everything</span> you already buy.</h1>
    <p class="lead">Biglo finds lower rates on insurance, internet, energy and loans, tracks the best deals, and gives you free tools to keep more of every paycheck.</p>
    <div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:22px">
      <a class="btn btn-primary btn-lg" href="quotes.html">Lower my bills →</a>
      <a class="btn btn-ghost btn-lg" href="deals.html">See today's deals</a>
    </div>
    <div class="trust-row"><span>100% free to use</span><span>No obligation</span><span>We never sell your data</span><span>Real humans, no bots</span></div>
  </div>
  <div class="reveal">{quick_quote()}</div>
</div></section>

<section class="section-tight"><div class="container stats">
  <div class="stat"><b>6</b><span>bill categories we shop</span></div>
  <div class="stat"><b>8</b><span>free money calculators</span></div>
  <div class="stat"><b>$0</b><span>cost to you, always</span></div>
  <div class="stat"><b>2 min</b><span>to get matched</span></div>
</div></section>

{ad("header")}

<section><div class="container">
  <div class="section-head"><div><span class="eyebrow">🔥 Hand-picked</span><h2>Today's top deals</h2><p>Voted up by the community, checked by our editors.</p></div><a class="btn btn-ghost" href="deals.html">All deals →</a></div>
  <div class="grid g3" data-deals="6"></div>
</div></section>

<section class="alt"><div class="container">
  <div class="section-head"><div><span class="eyebrow">How it works</span><h2>Three steps to a lower bill</h2></div></div>
  <div class="grid g3 steps-3">
    <div class="card reveal"><h3>Tell us what you pay</h3><p>Answer a few quick questions — no account, no credit check.</p></div>
    <div class="card reveal"><h3>Compare real offers</h3><p>We match you with up to 3 providers that serve your area.</p></div>
    <div class="card reveal"><h3>Switch & save</h3><p>Pick the winner or keep what you have. Zero pressure.</p></div>
  </div>
  <div class="center mt"><a class="btn btn-primary btn-lg" href="quotes.html">Start saving — it's free</a></div>
</div></section>

<section><div class="container">
  <div class="section-head"><div><span class="eyebrow">Free tools</span><h2>Money calculators that do the math for you</h2></div><a class="btn btn-ghost" href="tools.html">All tools →</a></div>
  <div class="grid g4">{tool_cards}</div>
</div></section>

{ad("inContent")}

<section class="alt"><div class="container">
  <div class="section-head"><div><span class="eyebrow">▶ Watch & save</span><h2>Money-saving videos</h2><p>Short, practical videos from creators who live the frugal life.</p></div><a class="btn btn-ghost" href="videos.html">More videos →</a></div>
  <div class="grid g3" data-videos="3"></div>
</div></section>

<section><div class="container">
  <div class="section-head"><div><span class="eyebrow">Guides</span><h2>Money guides that pay for themselves</h2></div><a class="btn btn-ghost" href="guides.html">All guides →</a></div>
  <div class="grid g3">{guide_cards}</div>
</div></section>

<section class="alt"><div class="container grid g2" style="align-items:center">
  <div class="reveal"><span class="eyebrow">🎁 Giveaway</span><h2>Win $500 to knock out your bills</h2><p class="lead">Free to enter. Earn bonus entries by sharing, subscribing and watching. Winner drawn at random.</p><a class="btn btn-accent btn-lg" href="contests.html">Enter the giveaway →</a></div>
  <div class="card reveal"><h3>Ends in</h3><div class="countdown" id="countdown"></div><p class="form-note">No purchase necessary. <a href="contests.html#rules">Official rules</a>.</p></div>
</div></section>

<section><div class="container grid g3">
  <a class="card card-link reveal" href="support.html"><div class="ico">♥</div><h3>Support Biglo</h3><p>Keep the tools free and ad-light. Chip in once or monthly.</p></a>
  <a class="card card-link reveal" href="careers.html"><div class="ico">🚀</div><h3>Write, film, build with us</h3><p>We're hiring editors, video creators and deal hunters.</p></a>
  <a class="card card-link reveal" href="advertise.html"><div class="ico">📣</div><h3>Advertise / partner</h3><p>Reach savings-minded shoppers who are ready to switch.</p></a>
</div></section>

{newsletter_band()}
{ad("footer")}
"""
org = {"@context": "https://schema.org", "@type": "Organization", "name": "Biglo", "url": SITE, "logo": SITE + "/assets/img/favicon.svg"}
out("index.html", page("index.html", "Biglo — Big Savings, Low Bills | Deals, Quotes & Money Tools",
                       "Lower your bills and find the best deals. Free quotes on insurance, internet, energy and loans, plus money calculators, guides and videos.",
                       home, schema=[org]))

# ------------------------------------------------------------------ QUOTES (lead gen)
quotes = page_hero("Get lower quotes", "Lower your bills in <span style='color:var(--brand)'>2 minutes</span>.",
                   "Answer a few questions and we'll match you with up to 3 providers who serve your area. Free. No obligation. No spam calls.") + f"""
<section id="start" style="padding-top:20px"><div class="container">
  <div class="funnel card" id="funnel">
    <div style="display:flex;justify-content:space-between;align-items:center"><button class="btn btn-ghost btn-sm" id="funnel-back" type="button">← Back</button><span class="muted" id="funnel-count" style="font-weight:700;font-size:.9rem"></span></div>
    <div class="progress" aria-hidden="true"><i></i></div>
    <div id="funnel-body" aria-live="polite"></div>
  </div>
  <div class="secure" style="margin-top:22px"><span>🔒 Bank-level encryption</span><span>✅ Licensed partners only</span><span>🙅 We never sell your info</span><span>💬 Real humans, no bots</span></div>
</div></section>
<section class="alt"><div class="container">
  <div class="section-head"><div><span class="eyebrow">Why Biglo</span><h2>Built to save you money — not to spam you</h2></div></div>
  <div class="grid g4">
    <div class="card"><div class="ico">⏱️</div><h3>2-minute form</h3><p>Only the questions providers actually need to price you.</p></div>
    <div class="card"><div class="ico">🎯</div><h3>Max 3 matches</h3><p>Never blasted to dozens of companies. You stay in control.</p></div>
    <div class="card"><div class="ico">📉</div><h3>No credit impact</h3><p>Quotes use soft or no credit checks. Nothing is final until you say yes.</p></div>
    <div class="card"><div class="ico">💸</div><h3>Always free</h3><p>Partners pay us a referral fee. Your price is the same either way.</p></div>
  </div>
</div></section>
<section><div class="container">
  <div class="section-head"><div><span class="eyebrow">Browse by category</span><h2>What can Biglo lower?</h2></div></div>
  <div class="grid g3">""" + "".join(
    f'<a class="card card-link" href="quotes.html?type={k}#start"><div class="ico">{e}</div><h3>{l}</h3><p>Compare {l.lower()} offers from providers in your area.</p></a>' for k, e, l in CATS) + f"""</div>
</div></section>
<section class="alt"><div class="container" style="max-width:820px"><h2>Questions</h2>{faq_html([
    ("Is Biglo really free?", "Yes. Providers pay Biglo a referral fee when you choose them. It never changes your price."),
    ("Who will contact me?", "A Biglo savings specialist and up to 3 matched partners — only about the request you made."),
    ("Will this affect my credit score?", "No. Getting matched does not involve a hard credit check. Individual lenders will ask before any hard inquiry."),
    ("Can I opt out later?", "Anytime. Reply STOP to texts, unsubscribe from emails, or contact us and we'll delete your request.")])}</div></section>
{newsletter_band()}
"""
out("quotes.html", page("quotes.html", "Get Lower Quotes — Insurance, Internet, Energy, Loans | Biglo",
                        "Compare free, no-obligation quotes for insurance, internet, energy, solar, loans, phone plans and moving in about 2 minutes.",
                        quotes, "quotes.html"))

# ------------------------------------------------------------------ DEALS
deals = page_hero("Deals", "Today's best deals, voted by real shoppers.",
                  "Hand-checked prices, working codes and expiring offers. Upvote what's hot — the best rise to the top.") + f"""
<section style="padding-top:24px"><div class="container">
  <p class="disclosure">Biglo is reader-supported: when you buy through links we may earn a commission, at no cost to you. <span class="muted">Launch preview — listings shown are sample deals while our live feed is connected.</span></p>
  <div class="toolbar mt">
    <label class="sr-only" for="deal-q">Search deals</label><input id="deal-q" type="search" placeholder="Search deals, stores, categories…">
    <label class="sr-only" for="deal-sort">Sort</label><select id="deal-sort"><option value="popular">Most popular</option><option value="new">Newest</option><option value="ending">Ending soon</option><option value="discount">Biggest discount</option></select>
    <label class="sr-only" for="deal-tag">Filter</label><select id="deal-tag"><option value="">All deal types</option><option value="staff">Staff picks</option><option value="exclusive">Biglo exclusives</option><option value="hot">Hot right now</option></select>
  </div>
  <div class="chips" id="deal-cats"></div>
  <p class="muted" id="deal-count" style="font-weight:700"></p>
  <div class="grid g4" id="deal-grid"></div>
</div></section>
{ad("inContent")}
<section class="alt"><div class="container grid g2">
  <div class="card"><h2>🔔 Deal Alerts</h2><p>Tell us what you're hunting for. We'll email you the moment it drops.</p>
    <form data-form="deal-alert" data-subject="Deal alert signup" data-success="Alert set! We'll email you when it drops.">{form_hidden()}
      <div class="field"><label for="da-k">Keyword or product</label><input id="da-k" name="Keyword" required placeholder="e.g. robot vacuum, 5G plan"></div>
      <div class="row2"><div class="field"><label for="da-p">Max price (optional)</label><input id="da-p" name="Max price" type="number" min="0"></div>
      <div class="field"><label for="da-e">Email</label><input id="da-e" name="Email" type="email" required></div></div>
      <button class="btn btn-primary" type="submit">Create alert</button></form></div>
  <div class="card"><h2>🕵️ Found a deal?</h2><p>Share it with the community. Top finders get featured and win monthly prizes.</p><a class="btn btn-accent" href="submit-deal.html">Submit a deal →</a>
    <h3 class="mt">Are you a brand?</h3><p>Get your offer in front of shoppers ready to buy.</p><a class="btn btn-ghost" href="advertise.html">Feature your deal</a></div>
</div></section>
{newsletter_band()}
"""
out("deals.html", page("deals.html", "Today's Best Deals & Promo Codes | Biglo",
                       "The best deals, coupons and promo codes today — voted up by shoppers and checked by editors. Tech, home, groceries, travel and more.",
                       deals, "deals.html"))

# ------------------------------------------------------------------ SUBMIT DEAL
submit = page_hero("Submit a deal", "Submit a deal", "Found a great price? Share it. Approved deals credit you by name, and the top finder each month wins a gift card.") + f"""
<section style="padding-top:20px"><div class="container" style="max-width:760px"><div class="card">
<form data-form="submit-deal" data-subject="Deal submission" data-success="Thanks! Our editors will review your deal within 24 hours.">{form_hidden()}
  <div class="field"><label for="sd-t">Deal title</label><input id="sd-t" name="Title" required placeholder="e.g. 6-qt air fryer $69 (was $129)"></div>
  <div class="field"><label for="sd-u">Link to the deal</label><input id="sd-u" name="URL" type="url" required placeholder="https://"></div>
  <div class="row2"><div class="field"><label for="sd-p">Deal price</label><input id="sd-p" name="Price" required></div><div class="field"><label for="sd-c">Promo code (if any)</label><input id="sd-c" name="Code"></div></div>
  <div class="row2"><div class="field"><label for="sd-cat">Category</label><select id="sd-cat" name="Category"><option>Tech</option><option>Home</option><option>Groceries</option><option>Fashion</option><option>Travel</option><option>Phone plans</option><option>Internet</option><option>Streaming</option><option>Other</option></select></div>
  <div class="field"><label for="sd-e">Expires</label><input id="sd-e" name="Expires" type="date"></div></div>
  <div class="field"><label for="sd-n">Why is it a great deal?</label><textarea id="sd-n" name="Notes"></textarea></div>
  <div class="row2"><div class="field"><label for="sd-nm">Your name / handle</label><input id="sd-nm" name="Name" required></div><div class="field"><label for="sd-em">Email</label><input id="sd-em" name="Email" type="email" required></div></div>
  <button class="btn btn-primary btn-lg" type="submit">Submit deal</button>
</form></div></div></section>"""
out("submit-deal.html", page("submit-deal.html", "Submit a Deal | Biglo", "Share a great deal with the Biglo community and get featured.", submit))

# ------------------------------------------------------------------ TOOLS
def inp(id_, label, val, step="1", pre=""):
    return f'<div class="field"><label for="{id_}">{label}</label><input id="{id_}" type="number" min="0" step="{step}" value="{val}" inputmode="decimal"></div>'


def res(title, big_id, rows, cta_type="", extra=""):
    dl = "".join(f"<dt>{a}</dt><dd id=\"{b}\">—</dd>" for a, b in rows)
    cta = f'<a class="btn btn-primary btn-block" href="quotes.html?type={cta_type}#start">Get real quotes for my area →</a>' if cta_type else '<a class="btn btn-primary btn-block" href="quotes.html">Find ways to lower my bills →</a>'
    return f'<div class="result" aria-live="polite"><div class="muted" style="font-weight:700">{title}</div><div class="big" id="{big_id}">—</div><dl>{dl}</dl>{extra}{cta}</div>'


tabs = "".join(f'<button type="button" class="chip{" active" if i == 0 else ""}" data-tool-tab="{k}" role="tab" aria-selected="{"true" if i == 0 else "false"}">{e} {t}</button>' for i, (k, e, t, d) in enumerate(TOOLS))
tools = page_hero("Tools", "Free money calculators", "Run the numbers before you switch, borrow or buy. Private — everything is calculated in your browser.") + f"""
<section style="padding-top:20px"><div class="container">
<div class="tool-tabs" role="tablist">{tabs}</div>
<div class="card">
 <div class="tool active" id="bills"><div><h2>🧾 Bill Savings Estimator</h2><p class="muted">Enter what you pay monthly. We apply typical savings people get by shopping around.</p>
  {inp("b-ins","Insurance (car + home) / month",180)}{inp("b-net","Internet / month",75)}{inp("b-phone","Phone plan(s) / month",110)}{inp("b-energy","Electricity & gas / month",160)}{inp("b-stream","Streaming & subscriptions / month",55)}</div>
  {res("Estimated yearly savings","bills-out",[("Per month","bills-mo"),("Over 5 years","bills-5")],"insurance",'<div class="bar-chart" id="bills-bars"></div><p class="form-note">Estimates use illustrative savings rates (insurance 18%, internet 25%, phone 35%, energy 12%, subscriptions 30%). Your results will vary.</p>')}</div>

 <div class="tool" id="subs"><div><h2>🔁 Subscription Audit</h2><p class="muted">Tick the ones you'd cancel.</p>
  <div class="sub-row muted" style="font-size:.8rem;font-weight:700"><span>Subscription</span><span>$/month</span><span>Cut</span></div>
  <div id="subs-list">""" + "".join(
    f'<div class="sub-row"><input aria-label="Subscription name" value="{n}"><input type="number" min="0" step="0.01" aria-label="Monthly cost" value="{v}"><input type="checkbox" aria-label="Cancel"{" checked" if c else ""}></div>'
    for n, v, c in [("Video streaming #1", 15.49, False), ("Video streaming #2", 17.99, True), ("Music", 10.99, False), ("Cloud storage", 2.99, False), ("Gym", 39.99, True), ("News / magazine", 12, True), ("App subscription", 6.99, False)]) + f"""</div>
  <button type="button" class="btn btn-ghost btn-sm" id="subs-add">+ Add subscription</button></div>
  {res("You'd save per year","subs-out",[("Current total","subs-total"),("Kept per year","subs-keep")])}</div>

 <div class="tool" id="debt"><div><h2>💳 Debt Payoff</h2>{inp("d-bal","Balance ($)",8000)}{inp("d-apr","APR (%)",22.9,"0.1")}{inp("d-pay","Monthly payment ($)",300)}</div>
  {res("Debt-free in","debt-out",[("Total interest","debt-int"),("Add $100/month","debt-extra")],"loans")}</div>

 <div class="tool" id="loan"><div><h2>🏦 Loan & Refinance</h2>{inp("l-amt","Loan amount ($)",250000)}{inp("l-rate","Interest rate (%)",6.8,"0.01")}{inp("l-years","Term (years)",30)}</div>
  {res("Monthly payment","loan-out",[("Total paid","loan-total"),("Total interest","loan-int"),("Savings if rate drops 1.5%","loan-refi")],"loans")}</div>

 <div class="tool" id="solar"><div><h2>☀️ Solar Payback</h2>{inp("so-bill","Average monthly electric bill ($)",180)}{inp("so-cost","System cost before incentives ($)",20000)}{inp("so-offset","% of bill offset by solar",85)}{inp("so-inc","Incentives / tax credits (%)",30)}</div>
  {res("Year-one savings","solar-out",[("Net system cost","solar-net"),("Payback","solar-pay"),("25-year net savings*","solar-life")],"energy",'<p class="form-note">*Assumes 3%/yr utility price increases. Check current incentives for your address.</p>')}</div>

 <div class="tool" id="savings"><div><h2>🎯 Savings Goal</h2>{inp("s-goal","Goal ($)",10000)}{inp("s-start","Already saved ($)",1000)}{inp("s-rate","Savings APY (%)",4,"0.1")}{inp("s-months","Months to goal",24)}</div>
  {res("Save per month","sav-out",[("Per week","sav-week"),("Interest earned","sav-int")])}</div>

 <div class="tool" id="budget"><div><h2>📊 50/30/20 Budget</h2>{inp("bu-inc","Monthly take-home pay ($)",5000)}<p class="muted">50% needs (rent, bills, groceries), 30% wants, 20% savings & debt payoff.</p></div>
  {res("Needs","bu-needs",[("Wants","bu-wants"),("Savings & debt","bu-save")],"",'<div class="bar-chart" id="bu-bars"></div>')}</div>

 <div class="tool" id="unit"><div><h2>⚖️ Unit Price Compare</h2><div class="row2">{inp("u-pa","Option A price ($)",12.99,"0.01")}{inp("u-qa","Option A quantity",24)}</div><div class="row2">{inp("u-pb","Option B price ($)",19.49,"0.01")}{inp("u-qb","Option B quantity",40)}</div></div>
  {res("Verdict","unit-out",[("A per unit","unit-a"),("B per unit","unit-b")])}</div>
</div>
<p class="form-note">Calculators are for education and estimates only — not financial advice.</p>
</div></section>
{ad("inContent")}
{newsletter_band()}
"""
out("tools.html", page("tools.html", "Free Money Calculators — Bills, Debt, Loans, Solar | Biglo",
                       "Free calculators: bill savings, subscription audit, debt payoff, loan & refinance, solar payback, savings goal, 50/30/20 budget and unit price.",
                       tools, "tools.html"))

# ------------------------------------------------------------------ GUIDES
cats = sorted(set(g["cat"] for g in GUIDES))
all_cards = "".join(
    f'<a class="card card-link reveal" href="guide-{g["slug"]}.html"><div class="ico">{g["emoji"]}</div><span class="badge">{g["cat"]} · {g["mins"]} min read</span><h3 style="margin-top:10px">{g["title"]}</h3><p>{g["desc"]}</p></a>'
    for g in GUIDES)
guides = page_hero("Guides", "Money guides that pay for themselves", "Clear, practical playbooks for cutting bills, killing debt and spending smarter. Updated regularly.") + f"""
<section style="padding-top:20px"><div class="container"><div class="grid g3">{all_cards}</div></div></section>
{ad("inContent")}
<section class="alt"><div class="container grid g2" style="align-items:center"><div><h2>Want to write for Biglo?</h2><p class="lead">We pay freelance writers and subject experts. Pitch us a guide.</p></div><div><a class="btn btn-primary btn-lg" href="careers.html#apply">Pitch a guide →</a></div></div></section>
{newsletter_band()}"""
out("guides.html", page("guides.html", "Money-Saving Guides | Biglo", "Step-by-step guides to lower your bills, insurance, internet, energy and debt costs.", guides, "guides.html"))

for g in GUIDES:
    toc = "".join(f'<li><a href="#s{i}">{h}</a></li>' for i, (h, _) in enumerate(g["sections"]))
    secs = ""
    for i, (h, b) in enumerate(g["sections"]):
        secs += f'<h2 id="s{i}">{i + 1}. {h}</h2>' + b.replace("../", "")
        if i == 2:
            secs += ad("inContent")
        if i == 4 and g["cta"]:
            secs += f'<div class="card" style="margin:24px 0;background:var(--brand-soft)"><h3>💡 See what you could save</h3><p>Compare free quotes from providers in your area — about 2 minutes, no obligation.</p><a class="btn btn-primary" href="quotes.html?type={g["cta"]}#start">Get my free quotes →</a></div>'
    related = "".join(f'<a class="card card-link" href="guide-{r["slug"]}.html"><div class="ico">{r["emoji"]}</div><h3>{r["title"]}</h3></a>' for r in [x for x in GUIDES if x is not g][:3])
    body = f"""<section class="page-hero"><div class="container article">
<div class="breadcrumbs"><a href="index.html">Home</a> › <a href="guides.html">Guides</a> › {g["cat"]}</div>
<h1 style="font-size:clamp(1.9rem,4vw,2.8rem)">{g["title"]}</h1><p class="lead">{g["desc"]}</p>
<div class="byline"><span>By the Biglo Editorial Team</span><span>·</span><span>Updated {TODAY}</span><span>·</span><span>{g["mins"]} min read</span></div>
<p class="disclosure">Editorial independence: our guides are written without input from partners. Some links may earn us a commission. <a href="disclosure.html">How we make money</a>.</p>
</div></section>
<section style="padding-top:10px"><div class="container article">
<div class="takeaways"><b>Key takeaways</b><ul>{"".join(f"<li>{t}</li>" for t in g["takeaways"])}</ul></div>
<nav class="toc" aria-label="Contents"><b>In this guide</b><ol>{toc}</ol></nav>
{secs}
<h2>FAQ</h2>{faq_html(g["faq"])}
<div class="card mt"><h3>▶ Watch: related video</h3><div class="grid" data-videos="1"></div></div>
<div class="card mt"><h3>Share this guide</h3><div style="display:flex;gap:8px;flex-wrap:wrap">
<a class="btn btn-ghost btn-sm" target="_blank" rel="noopener" href="https://twitter.com/intent/tweet?url={SITE}/guide-{g["slug"]}.html&text={g["title"]}">Post on X</a>
<a class="btn btn-ghost btn-sm" target="_blank" rel="noopener" href="https://www.facebook.com/sharer/sharer.php?u={SITE}/guide-{g["slug"]}.html">Facebook</a>
<a class="btn btn-ghost btn-sm" target="_blank" rel="noopener" href="https://www.linkedin.com/sharing/share-offsite/?url={SITE}/guide-{g["slug"]}.html">LinkedIn</a>
<a class="btn btn-ghost btn-sm" href="sms:?&body={SITE}/guide-{g["slug"]}.html">Text it</a></div></div>
</div></section>
<section class="alt"><div class="container"><h2>Keep reading</h2><div class="grid g3">{related}</div></div></section>
{newsletter_band()}"""
    art = {"@context": "https://schema.org", "@type": "Article", "headline": g["title"], "description": g["desc"],
           "dateModified": TODAY, "author": {"@type": "Organization", "name": "Biglo Editorial Team"},
           "publisher": {"@type": "Organization", "name": "Biglo"}, "mainEntityOfPage": f"{SITE}/guide-{g['slug']}.html"}
    out(f"guide-{g['slug']}.html", page(f"guide-{g['slug']}.html", g["title"] + " | Biglo", g["desc"], body, "guides.html", [art, faq_schema(g["faq"])]))

# ------------------------------------------------------------------ VIDEOS
videos = page_hero("Videos", "Watch, learn, save.", "The best money-saving videos on YouTube — curated. Subscribe to our channel for new videos every week.") + f"""
<section style="padding-top:20px"><div class="container"><div class="grid g3" data-videos></div></div></section>
{ad("inContent")}
<section class="alt"><div class="container grid g2" style="align-items:center">
  <div><span class="eyebrow">Creators</span><h2>Make money-saving videos? Get featured.</h2><p class="lead">We feature creators on Biglo and pay for sponsored integrations. Send us your channel.</p></div>
  <div class="card"><form data-form="creator" data-subject="Creator / YouTube feature request" data-success="Thanks — we'll review your channel this week.">{form_hidden()}
    <div class="field"><label for="cr-ch">Channel URL</label><input id="cr-ch" name="Channel" type="url" required placeholder="https://youtube.com/@..."></div>
    <div class="row2"><div class="field"><label for="cr-n">Name</label><input id="cr-n" name="Name" required></div><div class="field"><label for="cr-e">Email</label><input id="cr-e" name="Email" type="email" required></div></div>
    <button class="btn btn-primary" type="submit">Get featured</button></form></div>
</div></section>
{newsletter_band()}"""
out("videos.html", page("videos.html", "Money-Saving Videos | Biglo", "Curated money-saving, budgeting and bill-cutting videos.", videos, "videos.html"))

# ------------------------------------------------------------------ CONTESTS
contest = page_hero("Giveaways", "🎁 The $500 Bill-Buster Giveaway", "One winner gets $500 to knock out their bills. Free to enter — earn bonus entries below.") + f"""
<section style="padding-top:20px"><div class="container grid g2">
 <div class="card"><h2>Enter now</h2><p class="muted">Ends in:</p><div class="countdown" id="countdown" style="margin-bottom:18px"></div>
  <form data-form="contest-entry" data-subject="Giveaway entry" data-success="You're entered! Grab bonus entries on the right →">{form_hidden()}
   <div class="row2"><div class="field"><label for="ce-n">Full name</label><input id="ce-n" name="Name" required autocomplete="name"></div><div class="field"><label for="ce-e">Email</label><input id="ce-e" name="Email" type="email" required autocomplete="email"></div></div>
   <div class="row2"><div class="field"><label for="ce-c">Country</label><input id="ce-c" name="Country" required autocomplete="country-name"></div><div class="field"><label for="ce-a">Age confirmation</label><select id="ce-a" name="Age" required><option value="">Select…</option><option>I am 18 or older</option></select></div></div>
   <div class="field"><label for="ce-q">What bill would you pay off first?</label><input id="ce-q" name="Answer" placeholder="e.g. my car insurance"></div>
   <input type="hidden" name="Entries" id="entry-count" value="1"><input type="hidden" name="Referred by" id="entry-ref">
   <label class="check"><input type="checkbox" name="Rules accepted" value="Yes" required> I agree to the <a href="#rules">official rules</a> and to receive the Biglo newsletter (unsubscribe anytime).</label>
   <button class="btn btn-accent btn-lg btn-block mt" type="submit">Enter giveaway — free</button>
  </form></div>
 <div class="card"><h2>Bonus entries</h2><p class="muted">Your entries: <b id="entry-total" style="font-size:1.4rem;color:var(--brand-dark)">1</b></p>
  <ul class="entry-list" id="entries">
   <li data-entry="quote" data-pts="5"><span>💸 Get a free quote (2 min)</span><a class="btn btn-primary btn-sm" data-entry-go href="quotes.html" target="_blank">+5</a></li>
   <li data-entry="yt" data-pts="3"><span>▶ Watch a Biglo video</span><button class="btn btn-ghost btn-sm" data-entry-go data-url="videos.html">+3</button></li>
   <li data-entry="tool" data-pts="2"><span>🧮 Try the Bill Savings calculator</span><button class="btn btn-ghost btn-sm" data-entry-go data-url="tools.html">+2</button></li>
   <li data-entry="deal" data-pts="2"><span>🕵️ Submit a deal</span><button class="btn btn-ghost btn-sm" data-entry-go data-url="submit-deal.html">+2</button></li>
   <li data-entry="share" data-pts="5"><span>📣 Share your referral link</span><button class="btn btn-ghost btn-sm" data-entry-go>+5</button></li>
  </ul>
  <p class="form-note">Your referral link: <code id="ref-link" style="word-break:break-all"></code><br>Each friend who enters with your link = +5 entries for you.</p></div>
</div></section>
{ad("inContent")}
<section class="alt"><div class="container grid g2">
 <div><h2>Upcoming giveaways</h2><div class="grid">
  <div class="card"><h3>🛒 $250 Grocery Gift Card</h3><p>Opens January · Enter by sharing your best grocery hack.</p></div>
  <div class="card"><h3>☀️ Smart Home Energy Kit</h3><p>Opens February · Smart thermostat + LED bundle.</p></div>
  <div class="card"><h3>🎬 Creator Challenge — $1,000</h3><p>Best 60-second money-saving video wins. Judged on usefulness & creativity.</p></div></div></div>
 <div><h2>Sponsor a giveaway</h2><p class="lead">Put your brand in front of thousands of engaged entrants. Contests are the fastest way to grow a qualified email list.</p><a class="btn btn-primary" href="advertise.html#contact">Sponsor a contest →</a>
 <h3 class="mt">Past winners</h3><p class="muted">Our first winner will be announced here when the current giveaway closes.</p></div>
</div></section>
<section id="rules"><div class="container article"><h2>Official rules (summary)</h2>
<p><b>No purchase necessary.</b> A purchase does not improve your chances of winning. Void where prohibited.</p>
<ul><li><b>Eligibility:</b> Open to legal residents 18+ (or age of majority) where sweepstakes are lawful. Employees of Biglo and their families are not eligible.</li>
<li><b>Entry period:</b> Opens on publication and closes on the date shown by the countdown (Eastern Time).</li>
<li><b>How to enter:</b> Complete the entry form (1 entry). Optional bonus actions add entries; none require a purchase or social account. Alternate free entry: email us via the <a href="contact.html">contact form</a> with your name and “Giveaway entry”.</li>
<li><b>Winner selection:</b> One winner is selected by random draw from all eligible entries within 7 days of close, and notified by email. Winner must respond within 7 days or an alternate is drawn.</li>
<li><b>Prize:</b> $500 USD paid by PayPal or bank transfer. Taxes are the winner's responsibility. Odds depend on the number of eligible entries.</li>
<li><b>Fair play:</b> Duplicate, automated or fraudulent entries are disqualified.</li>
<li><b>Privacy:</b> Entry data is used to run the giveaway and send the newsletter, per our <a href="privacy.html">Privacy Policy</a>.</li></ul></div></section>
"""
out("contests.html", page("contests.html", "Win $500 — Biglo Bill-Buster Giveaway", "Enter free to win $500 toward your bills. Earn bonus entries by sharing, watching and saving.", contest, "contests.html"))

# ------------------------------------------------------------------ SUPPORT / DONATE
support = page_hero("Support", "Keep Biglo free for everyone ♥", "Your support funds new tools, honest guides, giveaways, and paying our writers and creators — with fewer ads.") + f"""
<section style="padding-top:20px"><div class="container grid g2">
 <div class="card" id="donate"><h2>Make a contribution</h2>
  <div class="toggle" role="group" aria-label="Frequency"><button type="button" class="active" data-freq="once">One-time</button><button type="button" data-freq="monthly">Monthly ♥</button></div>
  <div class="amount-grid"><button type="button" class="chip" data-amt="5">$5</button><button type="button" class="chip" data-amt="10">$10</button><button type="button" class="chip active" data-amt="25">$25</button><button type="button" class="chip" data-amt="50">$50</button></div>
  <div class="field"><label for="don-custom">Or enter an amount (USD)</label><input id="don-custom" type="number" min="1" placeholder="Custom amount"></div>
  <div class="field"><label for="don-purpose">Put it toward</label><select id="don-purpose"><option>General operations</option><option>New free tools</option><option>Giveaways & prizes</option><option>Hiring writers & creators</option><option>Marketing & promotion</option></select></div>
  <button type="button" class="btn btn-primary btn-lg btn-block" id="don-paypal">Give <span id="don-label">$25</span> with PayPal / card</button>
  <div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:10px"><a class="btn btn-ghost btn-sm" id="don-kofi" target="_blank" rel="noopener">☕ Ko-fi</a><a class="btn btn-ghost btn-sm" id="don-bmc" target="_blank" rel="noopener">☕ Buy Me a Coffee</a><a class="btn btn-ghost btn-sm" id="don-stripe" target="_blank" rel="noopener">💳 Card (Stripe)</a></div>
  <p class="form-note">Secure checkout by the payment provider. Biglo never sees your card details. Contributions are not tax-deductible.</p></div>
 <div>
  <div class="card"><h3>This month's goal</h3><div class="meter"><i id="don-meter" style="width:0"></i></div><p class="muted" style="margin-top:8px"><b id="don-raised">$0</b> raised of <b id="don-goal">$5,000</b></p>
   <table><tr><th>Where it goes</th><th>Share</th></tr><tr><td>Hosting, data & tools</td><td>25%</td></tr><tr><td>Writers, editors & creators</td><td>40%</td></tr><tr><td>Giveaways & prizes</td><td>20%</td></tr><tr><td>Marketing & outreach</td><td>15%</td></tr></table></div>
  <div class="card mt"><h3>Prefer to pledge or give another way?</h3>
   <form data-form="pledge" data-subject="Donation pledge / sponsorship" data-success="Thank you! We'll follow up with payment options.">{form_hidden()}
    <div class="row2"><div class="field"><label for="pl-n">Name</label><input id="pl-n" name="Name" required></div><div class="field"><label for="pl-e">Email</label><input id="pl-e" name="Email" type="email" required></div></div>
    <div class="row2"><div class="field"><label for="pl-a">Amount</label><input id="pl-a" name="Amount" required></div><div class="field"><label for="pl-m">Method</label><select id="pl-m" name="Method"><option>Bank transfer</option><option>Interac e-Transfer</option><option>UPI</option><option>Crypto</option><option>Other</option></select></div></div>
    <div class="field"><label for="pl-msg">Message (optional — say something nice!)</label><textarea id="pl-msg" name="Message" style="min-height:80px"></textarea></div>
    <label class="check"><input type="checkbox" name="Show on supporter wall" value="Yes"> Thank me publicly on the supporter wall</label>
    <button class="btn btn-ghost mt" type="submit">Send pledge</button></form></div>
 </div>
</div></section>
<section class="alt"><div class="container"><div class="section-head"><div><span class="eyebrow">Membership</span><h2>Become a Biglo Insider</h2></div></div>
<div class="grid g3">
 <div class="card tier"><h3>Saver</h3><div class="amt">$3<span class="muted" style="font-size:1rem">/mo</span></div><ul><li>Ad-light experience</li><li>Name on supporter wall</li><li>Monthly insider email</li></ul><a class="btn btn-ghost btn-block" href="#donate">Choose Saver</a></div>
 <div class="card tier featured"><span class="badge badge-green">Most popular</span><h3>Insider</h3><div class="amt">$9<span class="muted" style="font-size:1rem">/mo</span></div><ul><li>Everything in Saver</li><li>Early deal alerts (24h head start)</li><li>+10 entries in every giveaway</li><li>Vote on new tools</li></ul><a class="btn btn-primary btn-block" href="#donate">Choose Insider</a></div>
 <div class="card tier"><h3>Champion</h3><div class="amt">$25<span class="muted" style="font-size:1rem">/mo</span></div><ul><li>Everything in Insider</li><li>Quarterly 1:1 bill review call</li><li>Logo/name on About page</li></ul><a class="btn btn-ghost btn-block" href="#donate">Choose Champion</a></div>
</div></div></section>
"""
out("support.html", page("support.html", "Support Biglo — Donate or Become an Insider", "Support Biglo's free tools, guides and giveaways with a one-time or monthly contribution.", support, "support.html"))

# ------------------------------------------------------------------ CAREERS
roles = [("Senior Personal Finance Editor", "Remote · Contract/Full-time", "Own guide quality, fact-checking and editorial standards."),
         ("Deal Hunter (part-time)", "Remote · Flexible", "Find, verify and post the best daily deals and codes."),
         ("YouTube / Short-form Video Creator", "Remote · Per project", "Script, shoot and edit money-saving videos and Shorts."),
         ("Growth & SEO Marketer", "Remote · Contract", "Grow organic traffic, email list and partnerships."),
         ("Freelance Writer", "Remote · Per article", "Write practical guides on bills, insurance, energy and debt."),
         ("Partnerships Manager", "Remote · Commission + base", "Sign insurance, energy, telecom and lending partners.")]
role_cards = "".join(f'<div class="card"><span class="badge badge-green">{m}</span><h3 style="margin-top:10px">{t}</h3><p>{d}</p><a class="btn btn-ghost btn-sm mt" href="#apply" onclick="document.getElementById(\'ap-role\').value=\'{t}\'">Apply →</a></div>' for t, m, d in roles)
careers = page_hero("Careers", "Help millions pay less.", "Biglo is a remote-first team of editors, creators and builders. We hire talent from anywhere.") + f"""
<section style="padding-top:20px"><div class="container">
<div class="grid g4" style="margin-bottom:36px"><div class="stat"><b>100%</b><span>remote</span></div><div class="stat"><b>Async</b><span>by default</span></div><div class="stat"><b>Flexible</b><span>hours</span></div><div class="stat"><b>Paid</b><span>per project or salary</span></div></div>
<h2>Open roles</h2><div class="grid g3">{role_cards}</div></div></section>
<section class="alt" id="apply"><div class="container" style="max-width:820px"><div class="card"><h2>Apply / pitch us</h2><p class="muted">Don't see your role? Pitch us anyway.</p>
<form data-form="job-application" data-subject="Job application" data-success="Application received! We reply to every applicant within 5 business days.">{form_hidden()}
 <div class="row2"><div class="field"><label for="ap-n">Full name</label><input id="ap-n" name="Name" required></div><div class="field"><label for="ap-e">Email</label><input id="ap-e" name="Email" type="email" required></div></div>
 <div class="row2"><div class="field"><label for="ap-role">Role</label><input id="ap-role" name="Role" required list="rolelist"><datalist id="rolelist">{"".join(f"<option>{t}</option>" for t, _, _ in roles)}</datalist></div><div class="field"><label for="ap-l">Location / time zone</label><input id="ap-l" name="Location"></div></div>
 <div class="row2"><div class="field"><label for="ap-p">Portfolio / LinkedIn / channel</label><input id="ap-p" name="Portfolio" type="url" required placeholder="https://"></div><div class="field"><label for="ap-cv">Resume link (Drive, Dropbox…)</label><input id="ap-cv" name="Resume" type="url" placeholder="https://"></div></div>
 <div class="row2"><div class="field"><label for="ap-r">Expected rate</label><input id="ap-r" name="Rate"></div><div class="field"><label for="ap-a">Available from</label><input id="ap-a" name="Available" type="date"></div></div>
 <div class="field"><label for="ap-w">Why you, in 3 sentences</label><textarea id="ap-w" name="Pitch" required></textarea></div>
 <button class="btn btn-primary btn-lg" type="submit">Submit application</button></form></div></div></section>"""
out("careers.html", page("careers.html", "Careers at Biglo — Remote Jobs for Writers, Creators & Marketers", "Join Biglo: remote roles for editors, deal hunters, video creators, SEO marketers and partnerships.", careers))

# ------------------------------------------------------------------ ADVERTISE
adv = page_hero("Advertise", "Reach shoppers who are ready to switch.", "Biglo visitors arrive with intent: they want a lower bill or a better price today. Put your brand in that moment.") + f"""
<section style="padding-top:20px"><div class="container"><div class="grid g3">
 <div class="card"><div class="ico">🎯</div><h3>Pay-per-lead partnerships</h3><p>Exclusive or shared, TCPA-consented leads for insurance, energy/solar, telecom, lending and moving. Filter by ZIP, product and intent.</p></div>
 <div class="card"><div class="ico">🏷️</div><h3>Featured deals</h3><p>Top-of-page placement on Deals, homepage carousel and the weekly newsletter.</p></div>
 <div class="card"><div class="ico">📰</div><h3>Sponsored guides</h3><p>Clearly labeled sponsored content written by our editors to our standards.</p></div>
 <div class="card"><div class="ico">▶</div><h3>Video integrations</h3><p>Sponsor segments in Biglo YouTube videos and Shorts.</p></div>
 <div class="card"><div class="ico">🎁</div><h3>Contest sponsorship</h3><p>Co-branded giveaways that grow your list with opted-in entrants.</p></div>
 <div class="card"><div class="ico">🖼️</div><h3>Display & newsletter</h3><p>Direct-sold banner placements and newsletter sponsorships.</p></div>
</div></div></section>
<section class="alt" id="media-kit"><div class="container grid g2">
 <div><span class="eyebrow">Media kit</span><h2>Audience & formats</h2><p>Request the current media kit for up-to-date traffic, list size and rates.</p>
 <table><tr><th>Placement</th><th>Model</th></tr><tr><td>Lead partnerships</td><td>CPL / rev-share</td></tr><tr><td>Featured deal</td><td>Flat weekly / CPC</td></tr><tr><td>Sponsored guide</td><td>Flat fee</td></tr><tr><td>Newsletter sponsor</td><td>Per send</td></tr><tr><td>Video integration</td><td>Per video</td></tr><tr><td>Giveaway sponsor</td><td>Flat + prize</td></tr></table>
 <p class="form-note">Editorial independence: advertisers never influence our reviews or rankings. All paid placements are labeled.</p></div>
 <div class="card" id="contact"><h2>Get the media kit</h2>
 <form data-form="advertise" data-subject="Advertising / partnership inquiry" data-success="Thanks! Our partnerships team will reply within 1 business day with the media kit.">{form_hidden()}
  <div class="row2"><div class="field"><label for="ad-n">Name</label><input id="ad-n" name="Name" required></div><div class="field"><label for="ad-c">Company</label><input id="ad-c" name="Company" required></div></div>
  <div class="row2"><div class="field"><label for="ad-e">Work email</label><input id="ad-e" name="Email" type="email" required></div><div class="field"><label for="ad-w">Website</label><input id="ad-w" name="Website" type="url" placeholder="https://"></div></div>
  <div class="row2"><div class="field"><label for="ad-t">Interested in</label><select id="ad-t" name="Interest"><option>Lead partnership (CPL)</option><option>Featured deals</option><option>Sponsored content</option><option>Video integration</option><option>Giveaway sponsorship</option><option>Display / newsletter</option><option>Acquire this website/domain</option></select></div>
  <div class="field"><label for="ad-b">Monthly budget</label><select id="ad-b" name="Budget"><option>Under $1k</option><option>$1k–$5k</option><option>$5k–$25k</option><option>$25k+</option></select></div></div>
  <div class="field"><label for="ad-g">Goals</label><textarea id="ad-g" name="Goals" style="min-height:90px"></textarea></div>
  <button class="btn btn-primary btn-lg btn-block" type="submit">Request media kit</button></form></div>
</div></section>"""
out("advertise.html", page("advertise.html", "Advertise on Biglo — Leads, Sponsorships & Media Kit", "Advertise with Biglo: pay-per-lead partnerships, featured deals, sponsored guides, video and giveaway sponsorships.", adv, "advertise.html"))

# ------------------------------------------------------------------ PARTNERS
partners = page_hero("Partners", "Become a Biglo partner", "Insurance carriers & agents, ISPs, energy suppliers, solar installers, lenders, movers — get qualified, consented customers.") + f"""
<section style="padding-top:20px"><div class="container grid g2">
 <div><h2>Why partner</h2><ul class="lead" style="padding-left:20px"><li>High-intent, consented leads</li><li>ZIP, product and budget filtering</li><li>Pay only for qualified leads</li><li>Real-time delivery by email, webhook or CRM</li><li>Dedicated partner manager</li></ul>
 <h3 class="mt">Affiliate & creator program</h3><p>Bloggers and creators earn a commission on every qualified quote they refer. Use your referral link <code>biglo.com/quotes.html?ref=YOURCODE</code>.</p></div>
 <div class="card"><form data-form="partner" data-subject="Partner application" data-success="Thanks! A partner manager will reach out within 1 business day.">{form_hidden()}
  <div class="row2"><div class="field"><label for="pa-c">Company</label><input id="pa-c" name="Company" required></div><div class="field"><label for="pa-n">Contact name</label><input id="pa-n" name="Name" required></div></div>
  <div class="row2"><div class="field"><label for="pa-e">Email</label><input id="pa-e" name="Email" type="email" required></div><div class="field"><label for="pa-p">Phone</label><input id="pa-p" name="Phone" type="tel"></div></div>
  <div class="row2"><div class="field"><label for="pa-t">Partner type</label><select id="pa-t" name="Type"><option>Insurance</option><option>Internet / TV</option><option>Energy / Solar</option><option>Lending</option><option>Mobile carrier</option><option>Moving</option><option>Affiliate / creator</option></select></div>
  <div class="field"><label for="pa-g">Regions served</label><input id="pa-g" name="Regions" placeholder="States, provinces, countries"></div></div>
  <div class="field"><label for="pa-v">Monthly lead volume wanted</label><input id="pa-v" name="Volume"></div>
  <button class="btn btn-primary btn-lg btn-block" type="submit">Apply to partner</button></form></div>
</div></section>"""
out("partners.html", page("partners.html", "Partner with Biglo — Lead Partnerships & Affiliate Program", "Get high-intent, consented customer leads or join the Biglo affiliate program.", partners))

# ------------------------------------------------------------------ ABOUT
about = page_hero("About", "We help people pay less for the stuff they already buy.", "Biglo = Big savings, Low bills. We combine deals, free tools and honest quote matching in one place.") + """
<section style="padding-top:20px"><div class="container grid g2">
 <div class="article" style="margin:0"><h2>Our mission</h2><p>Most households overpay for insurance, internet, phone, energy and debt simply because comparing is tedious. Biglo makes it fast: tell us what you pay, and we show you how to pay less.</p>
 <h2>How we're different</h2><ul><li><b>Free for you, always.</b> Partners pay us, never you.</li><li><b>No lead blasting.</b> Maximum 3 matches per request.</li><li><b>Editorial independence.</b> Partners can't buy rankings or reviews.</li><li><b>Privacy first.</b> We never sell your personal data.</li></ul></div>
 <div class="grid"><div class="card"><h3>📬 Get in touch</h3><p>Questions, feedback, press or corrections — we read everything.</p><a class="btn btn-primary" href="contact.html">Contact us</a></div>
 <div class="card"><h3>💼 Interested in this website?</h3><p>The Biglo.com domain and website may be available for acquisition or partnership.</p><a class="btn btn-ghost" href="https://web.works/contact" target="_blank" rel="noopener">Inquire at web.works</a></div></div>
</div></section>"""
out("about.html", page("about.html", "About Biglo", "Biglo helps people lower their bills and find better deals with free tools and honest quote matching.", about))

# ------------------------------------------------------------------ CONTACT
contact = page_hero("Contact", "Contact Biglo", "We reply to every message within 1 business day.") + f"""
<section style="padding-top:20px"><div class="container grid g2">
 <div class="card"><form data-form="contact" data-subject="Contact form" data-success="Message sent! We'll reply within 1 business day.">{form_hidden()}
  <div class="row2"><div class="field"><label for="c-n">Name</label><input id="c-n" name="Name" required autocomplete="name"></div><div class="field"><label for="c-e">Email</label><input id="c-e" name="Email" type="email" required autocomplete="email"></div></div>
  <div class="field"><label for="c-t">Topic</label><select id="c-t" name="Topic"><option>General question</option><option>Help with my quote</option><option>Deal / listing issue</option><option>Advertising & partnerships</option><option>Press</option><option>Careers</option><option>Donations & support</option><option>Giveaway</option><option>Privacy / data request</option><option>Buy this website / domain</option></select></div>
  <div class="field"><label for="c-m">Message</label><textarea id="c-m" name="Message" required></textarea></div>
  <button class="btn btn-primary btn-lg" type="submit">Send message</button></form></div>
 <div class="grid">
  <div class="card"><h3>✉️ Prefer email?</h3><p>Open your mail app with our address pre-filled.</p><a class="btn btn-ghost" href="contact.html" data-mail="Biglo inquiry">Email Biglo</a></div>
  <div class="card"><h3>💼 Domain & website inquiries</h3><p>Interested in acquiring Biglo.com or this website?</p><a class="btn btn-accent" href="https://web.works/contact" target="_blank" rel="noopener">Contact via web.works</a></div>
  <div class="card"><h3>📣 Advertisers</h3><p>Media kit, lead partnerships, sponsorships.</p><a class="btn btn-ghost" href="advertise.html#contact">Advertising inquiries</a></div>
 </div>
</div></section>"""
out("contact.html", page("contact.html", "Contact Biglo", "Contact Biglo for help, partnerships, press, careers and domain inquiries.", contact))

# ------------------------------------------------------------------ LEGAL
def legal(name, title, h, sections):
    body = page_hero(h, h, f"Last updated: {TODAY}") + '<section style="padding-top:10px"><div class="container article">' + "".join(
        f"<h2>{a}</h2>{b}" for a, b in sections) + "</div></section>"
    out(name, page(name, title + " | Biglo", title + " for Biglo.com.", body))


legal("privacy.html", "Privacy Policy", "Privacy Policy", [
    ("What we collect", "<p>Information you submit in forms (such as name, email, phone, ZIP/postal code and your answers), and technical data such as device, browser and pages viewed collected via cookies and similar technologies.</p>"),
    ("How we use it", "<p>To respond to you, match your quote request with up to 3 relevant partners (only when you consent), send newsletters you signed up for, run giveaways, prevent fraud, and improve the site.</p>"),
    ("Sharing", "<p>We share quote-request details only with partners you consent to be matched with. We use service providers for form delivery, analytics and advertising. <b>We do not sell your personal information.</b></p>"),
    ("Advertising & cookies", "<p>We may use Google AdSense. Google and its partners use cookies to serve ads based on prior visits to this and other websites. You can opt out of personalized advertising at <a href=\"https://adssettings.google.com\" target=\"_blank\" rel=\"noopener\">Google Ad Settings</a> or <a href=\"https://www.aboutads.info\" target=\"_blank\" rel=\"noopener\">aboutads.info</a>. YouTube videos load in privacy-enhanced mode only after you press play.</p>"),
    ("Your rights", "<p>Depending on where you live (e.g. GDPR, CCPA/CPRA, PIPEDA, Quebec Law 25), you may request access, correction, deletion or portability of your data, and opt out of marketing. Use the <a href=\"contact.html\">contact form</a> and choose “Privacy / data request”.</p>"),
    ("Retention & security", "<p>We keep data only as long as needed for the purposes above, and use encryption in transit (HTTPS).</p>"),
    ("Children", "<p>Biglo is not directed to children under 16, and giveaways require entrants to be 18+.</p>"),
    ("Contact", "<p>Questions? Reach us through the <a href=\"contact.html\">contact page</a>.</p>")])
legal("terms.html", "Terms of Use", "Terms of Use", [
    ("Using Biglo", "<p>By using Biglo.com you agree to these terms. Content is for general information and education only and is not financial, legal, tax or insurance advice.</p>"),
    ("Quotes & partners", "<p>Biglo is not an insurer, lender, utility or carrier. Offers, rates and eligibility are set by partners and may change. Always review terms with the provider before purchasing.</p>"),
    ("Deals", "<p>Prices and availability change quickly. We try to keep listings accurate but can't guarantee them.</p>"),
    ("User submissions", "<p>By submitting deals, comments or content you grant Biglo a license to publish them. Don't submit anything unlawful or that you don't have rights to.</p>"),
    ("Giveaways", "<p>Each giveaway is governed by its official rules.</p>"),
    ("Liability", "<p>Biglo is provided “as is”. To the extent permitted by law, we are not liable for indirect or consequential losses arising from use of the site.</p>"),
    ("Changes", "<p>We may update these terms; continued use means you accept the updated terms.</p>")])
legal("disclosure.html", "How We Make Money", "How we make money", [
    ("Short version", "<p>Biglo is free for you. We earn money from advertising (including Google AdSense), affiliate commissions when you buy through our links, referral fees from partners when you request quotes, sponsorships, and reader contributions.</p>"),
    ("Does it change your price?", "<p>No. Commissions and referral fees are paid by the partner and don't change the price you pay.</p>"),
    ("Editorial independence", "<p>Partners can't pay to change our guides, calculators or rankings. Paid placements are always labeled “Sponsored” or “Featured”.</p>"),
    ("Affiliate disclosure (FTC)", "<p>Some links on Biglo are affiliate links. If you click and make a purchase, we may receive a commission.</p>")])

# ------------------------------------------------------------------ 404
out("404.html", page("404.html", "Page not found | Biglo", "Page not found.", """<section class="hero"><div class="container center"><div style="font-size:4rem">🔍</div><h1>This page went bargain hunting.</h1><p class="lead" style="margin:0 auto 20px">We couldn't find it — but we can find you a lower bill.</p><a class="btn btn-primary btn-lg" href="index.html">Go home</a> <a class="btn btn-ghost btn-lg" href="deals.html">See deals</a></div></section>"""))

# ------------------------------------------------------------------ SITEMAP
urls = [n for n in PAGES if n != "404.html"]
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
    f"  <url><loc>{SITE}/{'' if n == 'index.html' else n}</loc><lastmod>{TODAY}</lastmod><priority>{'1.0' if n == 'index.html' else '0.8'}</priority></url>\n" for n in sorted(urls)) + "</urlset>\n"
open(os.path.join(ROOT, "sitemap.xml"), "w").write(sm)
print("Built", len(PAGES), "pages")
