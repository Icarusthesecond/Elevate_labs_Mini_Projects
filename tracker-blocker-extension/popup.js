function updateCount() {
  chrome.storage.local.get(["blocked"], function(data) {
    document.getElementById("count").innerText = data.blocked || 0;
  });
}

function addWhitelist() {
  let site = document.getElementById("site").value;

  chrome.storage.local.get(["whitelist"], function(data) {
    let list = data.whitelist || [];
    list.push(site);

    chrome.storage.local.set({ whitelist: list });
    alert("Added to whitelist");
  });
}

updateCount();
