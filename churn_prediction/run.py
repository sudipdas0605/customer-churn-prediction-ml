"""Development entry point.

Run with::

    python run.py

For production use a WSGI server, e.g. ``gunicorn "run:app"``.
"""

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host=app.config["HOST"], port=app.config["PORT"], debug=app.config["DEBUG"])
