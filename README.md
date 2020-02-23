# AutomationScripts
Some small ideas and projects working with python. At the moment, these scripts work primarily with Linux distros. You will have to configure them for windows/OSX etc.

# requirements:
- Python 3.7 (https://www.python.org/)
- bs4
- pandas
- selenium 
- geckodriver
- chromedriver
- requests
- prettytable

# For Linux 
python 3 should already be installed out of the box for linux distros

Command line:
- pip3 install bs4 pandas selenium requests prettytable

browser drivers can be found at https://github.com/mozilla/geckodriver/releases for geckodriver, and https://chromedriver.chromium.org/ for chromedriver. By default, these scripts use geckodriver unless otherwise specified.

once downloaded:
- sudo tar -xvf geckodriver-v0.{version}.0-linux{os bit type}.tar.gz
- for example: sudo tar -xvf geckodriver-v0.26.0-linux64.tar.gz

then:
- mv geckodriver /usr/bin/



