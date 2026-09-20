/* ==========================================================================
   BIGLO SITE CONFIG — edit this file to switch on monetization.
   Everything here is safe to change without touching page code.
   ========================================================================== */
window.BIGLO_CONFIG = {
  siteName: "Biglo",
  siteUrl: "https://biglo.com",
  domainInquiryUrl: "https://web.works/contact",

  /* ---- Google AdSense -------------------------------------------------
     1. Get approved at https://adsense.google.com
     2. Paste your publisher ID below (format: "ca-pub-1234567890123456")
     3. Put the same ID into /ads.txt
     4. Optionally map slot IDs per placement. Empty slot = Auto ads fill.
     While empty, the site shows labelled "Advertise here" placeholders. */
  adsenseClient: "",
  adSlots: { header: "", inContent: "", sidebar: "", footer: "" },

  /* ---- Analytics (optional) — GA4 measurement ID e.g. "G-XXXXXXX" ---- */
  ga4Id: "",

  /* ---- Contact routing ------------------------------------------------
     All forms submit to ONE inbox via FormSubmit (free, no backend).
     The address is stored encoded and is never printed on the site.
     After the first submission FormSubmit emails an activation link —
     click it once. FormSubmit then gives you a random alias string;
     paste it into formAlias to stop using the address entirely.       */
  formAlias: "",
  _m: [122,120,116,57,123,126,118,122,112,87,38,118,100,124,101,120,96,117,114,96],

  /* ---- Donations / support -------------------------------------------
     PayPal donate works immediately if the site inbox has a PayPal
     account. Add Ko-fi / Buy Me a Coffee / Stripe Payment Links when
     ready — any empty link is hidden automatically.                    */
  donate: {
    paypal: true,
    kofi: "",            // e.g. "https://ko-fi.com/biglo"
    buymeacoffee: "",    // e.g. "https://buymeacoffee.com/biglo"
    stripe: "",          // Stripe Payment Link URL
    goal: 5000,          // monthly operating goal (USD)
    raised: 0            // update manually
  },

  /* ---- Social / YouTube ---------------------------------------------- */
  youtubeChannel: "",    // e.g. "https://www.youtube.com/@biglo"
  socials: { youtube: "", x: "", instagram: "", tiktok: "", facebook: "" },

  /* ---- Contest ------------------------------------------------------- */
  contest: {
    title: "The $500 Bill-Buster Giveaway",
    prize: "$500 cash (PayPal or bank transfer) + Biglo Savings Kit",
    endsAt: "2026-12-31T23:59:59-05:00"
  }
};
