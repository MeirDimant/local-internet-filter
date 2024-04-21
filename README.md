# Project Setup Instructions

## Prerequisites

Before installing mitmproxy, ensure you have Python 3.8 or newer installed on your system. This is required to ensure full compatibility with mitmproxy.

You can verify your Python version by running:

```bash
python --version
```

If you do not have Python installed, or if your Python version is below 3.8, please install the latest Python version from the [official Python website](https://www.python.org/downloads/).

## Additional Requirements

### Install mitmproxy

To install mitmproxy, run the following command:

```bash
pip install mitmproxy
```

This will install the latest version of mitmproxy.

### Install Firefox

Ensure you have Mozilla Firefox installed on your system. If Firefox is not installed, download and install it from the [official Firefox website](https://www.mozilla.org/firefox/new/).

### Configure Firefox to Use mitmproxy

To make Firefox use mitmproxy for web traffic, follow these steps:

1.  Open Firefox and go to the Preferences menu.
2.  Scroll to the Network Settings section and click on `Settings...`.
3.  In the Connection Settings dialog, select the option `Manual proxy configuration`.
4.  Set the HTTP Proxy to `localhost` and the Port to `8080` (or whatever port you configured mitmproxy to listen on).
5.  Check the option `Also use this proxy for HTTPS`.
6.  Click OK to save the settings.

Now, when you browse with Firefox, all web traffic will pass through mitmproxy.

### Install mitmproxy CA Certificate in Firefox

To allow mitmproxy to intercept HTTPS traffic, Firefox must trust the mitmproxy Certificate Authority (CA). You can install the CA certificate by following these steps:

1.  **Run mitmproxy:** Start the mitmproxy tool on your computer. You can do this by typing `mitmproxy`, `mitmdump`, or `mitmweb` in your command line or terminal.
2.  **Access the mitmproxy's web interface:** Open a web browser and navigate to [http://mitm.it](http://mitm.it). This page is served directly by mitmproxy and provides links to download the certificate for various operating systems and browsers.
3.  **Download the Certificate:** Click on the appropriate link to download the mitmproxy certificate for Firefox. The file usually ends with a `.pem` or `.crt` extension.
4.  **Install the Certificate in Firefox:**
    - Open Firefox.
    - Go to settings by clicking the menu button and selecting "settings".
    - Scroll down to "Privacy & Security" and go to the "Certificates" section.
    - Click on "View Certificates" to open the Certificate Manager.
    - In the Certificate Manager, go to the "Authorities" tab.
    - Click "Import" and select the downloaded certificate file.
    - Confirm that you want to trust this certificate for identifying websites.
5.  **Restart Firefox:** Close and reopen Firefox to ensure that the changes take effect.

## Setup Script

1.  Create a new shell script file named `script-test.sh` in your preferred directory.
2.  Open the `script-test.sh` file with a text editor of your choice and add the following line:

```bash
mitmweb.exe -s <directory>/runner.py --no-web-open-browser --mode regular@8080
```

**Note:** Replace `<directory>` with the actual path to the root directory where the `runner.py` file is located.

3.  Save the file and close the editor.

This script configures mitmweb to run without opening a browser and sets it to regular mode on port 8080.
