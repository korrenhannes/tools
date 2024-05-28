from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Smartproxy credentials and proxy details
username = 'sp9zw4gx22'
password = 'kXeSr49iPa5oxhLw3z'
proxy_host = 'il.smartproxy.com'
proxy_port = '30001'

# Path to the proxy authentication Chrome extension
proxy_auth_plugin_path = '/Users/korrenhannes/Desktop/random shit/proxy_auth_plugin/Archive.zip'

# Create a Chrome Options object to configure ChromeDriver
chrome_options = Options()
chrome_options.add_argument("user-agent=Mozilla/5.0")

# Set up the proxy with authentication
chrome_options.add_argument(f'--proxy-server={proxy_host}:{proxy_port}')

# Add the proxy authentication extension
chrome_options.add_extension(proxy_auth_plugin_path)

# Initialize the WebDriver with the configured options
driver = webdriver.Chrome(options=chrome_options)

# Open a new browser tab with a URL
driver.get('http://google.com')

# Add a pause to observe the behavior
input("Press Enter to close the browser")

# Close the browser
driver.quit()
