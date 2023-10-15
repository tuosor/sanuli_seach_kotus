# What is this repository about
I regularly play Sanuli (Finnish Wordle: https://sanuli.fi/), but I got stuck with a rather exotic (non-Finnish) origin word. Thus, I wrote this little script to find the word I was looking for based on the clues I had gathered, i.e. locations of certain letters and exclusions of some.
Implemented on Python version 3.11.5, on 64-bit Windows 10.

## First, download and unzip the Kotus library that Sanuli uses.
The library is found in: https://kaino.kotus.fi/sanat/nykysuomi/.


## Fire up your cmd.
Change to your directory (replace *your directory here* below) and create virtual environment.
```
cd *your directory here*
python -m venv venv
.\venv\Scripts\activate
```

## Install requirements
```
pip install -r requirements.txt
```

## Modify the KOTUS_FILE_PATH (path to the xml file you unzipped).


## Run script
```
python search_kotus_hack.py
```
