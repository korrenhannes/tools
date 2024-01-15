from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Smartproxy credentials and proxy details
username = 'sp9zw4gx22'
password = 'kXeSr49iPa5oxhLw3z'
proxy_host = 'gate.smartproxy.com'  # Example host
proxy_port = '10001'  # Example port

proxy_auth_plugin_path = 'proxy_auth_plugin.zip'

# Create a Chrome Options object to configure ChromeDriver
options = Options()

# Set up the proxy with authentication
options.add_argument(f'--proxy-server={proxy_host}:{proxy_port}')

# Initialize the WebDriver with the configured options
driver = webdriver.Chrome(options=options)

# Open a new browser tab with a URL
driver.get('http://google.com')

# Remember to close the browser after your task is done
# driver.quit()
