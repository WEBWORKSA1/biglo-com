# Biglo.com: Phase-by-Phase Build Prompt

**Concept:** Biglo = **Big** savings, **Lo**w bills. The site is a consumer money-saving hub with four parts: deals, free money calculators, guides and videos, and a high-intent **"Get lower quotes"** lead-generation funnel covering insurance, internet, energy and solar, loans, phone plans and moving.

**Why this concept:**
- Insurance, loan, energy and solar keywords are among the most expensive AdSense and search keywords, so they pay the highest per ad click.
- Pay-per-lead in these same verticals commonly pays $10–$100+ per consented lead.
- Deals and calculators bring repeat, shareable traffic and backlinks, which feed the funnel.
- "Biglo" is short and brandable, and it states what the site does.

Use the prompts below in order, one phase per session. Each phase lists its acceptance criteria.

---

## Phase 0: Global rules (paste at the top of every phase)
```
You are building Biglo.com, a static, free-hosted (GitHub Pages) money-saving website.
Hard rules:
1. Every page starts with a top bar: "Contact, if you are interested in this website/domain name" linking to https://web.works/contact (new tab).
2. All forms and contact actions deliver to ONE private inbox. The address must NEVER appear in HTML/visible text.
   Store it encoded in assets/js/config.js and decode at runtime. Forms POST via FormSubmit AJAX (or the alias from config).
   "Email us" links build the mailto on click only.
3. Pure HTML/CSS/vanilla JS. No backend, no paid services, no build step needed to serve. Relative links only (works on *.github.io/biglo-com/ and on a custom domain).
4. Mobile-first, responsive to 360px, light and dark mode, WCAG AA contrast, keyboard accessible, prefers-reduced-motion respected.
5. SEO: unique title/description, canonical, OpenGraph, JSON-LD (WebSite, Organization, Article, FAQPage), sitemap.xml, robots.txt.
6. Monetization hooks everywhere: AdSense slots, YouTube lite embeds, affiliate deal links (rel="sponsored"), lead funnel CTAs, donation, sponsorship.
7. Honest content: no fake reviews, fake stats or fake testimonials. Sample data must be labeled.
```

## Phase 1: Foundation and design system
```
Create the repo structure: /assets/css/style.css, /assets/js/{config,data,main}.js, /assets/img, /_build (Python page generator), /docs.
Design tokens: brand green #0f9d58, accent amber #ffb020, ink #0f1a14; font Plus Jakarta Sans; radius 18px; soft shadows.
Build components: sticky glass header with mobile drawer, domain top bar, buttons (primary/accent/ghost), cards, badges,
stat tiles, forms (with honeypot), chips, progress bar, modal, toast, cookie banner, sticky CTA, footer (5 columns).
Build a Python layout generator (_build/layout.py + build.py) so every page shares header/footer and meta.
Acceptance: all pages render with header, top bar and footer; Lighthouse accessibility ≥ 95.
```

## Phase 2: Homepage (conversion hub)
```
Sections in order:
1. Hero: headline, subhead, 2 CTAs, trust row, and a quick-quote widget (6 category pills + ZIP → quotes.html?type=&zip=).
2. Stat bar (only true, verifiable numbers).
3. Ad slot.
4. Top deals (6, most-voted).
5. How it works (3 numbered steps).
6. Tools grid (8).
7. Ad slot.
8. Video row (3).
9. Guides (3).
10. Giveaway teaser with countdown.
11. Support / careers / advertise cards.
12. Newsletter band.
13. Footer ad.
Acceptance: the quick-quote goes straight into step 2 of the funnel with the category preselected.
```

## Phase 3: Lead-generation funnel (quotes.html), the revenue engine
```
Multi-step, one question per screen, big tap targets, progress bar, back button, auto-advance on selection.
Flow: Category → 4 category-specific questions → ZIP → Contact (first, last, email, phone optional, TCPA-style consent checkbox).
Categories and questions:
- Insurance: coverage type, currently insured, count, claims
- Internet: current bill, usage, household size, TV
- Energy: bill, own/rent, interest (solar/battery/plan/heat pump), shade
- Loans: type, amount, credit range (ranges only, never SSN), timeline
- Phone: lines, bill, data, own phones
- Moving: size, distance, date, services
Trust microcopy under the CTA: 256-bit SSL, no spam calls, 100% free, never sold.
Submit the full answer set as one lead email with a subject line like "NEW LEAD — {type} — {ZIP}"; read ?ref= for affiliate attribution.
Success screen: "You're matched" plus 3 next steps; fallback to mailto if the network fails.
Below the funnel: why Biglo (4 cards), category grid, FAQ.
Acceptance: complete funnel in under 60 seconds on mobile; lead payload contains every answer.
```

