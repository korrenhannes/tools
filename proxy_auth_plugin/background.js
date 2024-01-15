var config = {
    mode: "fixed_servers",
    rules: {
      singleProxy: {
        scheme: "http",
        host: "YOUR_PROXY_HOST",
        port: parseInt(YOUR_PROXY_PORT)
      },
      bypassList: ["localhost"]
    }
  };

chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

function callbackFn(details) {
    return {
        authCredentials: {
            username: "YOUR_PROXY_USERNAME",
            password: "YOUR_PROXY_PASSWORD"
        }
    };
}

chrome.webRequest.onAuthRequired.addListener(
        callbackFn,
        {urls: ["<all_urls>"]},
        ['blocking']
);
