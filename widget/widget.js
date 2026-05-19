(function () {
  var script = document.currentScript;
  if (!script) {
    var scripts = document.getElementsByTagName("script");
    script = scripts[scripts.length - 1];
  }

  var siteKey = script && (script.getAttribute("data-site-id") || script.getAttribute("data-site-key"));
  if (!siteKey) {
    console.warn("KoyunChat: missing data-site-id");
    return;
  }

  var scriptUrl = new URL(script.src);
  var baseUrl = scriptUrl.origin;
  var storageKey = "koyunchat_visitor_uid_" + siteKey;
  var visitorUid = localStorage.getItem(storageKey);
  if (!visitorUid) {
    visitorUid = "visitor_" + Math.random().toString(36).slice(2) + Date.now().toString(36);
    localStorage.setItem(storageKey, visitorUid);
  }

  function postJson(path, body) {
    return fetch(baseUrl + path, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
      credentials: "omit"
    }).catch(function () {
      return null;
    });
  }

  var iframe = document.createElement("iframe");
  iframe.title = "KoyunChat";
  iframe.src = baseUrl + "/widget/" + encodeURIComponent(siteKey) + "?visitor_uid=" + encodeURIComponent(visitorUid);
  iframe.style.position = "fixed";
  iframe.style.right = "20px";
  iframe.style.bottom = "20px";
  iframe.style.width = "380px";
  iframe.style.height = "620px";
  iframe.style.maxWidth = "calc(100vw - 24px)";
  iframe.style.maxHeight = "calc(100vh - 24px)";
  iframe.style.border = "0";
  iframe.style.zIndex = "2147483647";
  iframe.style.background = "transparent";
  iframe.style.display = "none";
  iframe.allow = "clipboard-write";

  var launcher = document.createElement("button");
  launcher.type = "button";
  launcher.setAttribute("aria-label", "Open chat");
  launcher.innerHTML = "Chat";
  launcher.style.position = "fixed";
  launcher.style.right = "20px";
  launcher.style.bottom = "20px";
  launcher.style.height = "54px";
  launcher.style.minWidth = "82px";
  launcher.style.border = "0";
  launcher.style.borderRadius = "999px";
  launcher.style.background = "#2563eb";
  launcher.style.color = "#fff";
  launcher.style.font = "700 15px system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif";
  launcher.style.boxShadow = "0 14px 36px rgba(37, 99, 235, 0.35)";
  launcher.style.cursor = "pointer";
  launcher.style.zIndex = "2147483647";

  function setOpen(open) {
    iframe.style.display = open ? "block" : "none";
    launcher.style.display = open ? "none" : "block";
    iframe.contentWindow && iframe.contentWindow.postMessage({ type: open ? "koyunchat_open" : "koyunchat_close" }, baseUrl);
  }

  launcher.addEventListener("click", function () {
    setOpen(true);
  });

  window.addEventListener("message", function (event) {
    if (event.origin !== baseUrl || !event.data) return;
    if (event.data.type === "koyunchat_close") {
      setOpen(false);
    }
  });

  document.body.appendChild(iframe);
  document.body.appendChild(launcher);

  var pagePayload = {
    site_key: siteKey,
    visitor_uid: visitorUid,
    url: window.location.href,
    title: document.title,
    referrer: document.referrer || null,
    language: navigator.language,
    screen_width: window.screen && window.screen.width,
    screen_height: window.screen && window.screen.height
  };

  postJson("/api/widget/init", pagePayload);

  var params = new URLSearchParams(window.location.search);
  postJson("/api/widget/page-view", {
    site_key: siteKey,
    visitor_uid: visitorUid,
    url: window.location.href,
    title: document.title,
    referrer: document.referrer || null,
    utm_source: params.get("utm_source"),
    utm_medium: params.get("utm_medium"),
    utm_campaign: params.get("utm_campaign")
  });
})();
