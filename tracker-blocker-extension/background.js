let blockedCount = 0;
let trackerList = [
  "doubleclick.net",
  "google-analytics.com",
  "facebook.com"
];

browser.webRequest.onBeforeRequest.addListener(
  function(details) {
    let url = details.url;

    for (let tracker of trackerList) {
      if (url.includes(tracker)) {
        blockedCount++;

        browser.browserAction.setBadgeText({
          text: blockedCount.toString()
        });

        return { cancel: true };
      }
    }
  },
  { urls: ["<all_urls>"] },
  ["blocking"]
);
