# First-time setup

This guide is for a new laptop that does not have Python installed. You do not
need to install any extra Python packages for this project.

## 1. Get the project files

Copy or download the project onto your laptop, then locate the `translator`
folder. It should contain `server.py` and the `static` folder. If you received
the whole project as a ZIP file, extract it first.

## 2. Install Python

Install Python 3.10 or newer. Python includes everything this project needs.

- **macOS:** Download the macOS installer from
  [python.org/downloads](https://www.python.org/downloads/), open the downloaded
  `.pkg` file, and follow the installer steps.
- **Windows:** Download the Windows installer from
  [python.org/downloads](https://www.python.org/downloads/). Run it and select
  **Add python.exe to PATH** on the first installer screen before choosing
  **Install Now**.
- **Linux:** Python 3 is often already installed. If not, install Python 3 using
  your Linux distribution's software manager or package manager.

To check the installation, open Terminal (macOS/Linux) or Command Prompt
(Windows) and run:

```text
python3 --version
```

On Windows, try `py --version` if `python3` is not recognized. The version
should be 3.10 or newer.

## 3. Open a terminal in the `translator` folder

Change directory to the folder containing `server.py`. For example, if the
project is in Downloads:

```sh
cd ~/Downloads/codebase/translator
```

On Windows, the equivalent might be:

```bat
cd %USERPROFILE%\Downloads\codebase\translator
```

If you saved the project somewhere else, replace the example path with the
actual path. You can check that you are in the right folder by listing its
files: use `ls` on macOS/Linux or `dir` on Windows. You should see `server.py`
and `static`.

## 4. Start the translator

On macOS or Linux, run:

```sh
python3 server.py
```

On Windows, run:

```bat
py server.py
```

Leave the terminal window open while you use the translator. It should report
that it is running at `http://127.0.0.1:8790`.

## 5. Use it

Open [http://127.0.0.1:8790](http://127.0.0.1:8790) in your browser. Enter up
to 500 characters, then select **Translate**. Use the swap button to switch
between English-to-Korean and Korean-to-English.

To stop the server, return to the terminal and press **Ctrl+C**. Start it again
with the command in step 4 whenever you want to use the app.

## Troubleshooting

- **`python3` or `py` is not recognized:** Python may not be installed, or the
  terminal may have been open during installation. Install Python, close and
  reopen the terminal, then check its version again.
- **The browser cannot connect:** Confirm the server is still running in the
  terminal and the address is exactly `http://127.0.0.1:8790`.
- **Port 8790 is already in use:** Start the server on another port, for example
  `python3 server.py --port 8791` (macOS/Linux) or
  `py server.py --port 8791` (Windows), then open
  `http://127.0.0.1:8791`.
- **Translation fails:** The app needs an internet connection to contact the
  MyMemory translation service. Check your connection and try again.

Text submitted for translation is sent to the public MyMemory service. Do not
use this app for confidential or sensitive text.
