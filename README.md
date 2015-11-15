# calvinbookshelf-db

## Summary

This repository includes various scripts that were used to scrape class and book data for calvinbookshelf.

## Installation

### 1. Clone the Repository

Enter the directory that you use for git projects, then run:
```bash
$ git clone https://github.com/cs262teamd/calvinbookshelf-db
```

### 2. Set up your Virtual Environment

Install virtualenv.
```bash
$ pip install virtualenv
```
Create a virtual environment named `venv` by navigating into the `calvinbookshelf-db` directory and running:
```bash
$ virtualenv venv
```
You should have your virtual environment active while working on this project. To activate it, enter:
```bash
$ . venv/bin/activate
```
While your virtual environment is active, install the project's python dependencies with:
```bash
(venv)$ pip install -r requirements.txt
```
If you made a change to the project's dependencdies, run this in your virtual environment before committing:
```bash
(venv)$ pip freeze > requirements.txt
```
Don't forget to deactivate your virtual environment when you're done working in the repository. To do so, simply run:
```bash
(venv)$ deactivate
```

### 3. Install the WebDriver for Chrome

* Download the latest chromedriver release [here](https://sites.google.com/a/chromium.org/chromedriver/downloads).
* Extract the .zip file and place the chromedriver executable in a safe location, where it will not need to move.
* Append the line `export CHROMEDRIVER_PATH='/path/to/chromedriver'` to your `~/.profile` or `~/.bashrc` file.

## Scraping data

As of right now, the data scraping is a two-step process:

1. `scrape_classlist.py` is run to find a classlist for every term. It dumps its results to `data/`.

2. `scraper.py` is run to find book data for each of the files in `data/`. It dumps its results to `db/`.

Make sure that you've activated your virtual environment before running any scripts.
