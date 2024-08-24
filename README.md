# Requirements

- Python 3.8 - 3.12.4

# Setup

Create a virtual environment for requirements in the root of the folder and install requirements.

```bash
python3 -m venv venv
# activate venv
source venv/bin/activate

python -m pip install -r requirements.txt
```

Install Tesseract on your linux machine. I found this [installation answer](https://openprompt.co/conversations/4164) after searching solution to my problem. __This bash example belove works only on linux, to find compatible solution for your system check installation answer link above__

```bash
sudo apt-get install tesseract-ocr
```

Thats it you are all set!

# Run

To run the application change your directory to src

```bash
# In the root of the folder change directory to src
cd src/
python scraper.py
```