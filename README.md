<label id="top"></label>

<div align="center">
  <h1>Programming Languages Dictionary</h1>
  <h3>Formerly Known: AutoUpdate Languages 2</h3>
</div>

Table of Contents:

- [Introduction](#introduction)
- [Installation](#installation)

---

### Introduction

<u><i>Programming Languages Dictionary</i></u> is a PySide6 application that utilizes Python's [requests](https://pypi.org/project/requests/) and [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/) libraries to scrape, build, and display a list of all currently known programming languages, esoterik included.

---

### Installation

At this time, this project is currently built and compiled for Linux/Mac, using bash, as that is the current active development environment. In future dates, Windows options will become available.

<b><u>To Compile From Source</u></b>

1. Clone the repo
  - `git clone https://github.com/mek0124/programming-languages-dictionary.git`

2. CD into the project
  - `cd programming-languages-dictionary`

3. Run the project via the scripts/run.sh file or with python3
  - `bash scripts/run.sh` or with `python3 main.py`

<b><u>To Run From .AppImage</u></b>

1. Download the latest release from the releases page
  - https://github.com/mek0124/programming-languages-dictionary/releases/latest

2. Unzip the project with 7zip or Tar
  - `7z x programming-languages-dictionaryv1.0.0.tar.gz` or `tar -xvzf programming-languages-dictionaryv1.0.0.tar.gz`

3. CD into the project
  - `cd programming-languages-dictionaryv1.0.0` 
  
4. Run the .AppImage
  - `./dist/programming-languages-dictionary`