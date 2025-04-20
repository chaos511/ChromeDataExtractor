# ChromeDataExtractor

ChromeDataExtractor is a Python-based tool designed to extract sensitive data such as cookies and passwords stored in Google Chrome's local database. This repository contains two scripts, `cookie_extractor.py` and `password_extractor.py`, which allow users to retrieve and decrypt their Chrome data for analysis or backup purposes.

## Features

- **Cookie Extraction**: The `cookie_extractor.py` script allows users to extract and decrypt Chrome's stored cookies, saving them in a JSON format for easy access and analysis.
- **Password Extraction**: The `password_extractor.py` script enables users to extract and decrypt saved passwords in Google Chrome, saving them in a text file for later use.

## Prerequisites

To use this tool, you need the following Python libraries installed:

- `pywin32`: Required for interacting with Windows APIs.
- `pycryptodome`: Required for AES decryption of the Chrome data.
- `sqlite3`: For interacting with Chrome's SQLite databases.
- `base64`: For handling encoded data.
- `shutil`: For file manipulation.

You can install the necessary libraries with the following command:

```bash
pip install -r requirements.txt
