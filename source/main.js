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
      var text = "שלום עו\"ד טל, אשמח לבדיקה ראשונית.\nשם: " + name + "\nטלפון: " + phone + "\nנושא: " + f.elements.topic.value;
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
})();
