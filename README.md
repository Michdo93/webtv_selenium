# webtv_selenium
A Python script for login to german webtv livestreams via your browser.

# Installation

At first you have to install

```
python3 -m pip install PyAutoGUI
python3 -m pip install numpy
python3 -m pip install pillow
python3 -m pip install opencv-python
python3 -m pip install selenium
```

Then you have to clone the repository with:

```
git clone https://github.com/Michdo93/webtv_selenium.git
```

Also you have to make sure that you have installed your browser and browser driver. This could be the [geckodriver](https://github.com/mozilla/geckodriver/releases) for Mozilla Firefox or [ChromeDriver](https://chromedriver.chromium.org/downloads/version-selection) for your Chrome browser.

Also your Browser and your Browser Driver must be in the `PATH` variable because `shutil` should find it.

# Configuration

You have to change the `<path/to/images>` to the path where you have placed your images. Then you have to change `<email>` and `<password>` with the email address and password of your account.

# Usage

You can run it with following arguments:

```
# Kabel Eins
python3 selenium.py "Kabel Eins"

# Kabel Eins Doku
python3 selenium.py "Kabel Eins Doku"

# Sat.1
python3 selenium.py "SAT.1"

# Sat.1 Gold
python3 selenium.py "SAT1.GOLD"

# Pro 7
python3 selenium.py "ProSieben"

# Pro 7 Maxx
python3 selenium.py "ProSieben MAXX"

# sixx
python3 selenium.py "sixx"
```

Normally `shutil` should find your browser driver and browser if they are in the `PATH` variable.
