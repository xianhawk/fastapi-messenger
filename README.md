# FastChat

FastChat - this is a **FastAPI** web application for chatting.

## Install

Activate the *virtual environment* and install the modules with the *command*:

```console
pip install -r requirements.txt
```

+ Used modules:
  + fastapi[all]
  + SQLAlchemy
  + passlib[bcrypt]
  + PyJWT
  + flask-admin

## Launching

For a quick launch, you can simply run the file `main.py`.

```console
...\messenger\backend>$ python main.py
```

You can use [**`uvicorn`**](https://www.uvicorn.org/) for more fine-tuning the startup.
