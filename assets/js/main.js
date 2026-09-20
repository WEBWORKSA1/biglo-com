/* Biglo.com — core interactions. No framework, no build step. */
(function () {
  "use strict";
  var C = window.BIGLO_CONFIG || {};
  var D = window.BIGLO_DATA || { deals: [], videos: [] };
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var store = {
    get: function (k, d) { try { var v = localStorage.getItem("biglo_" + k); return v === null ? d : JSON.parse(v); } catch (e) { return d; } },
    set: function (k, v) { try { localStorage.setItem("biglo_" + k, JSON.stringify(v)); } catch (e) {} }
  };
  var money = function (n, dec) {
    if (!isFinite(n)) return "—";
    return "$" + Number(n).toLocaleString("en-US", { minimumFractionDigits: dec || 0, maximumFractionDigits: dec || 0 });
  };
  function toast(msg) {
    var t = $(".toast"); if (!t) { t = document.createElement("div"); t.className = "toast"; t.setAttribute("role", "status"); document.body.appendChild(t); }
    t.textContent = msg; t.classList.add("show"); clearTimeout(t._h); t._h = setTimeout(function () { t.classList.remove("show"); }, 2400);
  }
  window.bigloToast = toast;

  /* ---------- Private inbox (never rendered) ---------- */
  function inbox() { return (C._m || []).slice().reverse().map(function (c) { return String.fromCharCode(c ^ 23); }).join(""); }
  function endpoint() { return "https://formsubmit.co/ajax/" + (C.formAlias || inbox()); }
  $$("[data-mail]").forEach(function (a) {
    a.setAttribute("href", "contact.html");
    a.addEventListener("click", function (e) {
      e.preventDefault();
      var subj = encodeURIComponent(a.getAttribute("data-mail") || "Biglo inquiry");
      window.location.href = "mai" + "lto:" + inbox() + "?subject=" + subj;
    });
  });

  /* ---------- Theme ---------- */
  var root = document.documentElement;
  var saved = store.get("theme", null); if (saved) root.setAttribute("data-theme", saved);
  $$("[data-theme-toggle]").forEach(function (b) {
    b.addEventListener("click", function () {
      var dark = root.getAttribute("data-theme") === "dark" || (!root.getAttribute("data-theme") && matchMedia("(prefers-color-scheme: dark)").matches);
      var next = dark ? "light" : "dark"; root.setAttribute("data-theme", next); store.set("theme", next);
    });
  });

  /* ---------- Mobile nav ---------- */
  var menuBtn = $(".menu-btn"), links = $(".nav-links");
  if (menuBtn && links) menuBtn.addEventListener("click", function () {
    var open = links.classList.toggle("open"); menuBtn.setAttribute("aria-expanded", open);
  });

  /* ---------- Year ---------- */
  $$("[data-year]").forEach(function (e) { e.textContent = new Date().getFullYear(); });

  /* ---------- Reveal on scroll ---------- */
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (en) { en.forEach(function (x) { if (x.isIntersecting) { x.target.classList.add("in"); io.unobserve(x.target); } }); }, { threshold: .12 });
    $$(".reveal").forEach(function (e) { io.observe(e); });
    setTimeout(function () { $$(".reveal").forEach(function (e) { e.classList.add("in"); }); }, 4000);
  } else $$(".reveal").forEach(function (e) { e.classList.add("in"); });

  /* ---------- Cookie consent ---------- */
  var ck = $(".cookie");
  if (ck && !store.get("consent", null)) ck.classList.add("show");
  $$("[data-consent]").forEach(function (b) {
    b.addEventListener("click", function () { store.set("consent", b.getAttribute("data-consent")); ck && ck.classList.remove("show"); loadTracking(); });
  });

  /* ---------- AdSense + GA4 ---------- */
  function loadScript(src, attrs) { var s = document.createElement("script"); s.async = true; s.src = src; Object.keys(attrs || {}).forEach(function (k) { s.setAttribute(k, attrs[k]); }); document.head.appendChild(s); }
  function renderAds() {
    $$(".ad-slot").forEach(function (slot) {
      var place = slot.getAttribute("data-slot") || "inContent";
      var box = slot.querySelector(".ad-box");
      if (C.adsenseClient) {
        var ins = document.createElement("ins");
        ins.className = "adsbygoogle"; ins.style.display = "block";
        ins.setAttribute("data-ad-client", C.adsenseClient);
        var sid = (C.adSlots || {})[place];
        if (sid) ins.setAttribute("data-ad-slot", sid);
        ins.setAttribute("data-ad-format", "auto"); ins.setAttribute("data-full-width-responsive", "true");
        box.innerHTML = ""; box.appendChild(ins);
        try { (window.adsbygoogle = window.adsbygoogle || []).push({}); } catch (e) {}
      }
    });
  }
  if (C.adsenseClient) { loadScript("https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=" + C.adsenseClient, { crossorigin: "anonymous" }); renderAds(); }
  var tracked = false;
  function loadTracking() {
    if (tracked || !C.ga4Id || store.get("consent", "") !== "all") return; tracked = true;
    loadScript("https://www.googletagmanager.com/gtag/js?id=" + C.ga4Id);
    window.dataLayer = window.dataLayer || []; window.gtag = function () { dataLayer.push(arguments); };
    gtag("js", new Date()); gtag("config", C.ga4Id);
  }
  loadTracking();
  function track(ev, p) { if (window.gtag) window.gtag("event", ev, p || {}); }

  /* ---------- Forms (all routed to one hidden inbox) ---------- */
  function serialize(form) {
    var o = {}; new FormData(form).forEach(function (v, k) { if (k === "_honey") return; o[k] = o[k] ? o[k] + ", " + v : v; }); return o;
  }
  function submitPayload(payload, subject) {
    payload._subject = "[Biglo] " + subject;
    payload._template = "table";
    payload._captcha = "false";
    payload["Page"] = location.href;
    payload["Submitted"] = new Date().toISOString();
    return fetch(endpoint(), { method: "POST", headers: { "Content-Type": "application/json", Accept: "application/json" }, body: JSON.stringify(payload) })
      .then(function (r) { return r.json().catch(function () { return {}; }).then(function (j) { if (!r.ok || j.success === "false" || j.success === false) throw new Error(j.message || "Send failed"); return j; }); });
  }
  window.bigloSubmit = submitPayload;
  function status(form, ok, msg) {
    var s = form.querySelector(".form-status"); if (!s) { s = document.createElement("div"); s.className = "form-status"; s.setAttribute("role", "status"); form.appendChild(s); }
    s.className = "form-status " + (ok ? "ok" : "err"); s.innerHTML = msg;
  }
  $$("form[data-form]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (form.querySelector('[name="_honey"]') && form.querySelector('[name="_honey"]').value) return;
      if (!form.checkValidity()) { form.reportValidity(); return; }
      var btn = form.querySelector('[type="submit"]'); var label = btn ? btn.innerHTML : "";
      if (btn) { btn.disabled = true; btn.innerHTML = "Sending…"; }
      var subject = form.getAttribute("data-subject") || form.getAttribute("data-form");
      submitPayload(serialize(form), subject).then(function () {
        status(form, true, form.getAttribute("data-success") || "Thanks! We got it and will reply within 1 business day.");
        track("generate_lead", { form: form.getAttribute("data-form") });
        form.reset();
      }).catch(function () {
        status(form, false, 'Couldn\'t send right now. <a href="#" data-mail-fallback>Email us instead</a> — your message is safe to resend.');
        var fb = form.querySelector("[data-mail-fallback]");
        if (fb) fb.addEventListener("click", function (ev) { ev.preventDefault(); location.href = "mai" + "lto:" + inbox() + "?subject=" + encodeURIComponent("[Biglo] " + subject); });
      }).then(function () { if (btn) { btn.disabled = false; btn.innerHTML = label; } });
    });
  });

  /* ---------- YouTube (lite facade — fast pages, better Core Web Vitals) ---------- */
  function videoCard(v) {
    return '<div class="reveal in"><div class="video" data-yt="' + v.id + '" role="button" tabindex="0" aria-label="Play: ' + v.title.replace(/"/g, "") + '">' +
      '<img loading="lazy" src="https://i.ytimg.com/vi/' + v.id + '/hqdefault.jpg" alt="">' +
      '<span class="play"><i></i></span></div><div class="video-title">' + v.title + "</div></div>";
  }
  $$("[data-videos]").forEach(function (g) { var n = +g.getAttribute("data-videos") || D.videos.length; g.innerHTML = D.videos.slice(0, n).map(videoCard).join(""); });
  function playVideo(el) {
    var id = el.getAttribute("data-yt");
    el.innerHTML = '<iframe src="https://www.youtube-nocookie.com/embed/' + id + '?autoplay=1&rel=0" title="YouTube video" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>';
    track("video_play", { id: id });
  }
  document.addEventListener("click", function (e) { var v = e.target.closest && e.target.closest(".video[data-yt]"); if (v && !v.querySelector("iframe")) playVideo(v); });
  document.addEventListener("keydown", function (e) { if ((e.key === "Enter" || e.key === " ") && e.target.matches && e.target.matches(".video[data-yt]")) { e.preventDefault(); playVideo(e.target); } });

  /* ---------- Deals ---------- */
  var votes = store.get("votes", {});
  function daysLeft(iso) { if (!iso) return null; var d = Math.ceil((new Date(iso + "T23:59:59") - new Date()) / 864e5); return d; }
  function dealCard(d) {
    var off = d.was > d.price && d.price > 0 ? Math.round((1 - d.price / d.was) * 100) : 0;
    var dl = daysLeft(d.ends);
    var badges = [];
    if (d.tags.indexOf("staff") > -1) badges.push('<span class="badge badge-green">★ Staff pick</span>');
    if (d.tags.indexOf("exclusive") > -1) badges.push('<span class="badge badge-amber">Biglo exclusive</span>');
    if (d.tags.indexOf("hot") > -1) badges.push('<span class="badge badge-hot">🔥 Hot</span>');
    if (dl !== null && dl <= 3 && dl >= 0) badges.push('<span class="badge badge-hot">' + (dl === 0 ? "Ends today" : "Ends in " + dl + "d") + "</span>");
    var price = d.price > 0 ? '<div class="price"><b>' + money(d.price) + "</b>" + (d.was ? "<s>" + money(d.was) + "</s>" : "") + "</div>" : '<div class="price"><b>Promo</b><span class="muted">see code</span></div>';
    var code = d.code ? '<div class="code"><span>' + d.code + '</span><button type="button" data-copy="' + d.code + '">Copy</button></div>' : "";
    var voted = votes[d.id];
    return '<article class="deal reveal in"><div class="deal-img" aria-hidden="true">' + d.emoji + (off ? '<span class="off">-' + off + "%</span>" : "") + '</div><div class="deal-body">' +
      '<div style="display:flex;gap:6px;flex-wrap:wrap">' + badges.join("") + "</div><h3>" + d.title + "</h3>" + price + code +
      '<div class="deal-meta"><span>' + d.store + " · " + d.cat + '</span><button type="button" class="vote' + (voted ? " voted" : "") + '" data-vote="' + d.id + '" aria-label="Upvote">▲ <span>' + (d.votes + (voted ? 1 : 0)) + "</span></button></div>" +
      '<a class="btn btn-primary btn-sm btn-block" href="' + d.url + '" rel="sponsored nofollow noopener" target="_blank" data-deal="' + d.id + '">Get deal →</a></div></article>';
  }
  document.addEventListener("click", function (e) {
    var c = e.target.closest && e.target.closest("[data-copy]");
    if (c) { var t = c.getAttribute("data-copy"); (navigator.clipboard ? navigator.clipboard.writeText(t) : Promise.reject()).then(function () { toast("Code " + t + " copied"); }, function () { toast("Code: " + t); }); }
    var v = e.target.closest && e.target.closest("[data-vote]");
    if (v) { var id = v.getAttribute("data-vote"); var n = v.querySelector("span"); if (votes[id]) { delete votes[id]; n.textContent = +n.textContent - 1; v.classList.remove("voted"); } else { votes[id] = 1; n.textContent = +n.textContent + 1; v.classList.add("voted"); } store.set("votes", votes); }
    var g = e.target.closest && e.target.closest("[data-deal]");
    if (g) { track("deal_click", { id: g.getAttribute("data-deal") }); if (g.getAttribute("href") === "#") { e.preventDefault(); toast("Demo listing — affiliate link goes here"); } }
  });
  $$("[data-deals]").forEach(function (g) { var n = +g.getAttribute("data-deals") || 6; g.innerHTML = D.deals.slice().sort(function (a, b) { return b.votes - a.votes; }).slice(0, n).map(dealCard).join(""); });

  var dealGrid = $("#deal-grid");
  if (dealGrid) {
    var state = { cat: "All", q: "", sort: "popular", tag: "" };
    var cats = ["All"].concat(D.deals.map(function (d) { return d.cat; }).filter(function (v, i, a) { return a.indexOf(v) === i; }));
    var chips = $("#deal-cats");
    chips.innerHTML = cats.map(function (c) { return '<button type="button" class="chip' + (c === "All" ? " active" : "") + '" data-cat="' + c + '">' + c + "</button>"; }).join("");
    chips.addEventListener("click", function (e) { var b = e.target.closest("[data-cat]"); if (!b) return; state.cat = b.getAttribute("data-cat"); $$(".chip", chips).forEach(function (x) { x.classList.toggle("active", x === b); }); draw(); });
    $("#deal-q").addEventListener("input", function (e) { state.q = e.target.value.toLowerCase(); draw(); });
    $("#deal-sort").addEventListener("change", function (e) { state.sort = e.target.value; draw(); });
    $("#deal-tag").addEventListener("change", function (e) { state.tag = e.target.value; draw(); });
    function draw() {
      var list = D.deals.filter(function (d) {
        return (state.cat === "All" || d.cat === state.cat) && (!state.q || (d.title + d.store + d.cat).toLowerCase().indexOf(state.q) > -1) && (!state.tag || d.tags.indexOf(state.tag) > -1);
      });
      list.sort(function (a, b) {
        if (state.sort === "new") return b.added.localeCompare(a.added);
        if (state.sort === "ending") return (a.ends || "9999").localeCompare(b.ends || "9999");
        if (state.sort === "discount") { var da = a.was ? 1 - a.price / a.was : 0, db = b.was ? 1 - b.price / b.was : 0; return db - da; }
        return b.votes - a.votes;
      });
      dealGrid.innerHTML = list.length ? list.map(dealCard).join("") : '<p class="muted">No deals match. Try another filter — or set a Deal Alert below.</p>';
      $("#deal-count").textContent = list.length + " deal" + (list.length === 1 ? "" : "s");
    }
    draw();
  }

  /* ---------- Hero quick-start → quote funnel ---------- */
  $$("[data-quickquote]").forEach(function (box) {
    var type = "insurance";
    $$(".pill", box).forEach(function (p) { p.addEventListener("click", function () { type = p.getAttribute("data-type"); $$(".pill", box).forEach(function (x) { x.setAttribute("aria-pressed", x === p); }); }); });
    box.addEventListener("submit", function (e) {
      e.preventDefault(); var zip = (box.querySelector("[name=zip]") || {}).value || "";
      location.href = "quotes.html?type=" + type + (zip ? "&zip=" + encodeURIComponent(zip) : "") + "#start";
    });
  });

  /* ---------- Quote funnel ---------- */
  var funnel = $("#funnel");
  if (funnel) initFunnel(funnel);
  function initFunnel(f) {
    var Q = {
      insurance: { label: "Car & home insurance", steps: [
        { k: "Coverage", q: "What do you want to insure?", opts: ["🚗 Car", "🏠 Home", "🚗+🏠 Bundle (biggest savings)", "🏢 Renters"] },
        { k: "Current provider", q: "Are you currently insured?", opts: ["Yes — renewing soon", "Yes — just shopping", "No, I need new coverage"] },
        { k: "Vehicles/Property", q: "How many vehicles or properties?", opts: ["1", "2", "3", "4+"] },
        { k: "Record", q: "Any claims or tickets in the last 3 years?", opts: ["None", "1", "2 or more"] } ] },
      internet: { label: "Internet & TV", steps: [
        { k: "Current bill", q: "What do you pay for internet now?", opts: ["Under $50", "$50–$80", "$80–$120", "$120+"] },
        { k: "Usage", q: "How do you use it?", opts: ["📧 Browsing & email", "📺 Streaming 4K", "🎮 Gaming", "💼 Work from home"] },
        { k: "Household", q: "People online at home?", opts: ["1–2", "3–4", "5+"] },
        { k: "TV", q: "Want TV or streaming bundled?", opts: ["Internet only", "Add streaming", "Add live TV"] } ] },
      energy: { label: "Energy & solar", steps: [
        { k: "Monthly power bill", q: "Average monthly electricity bill?", opts: ["Under $100", "$100–$200", "$200–$300", "$300+"] },
        { k: "Home ownership", q: "Do you own your home?", opts: ["Yes, I own", "I rent"] },
        { k: "Interest", q: "What are you interested in?", opts: ["☀️ Solar panels", "🔋 Battery backup", "🔌 Cheaper energy plan", "🌡️ Heat pump"] },
        { k: "Roof shade", q: "How much shade does your roof get?", opts: ["Little or none", "Some", "A lot", "Not sure"] } ] },
      loans: { label: "Loans & refinance", steps: [
        { k: "Loan type", q: "What do you need?", opts: ["🏠 Mortgage refinance", "💳 Debt consolidation", "🚗 Auto refinance", "🎓 Student loan refi"] },
        { k: "Amount", q: "How much?", opts: ["Under $10k", "$10k–$50k", "$50k–$250k", "$250k+"] },
        { k: "Credit range", q: "Estimated credit score?", opts: ["Excellent (740+)", "Good (670–739)", "Fair (580–669)", "Rebuilding (<580)"] },
        { k: "Timeline", q: "When do you want to move?", opts: ["ASAP", "Within 30 days", "1–3 months", "Just researching"] } ] },
      phone: { label: "Phone plans", steps: [
        { k: "Lines", q: "How many lines?", opts: ["1", "2", "3–4", "5+"] },
        { k: "Current bill", q: "Total monthly phone bill?", opts: ["Under $50", "$50–$100", "$100–$200", "$200+"] },
        { k: "Data", q: "Data per line per month?", opts: ["Under 5GB", "5–20GB", "Unlimited"] },
        { k: "Phones", q: "Keeping your phones?", opts: ["Yes, bring my own", "Need new phones"] } ] },
      moving: { label: "Moving", steps: [
        { k: "Move size", q: "How big is your move?", opts: ["Studio / 1 bed", "2 bed", "3 bed", "4+ bed"] },
        { k: "Distance", q: "How far?", opts: ["Local (<50 mi)", "Long distance", "International"] },
        { k: "Move date", q: "When are you moving?", opts: ["Within 2 weeks", "Within a month", "1–3 months", "Flexible"] },
        { k: "Services", q: "What help do you need?", opts: ["Full service", "Labor only", "Truck only", "Storage too"] } ] }
    };
    var params = new URLSearchParams(location.search);
    var type = Q[params.get("type")] ? params.get("type") : null;
    var answers = {}; var idx = 0; var steps = [];
    var body = $("#funnel-body"), bar = $(".progress i", f), back = $("#funnel-back"), count = $("#funnel-count");
    function build() {
      steps = [{ k: "Category", q: "What bill do you want to lower?", cat: true }]
        .concat(type ? Q[type].steps : [])
        .concat([{ k: "ZIP", q: "Where do you live?", zip: true }, { k: "Contact", q: "Where should we send your matches?", contact: true }]);
    }
    function render() {
      var s = steps[idx]; var pct = Math.round(((idx + 1) / steps.length) * 100);
      bar.style.width = pct + "%"; count.textContent = "Step " + (idx + 1) + " of " + steps.length;
      back.style.visibility = idx ? "visible" : "hidden";
      var h = "<h2>" + s.q + "</h2>";
      if (s.cat) {
        h += '<div class="choice-grid">' + Object.keys(Q).map(function (k) { return '<button type="button" class="choice' + (type === k ? " selected" : "") + '" data-cat="' + k + '"><span class="e">' + ({ insurance: "🛡️", internet: "📡", energy: "⚡", loans: "🏦", phone: "📱", moving: "🚚" })[k] + "</span>" + Q[k].label + "</button>"; }).join("") + "</div>";
      } else if (s.opts) {
        h += '<div class="choice-grid">' + s.opts.map(function (o) { return '<button type="button" class="choice' + (answers[s.k] === o ? " selected" : "") + '" data-opt="' + o.replace(/"/g, "&quot;") + '">' + o + "</button>"; }).join("") + "</div>";
      } else if (s.zip) {
        h += '<div class="field"><label for="f-zip">ZIP / postal code</label><input id="f-zip" inputmode="text" autocomplete="postal-code" maxlength="10" placeholder="e.g. 10001 or H2X 1Y4" value="' + (answers.ZIP || params.get("zip") || "") + '"></div><button type="button" class="btn btn-primary btn-lg btn-block" id="zip-next">Continue →</button><p class="form-note">We use your location only to match providers who serve your area.</p>';
      } else if (s.contact) {
        h += '<form id="lead-form" novalidate><input class="hp" name="_honey" tabindex="-1" autocomplete="off"><div class="row2"><div class="field"><label for="f-fn">First name</label><input id="f-fn" name="First name" required autocomplete="given-name"></div><div class="field"><label for="f-ln">Last name</label><input id="f-ln" name="Last name" required autocomplete="family-name"></div></div>' +
          '<div class="field"><label for="f-em">Email</label><input id="f-em" name="Email" type="email" required autocomplete="email"></div>' +
          '<div class="field"><label for="f-ph">Phone <span class="muted">(optional — faster quotes)</span></label><input id="f-ph" name="Phone" type="tel" autocomplete="tel"></div>' +
          '<label class="check"><input type="checkbox" name="Consent" value="Yes" required> I agree to be contacted by Biglo and up to 3 matched partners about my request by email, phone or text. Consent is not a condition of purchase. See our <a href="privacy.html" target="_blank">Privacy Policy</a>.</label>' +
          '<button type="submit" class="btn btn-primary btn-lg btn-block mt">Get my free quotes →</button>' +
          '<div class="secure"><span>🔒 256-bit SSL</span><span>🚫 No spam calls</span><span>💸 100% free</span><span>🙅 We never sell your data</span></div></form>';
      }
      body.innerHTML = h;
      var first = body.querySelector("input,button"); if (first && idx) first.focus({ preventScroll: true });
      if (s.zip) { $("#zip-next").addEventListener("click", function () { var z = $("#f-zip").value.trim(); if (z.length < 3) { $("#f-zip").focus(); toast("Please enter your ZIP / postal code"); return; } answers.ZIP = z; next(); }); $("#f-zip").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); $("#zip-next").click(); } }); }
      if (s.contact) $("#lead-form").addEventListener("submit", sendLead);
    }
    function next() { if (idx < steps.length - 1) { idx++; render(); f.scrollIntoView({ behavior: "smooth", block: "start" }); } }
    body.addEventListener("click", function (e) {
      var c = e.target.closest("[data-cat]"); if (c) { type = c.getAttribute("data-cat"); answers = { ZIP: answers.ZIP }; build(); track("funnel_start", { type: type }); setTimeout(next, 120); render(); return; }
      var o = e.target.closest("[data-opt]"); if (o) { answers[steps[idx].k] = o.getAttribute("data-opt"); $$(".choice", body).forEach(function (x) { x.classList.toggle("selected", x === o); }); setTimeout(next, 160); }
    });
    back.addEventListener("click", function () { if (idx) { idx--; render(); } });
    function sendLead(e) {
      e.preventDefault(); var form = e.target;
      if (form._honey.value) return;
      if (!form.checkValidity()) { form.reportValidity(); return; }
      var payload = { "Lead type": Q[type].label }; Object.keys(answers).forEach(function (k) { payload[k] = answers[k]; });
      new FormData(form).forEach(function (v, k) { if (k !== "_honey") payload[k] = v; });
      if (params.get("ref")) payload.Referrer = params.get("ref");
      var btn = form.querySelector("[type=submit]"); btn.disabled = true; btn.textContent = "Matching you…";
      submitPayload(payload, "NEW LEAD — " + Q[type].label + " — " + (answers.ZIP || "")).then(done, function () { done(true); });
      function done(failed) {
        track("generate_lead", { type: type });
        bar.style.width = "100%"; count.textContent = "Done"; back.style.visibility = "hidden";
        body.innerHTML = '<div class="center"><div style="font-size:3rem">🎉</div><h2>You\'re matched, ' + (payload["First name"] || "") + "!</h2>" +
          (failed ? '<p class="lead" style="margin:auto">Our form server is busy — <a href="#" id="lead-mail">tap here to send your request by email</a> and we\'ll still match you today.</p>' : '<p class="lead" style="margin:0 auto 20px">A Biglo savings specialist will review your ' + Q[type].label.toLowerCase() + ' request and send your best options — usually within 1 business day.</p>') +
          '<div class="grid g3 steps-3 mt" style="text-align:left"><div class="card"><h3>We review</h3><p>Your answers are checked against providers serving ' + (answers.ZIP || "your area") + '.</p></div><div class="card"><h3>You compare</h3><p>Up to 3 offers, side by side. No obligation.</p></div><div class="card"><h3>You save</h3><p>Switch only if the numbers win. We do the heavy lifting.</p></div></div>' +
          '<p class="mt"><a class="btn btn-ghost" href="tools.html">Meanwhile, run the Bill Savings calculator →</a></p></div>';
        var lm = $("#lead-mail"); if (lm) lm.addEventListener("click", function (ev) { ev.preventDefault(); var t = Object.keys(payload).map(function (k) { return k + ": " + payload[k]; }).join("\n"); location.href = "mai" + "lto:" + inbox() + "?subject=" + encodeURIComponent("[Biglo] Lead — " + Q[type].label) + "&body=" + encodeURIComponent(t); });
      }
    }
    build();
    if (type) { idx = 1; }
    render();
  }

  /* ---------- Calculators ---------- */
  $$("[data-tool-tab]").forEach(function (b) {
    b.addEventListener("click", function () { var id = b.getAttribute("data-tool-tab"); $$("[data-tool-tab]").forEach(function (x) { x.classList.toggle("active", x === b); x.setAttribute("aria-selected", x === b); }); $$(".tool").forEach(function (t) { t.classList.toggle("active", t.id === id); }); history.replaceState(null, "", "#" + id); });
  });
  if (location.hash && $('[data-tool-tab="' + location.hash.slice(1) + '"]')) $('[data-tool-tab="' + location.hash.slice(1) + '"]').click();
  var num = function (id) { var e = document.getElementById(id); return e ? parseFloat(e.value) || 0 : 0; };
  var set = function (id, v) { var e = document.getElementById(id); if (e) e.innerHTML = v; };
  function bars(id, rows) { var max = Math.max.apply(null, rows.map(function (r) { return r[1]; })) || 1; set(id, rows.map(function (r) { return '<div class="bar-row"><span>' + r[0] + '</span><div class="bar" style="width:' + Math.max(2, r[1] / max * 100) + '%"></div><b>' + money(r[1]) + "</b></div>"; }).join("")); }
  var calcs = {
    bills: function () {
      var items = [["Insurance", num("b-ins"), .18], ["Internet", num("b-net"), .25], ["Phone", num("b-phone"), .35], ["Energy", num("b-energy"), .12], ["Streaming", num("b-stream"), .30]];
      var mo = items.reduce(function (s, i) { return s + i[1] * i[2]; }, 0);
      set("bills-out", money(mo * 12)); set("bills-mo", money(mo)); set("bills-5", money(mo * 60));
      bars("bills-bars", items.map(function (i) { return [i[0], i[1] * i[2] * 12]; }));
    },
    loan: function () {
      var P = num("l-amt"), r = num("l-rate") / 1200, n = num("l-years") * 12;
      var pmt = r ? P * r / (1 - Math.pow(1 + r, -n)) : P / n; var total = pmt * n;
      set("loan-out", money(pmt, 2)); set("loan-total", money(total)); set("loan-int", money(total - P));
      var r2 = Math.max(0, num("l-rate") - 1.5) / 1200, p2 = r2 ? P * r2 / (1 - Math.pow(1 + r2, -n)) : P / n;
      set("loan-refi", money((pmt - p2) * n));
    },
    debt: function () {
      var B = num("d-bal"), r = num("d-apr") / 1200, p = num("d-pay"), m = 0, i = 0;
      if (p <= B * r) { set("debt-out", "Never"); set("debt-int", "Payment too low"); set("debt-extra", "—"); return; }
      var b = B; while (b > 0 && m < 1200) { var it = b * r; i += it; b = b + it - p; m++; }
      set("debt-out", Math.floor(m / 12) + "y " + (m % 12) + "m"); set("debt-int", money(i));
      var b2 = B, m2 = 0, i2 = 0; while (b2 > 0 && m2 < 1200) { var t = b2 * r; i2 += t; b2 = b2 + t - (p + 100); m2++; }
      set("debt-extra", money(i - i2) + " saved, " + (m - m2) + " months sooner");
    },
    savings: function () {
      var goal = num("s-goal"), start = num("s-start"), r = num("s-rate") / 1200, n = num("s-months");
      var fvStart = start * Math.pow(1 + r, n); var need = goal - fvStart;
      var pmt = need <= 0 ? 0 : (r ? need * r / (Math.pow(1 + r, n) - 1) : need / n);
      set("sav-out", money(pmt, 2)); set("sav-week", money(pmt * 12 / 52, 2)); set("sav-int", money(Math.max(0, goal - start - pmt * n)));
    },
    solar: function () {
      var bill = num("so-bill"), cost = num("so-cost"), off = num("so-offset") / 100, inc = num("so-inc") / 100;
      var yr = bill * 12 * off; var net = cost * (1 - inc); var pay = yr ? net / yr : 0;
      var life = 0, y = yr; for (var k = 0; k < 25; k++) { life += y; y *= 1.03; }
      set("solar-out", money(yr)); set("solar-net", money(net)); set("solar-pay", pay ? pay.toFixed(1) + " years" : "—"); set("solar-life", money(life - net));
    },
    budget: function () {
      var inc = num("bu-inc"); set("bu-needs", money(inc * .5)); set("bu-wants", money(inc * .3)); set("bu-save", money(inc * .2));
      bars("bu-bars", [["Needs 50%", inc * .5], ["Wants 30%", inc * .3], ["Save 20%", inc * .2]]);
    },
    unit: function () {
      var a = num("u-pa") / (num("u-qa") || 1), b = num("u-pb") / (num("u-qb") || 1);
      set("unit-a", money(a, 3)); set("unit-b", money(b, 3));
      var better = a === b ? "Same price per unit" : (a < b ? "Option A" : "Option B") + " is cheaper by " + Math.abs((1 - Math.min(a, b) / Math.max(a, b)) * 100).toFixed(1) + "%";
      set("unit-out", better);
    },
    subs: function () {
      var rows = $$("#subs-list .sub-row"); var t = 0, cut = 0;
      rows.forEach(function (r) { var v = parseFloat(r.querySelector("input[type=number]").value) || 0; t += v; if (r.querySelector("input[type=checkbox]").checked) cut += v; });
      set("subs-out", money(cut * 12)); set("subs-total", money(t, 2) + "/mo · " + money(t * 12) + "/yr"); set("subs-keep", money((t - cut) * 12));
    }
  };
  Object.keys(calcs).forEach(function (k) {
    var el = document.getElementById(k); if (!el) return;
    el.addEventListener("input", calcs[k]); el.addEventListener("change", calcs[k]); calcs[k]();
  });
  var addSub = $("#subs-add");
  if (addSub) addSub.addEventListener("click", function () {
    var d = document.createElement("div"); d.className = "sub-row";
    d.innerHTML = '<input aria-label="Subscription name" placeholder="Subscription"><input type="number" min="0" step="0.01" aria-label="Monthly cost" value="9.99"><input type="checkbox" aria-label="Cancel">';
    $("#subs-list").appendChild(d); calcs.subs();
  });

  /* ---------- Donations ---------- */
  var don = $("#donate");
  if (don) {
    var amt = 25, freq = "once";
    $$("[data-amt]", don).forEach(function (b) { b.addEventListener("click", function () { amt = +b.getAttribute("data-amt"); $("#don-custom").value = ""; $$("[data-amt]", don).forEach(function (x) { x.classList.toggle("active", x === b); }); upd(); }); });
    $("#don-custom").addEventListener("input", function (e) { amt = parseFloat(e.target.value) || 0; $$("[data-amt]", don).forEach(function (x) { x.classList.remove("active"); }); upd(); });
    $$("[data-freq]", don).forEach(function (b) { b.addEventListener("click", function () { freq = b.getAttribute("data-freq"); $$("[data-freq]", don).forEach(function (x) { x.classList.toggle("active", x === b); }); upd(); }); });
    function upd() { $("#don-label").textContent = money(amt) + (freq === "monthly" ? "/month" : ""); }
    upd();
    var pp = $("#don-paypal");
    if (C.donate && C.donate.paypal) pp.addEventListener("click", function () {
      if (amt < 1) { toast("Choose an amount"); return; }
      var purpose = ($("#don-purpose") || {}).value || "General operations";
      var u = "https://www.paypal.com/donate?business=" + encodeURIComponent(inbox()) + "&amount=" + amt + "&currency_code=USD&no_recurring=" + (freq === "monthly" ? 0 : 1) + "&item_name=" + encodeURIComponent("Support Biglo — " + purpose);
      track("donate_click", { amount: amt, freq: freq }); window.open(u, "_blank", "noopener");
    }); else pp.style.display = "none";
    [["kofi", "#don-kofi"], ["buymeacoffee", "#don-bmc"], ["stripe", "#don-stripe"]].forEach(function (p) { var el = $(p[1]); if (!el) return; var u = (C.donate || {})[p[0]]; if (u) el.href = u; else el.style.display = "none"; });
    var g = (C.donate || {}).goal || 0, r = (C.donate || {}).raised || 0;
    if ($("#don-meter")) { $("#don-meter").style.width = Math.min(100, g ? r / g * 100 : 0) + "%"; set("don-raised", money(r)); set("don-goal", money(g)); }
  }

  /* ---------- Contest ---------- */
  var cd = $("#countdown");
  if (cd && C.contest) {
    var end = new Date(C.contest.endsAt).getTime();
    var tick = function () {
      var s = Math.max(0, Math.floor((end - Date.now()) / 1000));
      var parts = [Math.floor(s / 86400), Math.floor(s % 86400 / 3600), Math.floor(s % 3600 / 60), s % 60];
      cd.innerHTML = ["Days", "Hours", "Min", "Sec"].map(function (l, i) { return "<div><b>" + String(parts[i]).padStart(2, "0") + "</b><span>" + l + "</span></div>"; }).join("");
    };
    tick(); setInterval(tick, 1000);
  }
  var entries = $("#entries");
  if (entries) {
    var done = store.get("entries", {});
    var refCode = store.get("refcode", null) || Math.random().toString(36).slice(2, 8).toUpperCase(); store.set("refcode", refCode);
    var refUrl = location.origin + location.pathname + "?ref=" + refCode;
    set("ref-link", refUrl);
    function total() { return 1 + Object.keys(done).reduce(function (s, k) { var li = entries.querySelector('[data-entry="' + k + '"]'); return s + (li ? +li.getAttribute("data-pts") : 0); }, 0); }
    function paint() { $$("[data-entry]", entries).forEach(function (li) { li.classList.toggle("done", !!done[li.getAttribute("data-entry")]); }); set("entry-total", total()); var h = $("#entry-count"); if (h) h.value = total(); }
    entries.addEventListener("click", function (e) {
      var b = e.target.closest("[data-entry-go]"); if (!b) return;
      var li = b.closest("[data-entry]"); var k = li.getAttribute("data-entry"); var url = b.getAttribute("data-url");
      if (k === "share") { if (navigator.share) navigator.share({ title: "Win $500 on Biglo", url: refUrl }).catch(function () {}); else if (navigator.clipboard) navigator.clipboard.writeText(refUrl).then(function () { toast("Referral link copied"); }); }
      if (url) window.open(url, "_blank", "noopener");
      done[k] = 1; store.set("entries", done); paint(); toast("+" + li.getAttribute("data-pts") + " entries");
    });
    var ref = new URLSearchParams(location.search).get("ref"); if (ref && $("#entry-ref")) $("#entry-ref").value = ref;
    paint();
  }

  /* ---------- Sticky CTA + exit-intent newsletter ---------- */
  var sticky = $(".sticky-cta");
  if (sticky) window.addEventListener("scroll", function () { sticky.classList.toggle("show", window.scrollY > 900); }, { passive: true });
  var modal = $("#exit-modal");
  if (modal) {
    var shown = false; try { shown = sessionStorage.getItem("biglo_exit") === "1"; } catch (e) {}
    var open = function () { if (shown) return; shown = true; try { sessionStorage.setItem("biglo_exit", "1"); } catch (e) {} modal.classList.add("show"); };
    document.addEventListener("mouseout", function (e) { if (!e.relatedTarget && e.clientY < 10) open(); });
    setTimeout(function () { if (window.innerWidth < 760 && window.scrollY > 1400) open(); }, 45000);
    modal.addEventListener("click", function (e) { if (e.target === modal || e.target.closest(".close")) modal.classList.remove("show"); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") modal.classList.remove("show"); });
  }
})();
