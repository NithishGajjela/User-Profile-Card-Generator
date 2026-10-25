# User Profile Card Generator

A small Flask application that accepts profile details as JSON, validates and normalizes them on the server, and displays the returned profile in a responsive card without reloading the page.

## Requirements

- Python 3.9 or newer
- Windows PowerShell

## Run on Windows

Open PowerShell in the project folder and run:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

If PowerShell blocks virtual-environment activation, run the commands below instead (the activation command is not required):

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

Open <http://127.0.0.1:5000> in your browser. Stop the development server with `Ctrl+C`.

## Test

With the project environment active, run:

```powershell
python -m unittest discover -s tests -v
```

## Request and validation

The browser sends a JSON `POST` request to `/generate-profile`. The Flask endpoint trims and validates the submitted fields and responds with either a `profile` object or a JSON error. Names are limited to 80 characters, bios to 300, roles to 80, image URLs to 2048, and skills to 12 items of at most 30 characters each. Image URLs must use HTTP or HTTPS. No profile data is saved.