## Phase 4: Deals engine (deals.html + submit-deal.html)
```
Deal cards from data.js: emoji/image, % off badge, staff pick / exclusive / hot / ends-soon badges, price and was-price,
COPY CODE button, store, category, upvote (localStorage), "Get deal" affiliate link (rel="sponsored nofollow").
Toolbar: search, sort (popular/newest/ending/discount), type filter, category chips, result count.
Deal Alerts form (keyword, max price, email). A Submit-a-deal page with a full form. Affiliate disclosure at the top.
Acceptance: filters combine; copy-code works; the sample-data label is visible until a live feed is connected.
```

## Phase 5: Tools (tools.html)
```
Tabbed calculators with deep links (#id). Results update live on input:
1. Bill Savings Estimator (bars)
2. Subscription Audit (add rows, tick to cancel)
3. Debt Payoff (months, interest, +$100 scenario)
4. Loan & Refinance (payment, total, interest, 1.5% refi delta)
5. Solar Payback (net cost, payback, 25-year savings)
6. Savings Goal (monthly/weekly)
7. 50/30/20 Budget
8. Unit Price Compare
Every result panel ends with a CTA into the matching funnel category.
```

## Phase 6: Content (guides, videos)
```
Guide template: breadcrumb, H1, byline, updated date, read time, disclosure, key takeaways, TOC,
numbered sections, in-content ad after section 3, funnel CTA box after section 5, FAQ with FAQPage schema,
related video, share buttons (X, Facebook, LinkedIn, SMS), related guides, newsletter.
Launch with 6 guides: lower monthly bills, car insurance, internet/phone, solar, debt payoff, groceries. Target 20+ in 90 days.
Videos page: YouTube lite-facade grid (thumbnail first, iframe on click, youtube-nocookie) plus a creator "get featured" form.
```

## Phase 7: Community and revenue pages
```
- contests.html: prize, countdown, entry form (18+, rules consent), bonus-entry actions (quote +5, video +3, tool +2, submit deal +2, share +5),
  personal referral link, upcoming giveaways, sponsor CTA, official rules (no purchase necessary, free alternate entry, random draw).
- support.html: one-time/monthly toggle, preset amounts plus custom, purpose selector, PayPal donate (URL built at runtime),
  optional Ko-fi / Buy Me a Coffee / Stripe links from config, goal meter, allocation table, pledge form, membership tiers.
- careers.html: role cards and an application form. advertise.html: formats, media-kit table, inquiry form (includes "Acquire this website/domain").
- partners.html: lead-buyer and affiliate application.
- about, contact (with a mailto button built at runtime), privacy (AdSense cookie language, GDPR/CCPA/Law 25), terms, disclosure, 404.
```

## Phase 8: Monetization switch-on
```
1. AdSense: apply once there are 20+ quality pages and some traffic. Paste the ca-pub ID into config.adsenseClient and ads.txt.
2. Affiliates: Amazon Associates, Impact, CJ, Rakuten Advertising, ShareASale. Replace url:"#" in data.js.
3. Lead buyers: sign CPL agreements (insurance, solar, ISP, lenders). Forward lead emails, or later swap FormSubmit for a webhook.
4. YouTube: launch the Biglo channel; add its video IDs to data.js and the channel URL to config.
5. Donations: create a PayPal account on the site inbox (or add Ko-fi/BMC/Stripe links).
6. Analytics: add the GA4 ID (loads only after cookie consent). Track generate_lead, deal_click, video_play, donate_click.
```

## Phase 9: Deploy and scale
```
Push to GitHub (WEBWORKSA1/biglo-com), enable Pages (main, /root), then add the custom domain biglo.com
(CNAME file + DNS: A records 185.199.108-111.153, or a CNAME for www → webworksa1.github.io). Enforce HTTPS.
Scale: programmatic city/state pages ("cheap car insurance in {city}"), a comparison-table page per category,
weekly newsletter, Shorts repurposed from guides, and quarterly giveaways sponsored by partners.
```
