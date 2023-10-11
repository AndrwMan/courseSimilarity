# courseSimilarity
Given a pdf version of transcript, extract the taken courses. Then with extracted courses match them with their descriptions with relevant online course catalogs. With course signatures and course description pairs model how closely the courses are with NLP methods.  

## Motivation
* Pratice regular expressions when text parsing
* Pratice web-scraping with beautifulSoup
* Pratice using common python data science libraries (pandas, matplotlib)
* Apply common python machine learning library (sklearn) to text data
* Explore data visualization and user interactivity with visuals     

## Usage 
Intended for personal use. (Especially since parsing & scarping is specific to the transcripts & catalog structure used by UCSD). Still, the current build process involves the following: 

### Dependency Installation
1. Check if Python 3 is installed with `python3 --version`. If not, get python Python interpreter and standard library (https://www.python.org/downloads/windows/)
2. a.  Windows/macOS: Run the installer and check the box that says "Add Python x.x to PATH" during the installation. Follow wizard instructions to complete the installation. 
2. b. Linux: `sudo apt update`, `sudo apt install python3`

3. Check if pip is installed with `pip --version`. If you see a version number, then pip is already installed. If not, use `curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py`, then `python get-pip.py`

4. Use pip to install Python dependencies. Install a package with `pip install <package-name>`. pip install pdfplumber, beautifulsoup4, etc. Check the import statements of .py files. 
  * certain libraries (internal) don't need install; but still need import `re` 

### Configuration
* copy the relevant file into the project root, and specify it in `raw_pdf_file`

## License
**Copyright (c) [Andrew Man] [2019-2023]. All Rights Reserved.**
