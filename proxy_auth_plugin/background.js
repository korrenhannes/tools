var config = {
  mode: "fixed_servers",
  rules: {
    singleProxy: {
      scheme: "http",
      host: "gate.smartproxy.com", // Your proxy host
      port: parseInt(10001) // Your proxy port
    },
    bypassList: ["localhost"]
  }
};

chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

function callbackFn(details) {
  return {
      authCredentials: {
          username: "sp9zw4gx22", // Your proxy username
          password: "kXeSr49iPa5oxhLw3z" // Your proxy password
      }
  };
}

chrome.webRequest.onAuthRequired.addListener(
      callbackFn,
      {urls: ["<all_urls>"]},
      ['blocking']
);
