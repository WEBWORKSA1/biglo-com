# Biglo.com: Big savings, low bills

Biglo is a static money-saving hub with deals, free calculators, guides, videos, a multi-step "Get lower quotes" lead funnel, giveaways, donations, careers and an advertise section. It is built with plain HTML, CSS and JavaScript and hosted free on GitHub Pages.

> 💼 [Contact, if you are interested in this website/domain name](https://web.works/contact)

## Structure
```
index.html            Homepage (hero quick-quote, deals, tools, videos, guides, giveaway)
quotes.html           Lead-generation funnel (6 categories)
deals.html            Deals with search/sort/filter/votes/copy-code + Deal Alerts
tools.html            8 calculators (#bills #subs #debt #loan #solar #savings #budget #unit)
guides.html, guide-*  Evergreen articles with FAQ schema
videos.html           YouTube lite embeds + creator form
contests.html         Giveaway, countdown, bonus entries, referral link, rules
support.html          Donations (PayPal/Ko-fi/BMC/Stripe), pledge form, memberships
careers.html, advertise.html, partners.html, about.html, contact.html, legal pages
assets/js/config.js   ← switch on AdSense, GA4, donation links, contest settings
assets/js/data.js     ← deals + videos
_build/               Python generator (python3 _build/build.py regenerates every page)
docs/                 BUILD-PROMPT.md (phase-wise prompt) + RESEARCH.md
```

## Forms
All forms post through FormSubmit to one private inbox. The address is stored encoded in `config.js` and never appears in the page text.
1. The first submission triggers an activation email from FormSubmit. Click **Activate**.
2. Optional: copy the random alias FormSubmit provides into `formAlias` in `config.js`.

## Monetize
- **AdSense:** set `adsenseClient` in `config.js` and update `ads.txt`.
- **Affiliate deals:** replace `url:"#"` in `data.js` and set `dealsAreDemo:false`.
- **YouTube:** add your own video IDs to `data.js`.
- **Donations:** PayPal works on the site inbox. Add Ko-fi/BMC/Stripe URLs in `config.js`.

## Hosting (GitHub Pages, free)
Settings → Pages → Source: **Deploy from a branch** → Branch **main** / **(root)** → Save. The site goes live at `https://webworksa1.github.io/biglo-com/`.

## Custom domain
Add a `CNAME` file containing `biglo.com`, then point DNS A records to 185.199.108.153, .109.153, .110.153 and .111.153 (or a www CNAME to `webworksa1.github.io`). Enable "Enforce HTTPS" in Settings → Pages.
