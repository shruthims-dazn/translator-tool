# English-Korean Translator

A small, dependency-free web translator for English and Korean.

## Run

```sh
cd translator
python3 server.py
```

Open http://127.0.0.1:8790.

For first-time setup on a new laptop, see [setup.md](setup.md).

## Features

- English-to-Korean and Korean-to-English translation
- Language swap
- Copy translated text
- Character limit of 500 characters
- Keyboard shortcut: Command/Ctrl + Enter

Translation uses the public MyMemory API. An internet connection and a network
connection from the local server are required.
