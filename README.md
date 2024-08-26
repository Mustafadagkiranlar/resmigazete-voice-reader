# Requirements

- Python 3.11.3 (A good version that supports every library)

# Setup

Create a virtual environment for requirements in the root of the folder and install requirements.

```bash
python3 -m venv venv
# activate venv
source venv/bin/activate

python -m pip install -r requirements.txt
```

- You need to create `pdfid.txt` in src folder with the content of `0.pdf`.

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