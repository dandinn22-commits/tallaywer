(function () {
  var WA = "972536199967";
  window.dataLayer = window.dataLayer || [];
  function track(name) {
    window.dataLayer.push({ event: name });
    if (typeof window.gtag === "function") window.gtag("event", name);
  }
  var btn = document.querySelector(".menu-btn"), nav = document.getElementById("nav");
  if (btn && nav) btn.addEventListener("click", function () {
    var open = nav.classList.toggle("open");
    btn.setAttribute("aria-expanded", open ? "true" : "false");
  });
  document.querySelectorAll("[data-ev]").forEach(function (a) {
    a.addEventListener("click", function () { track(a.getAttribute("data-ev") + "_click"); });
  });

  document.querySelectorAll("[data-lead]").forEach(function (f) {
    f.addEventListener("submit", function (ev) {
      ev.preventDefault();
      var err = f.querySelector(".err");
      var name = f.elements.name.value.trim();
      var phone = f.elements.phone.value.replace(/[\s\-()]/g, "").replace(/^\+972/, "0");
      if (name.length < 2) { err.textContent = "כתבו שם מלא כדי שנדע איך לפנות אליכם."; err.hidden = false; f.elements.name.focus(); return; }
      if (!/^0\d{8,9}$/.test(phone)) { err.textContent = "מספר הטלפון לא תקין. כתבו מספר ישראלי, למשל 0501234567."; err.hidden = false; f.elements.phone.focus(); return; }
      err.hidden = true;
      var text = "שלום עו\"ד טל, אשמח לבדיקת התיק.\nשם: " + name + "\nטלפון: " + phone + "\nנושא: " + f.elements.topic.value;
      track("lead_submit");
      window.open("https://wa.me/" + WA + "?text=" + encodeURIComponent(text), "_blank", "noopener");
      window.location.href = "thanks.html";
    });
  });

  function addYears(d, n) {
    var r = new Date(d.getTime());
    r.setFullYear(r.getFullYear() + n);
    return r;
  }
  function deadline(event, found, birth) {
    var r = addYears(event, 7);
    if (found && found > event) {
      var late = addYears(found, 7), cap = addYears(event, 10);
      var v = late < cap ? late : cap;
      if (v > r) r = v;
    }
    if (birth && addYears(birth, 18) > event) {
      var m = addYears(birth, 25);
      if (m > r) r = m;
    }
    return r;
  }
  window.__deadline = deadline;
  document.querySelectorAll("[data-calc]").forEach(function (f) {
    var out = f.parentNode.querySelector("[data-out]");
    f.addEventListener("submit", function (ev) {
      ev.preventDefault();
      var ins = f.querySelectorAll("input");
      out.hidden = false; out.textContent = "";
      if (!ins[0].value) { out.textContent = "בחרו את תאריך הטיפול כדי לחשב."; return; }
      var d = function (i) { return ins[i].value ? new Date(ins[i].value + "T00:00:00") : null; };
      var r = deadline(d(0), d(1), d(2)), now = new Date();
      var b = document.createElement("b");
      b.textContent = r.toLocaleDateString("he-IL", { day: "numeric", month: "long", year: "numeric" });
      var p = document.createElement("p");
      if (r < now) {
        p.textContent = "לפי החישוב הכללי המועד כבר עבר, אבל יש חריגים. כדאי לבדוק לפני שמוותרים.";
      } else {
        var m = Math.floor((r - now) / (1000 * 60 * 60 * 24 * 30.44));
        p.textContent = "נותרו כ-" + m + " חודשים לפי החישוב הכללי. השגת תיק רפואי וחוות דעת נמשכת זמן, ולכן כדאי להתחיל מוקדם.";
      }
      out.appendChild(b); out.appendChild(p);
    });
  });

  // נגישות
  function store(k, v) { try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch (e) { return null; } }
  var root = document.documentElement, ab = document.querySelector(".a11y-btn"), panel = document.getElementById("a11y");
  var scale = 0, flags = { contrast: 0, links: 0, still: 0 };
  try { var sv = JSON.parse(store("a11y") || "{}"); scale = sv.scale || 0; ["contrast", "links", "still"].forEach(function (k) { flags[k] = sv[k] || 0; }); } catch (e) {}
  function apply() {
    document.body.style.zoom = scale ? String(1 + scale * 0.15) : "";
    ["contrast", "links", "still"].forEach(function (k) {
      root.classList.toggle("a-" + k, !!flags[k]);
      var b = panel && panel.querySelector('[data-a="' + k + '"]');
      if (b) b.setAttribute("aria-pressed", flags[k] ? "true" : "false");
    });
    store("a11y", JSON.stringify({ scale: scale, contrast: flags.contrast, links: flags.links, still: flags.still }));
  }
  if (ab && panel) {
    function toggle(o) { panel.hidden = !o; ab.setAttribute("aria-expanded", o ? "true" : "false"); }
    ab.addEventListener("click", function () { toggle(panel.hidden); if (!panel.hidden) panel.querySelector("button").focus(); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape" && !panel.hidden) { toggle(false); ab.focus(); } });
    panel.addEventListener("click", function (e) {
      var a = e.target.getAttribute && e.target.getAttribute("data-a"); if (!a) return;
      if (a === "bigger") scale = Math.min(2, scale + 1);
      else if (a === "smaller") scale = Math.max(0, scale - 1);
      else if (a === "reset") { scale = 0; flags = { contrast: 0, links: 0, still: 0 }; }
      else flags[a] = flags[a] ? 0 : 1;
      apply();
    });
    apply();
  }
  // עוגיות: גוגל נטענת רק אחרי אישור, ורק אם הוגדר מזהה
  var id = window.SITE_GTAG;
  function loadG() {
    var s = document.createElement("script"); s.async = true; s.src = "https://www.googletagmanager.com/gtag/js?id=" + id; document.head.appendChild(s);
    window.gtag = function () { window.dataLayer.push(arguments); }; window.gtag("js", new Date()); window.gtag("config", id);
  }
  if (id) {
    var c = store("consent"), box = document.querySelector("[data-consent]");
    if (c === "y") loadG();
    else if (!c && box) {
      box.hidden = false;
      box.addEventListener("click", function (e) { var v = e.target.getAttribute && e.target.getAttribute("data-c"); if (!v) return; store("consent", v); box.hidden = true; if (v === "y") loadG(); });
    }
  }
})();
