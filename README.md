# KeyLeacher: JavaScript API Key and Token Scanner

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

**KeyLeacher** is a Python-based tool that scans JavaScript files of websites for sensitive information such as API keys, tokens, and CAPTCHA keys. It automates the process of detecting potentially exposed secrets in a site's frontend code, helping security researchers and developers to identify vulnerabilities in their web applications.

## Features

- Scans JavaScript files for sensitive data such as:
  - API keys
  - Authentication tokens
  - reCAPTCHA and hCaptcha keys
- Alerts the user when sensitive information is found
- Supports both absolute and relative URLs for JavaScript files
- Can be run on any server or local machine
- Simple and easy-to-use

## Requirements

- Python 3.x
- Required Libraries:
  - `requests`
  - `beautifulsoup4`

To install the required libraries, use the following command:

```bash
pip install -r requirements.txt
```

# Installation
Clone the Repository

First, clone the repository to your local machine:

```git clone https://github.com/yourusername/key-leacher.git```
```cd key-leacher```

# Install Dependencies

Once inside the project directory, install the required libraries using pip:

pip install -r requirements.txt

Usage


```
python3 main.py
```
Enter the website URL you want to scan when prompted:

    Enter website URL: http://example.com

    The tool will scan the JavaScript files linked from the page and notify you of any sensitive information it finds. If no sensitive information is found, it will display a message indicating that.

Example Output:

If sensitive information is found:
```
Enter website URL: http://example.com
[+] Found sensitive info in: http://example.com/script1.js
    - API Key: ['12345ABCDE']
    - Token: ['my-secret-token-67890']
    - Captcha: ['6Lc_aXQTAAAAANMy5']
```
If no sensitive information is found:
```
Enter website URL: http://example.com
[-] No sensitive information found.
```
How It Works

    Extract JavaScript URLs: The tool scrapes the website's HTML to identify all linked JavaScript files.

    Scan JavaScript for Sensitive Data: For each JavaScript file, it scans the content for patterns related to API keys, tokens, and CAPTCHA keys.

    Report Findings: If any sensitive information is detected, the tool will output the results with details about the found data.

Contributing

Contributions are welcome! If you find bugs or have suggestions for improvements, feel free to open issues or submit pull requests.

To contribute:

    Fork the repository

    Create a new branch (git checkout -b feature-branch)

    Make your changes and commit them (git commit -am 'Add new feature')

    Push to the branch (git push origin feature-branch)

    Create a pull request

License

This tool is open-source and licensed under the MIT License.

Disclaimer:
This tool is intended for use in legal and ethical security research only. Always ensure you have permission to scan and test any website or web application.


