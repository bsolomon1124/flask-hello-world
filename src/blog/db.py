import psycopg2
import psycopg2.extras

import click
from flask import current_app
from flask import g
from flask import Flask
from flask.cli import with_appcontext

# Note: unlike the sqlite connection object, which has an .execute()
# that is a shortcut and creates a cursor object, psycopg2 asks us
# to create the cursor object explicitly.


def get_db():
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    if "db" not in g:
        g.conn = psycopg2.connect(dbname=current_app.config["DATABASE"])
        current_app.logger.info("Connected to %r on %d", g.conn.info.dbname, g.conn.info.port)
    return g.conn


def close_db(e=None):
    """If this request connected to the database, close the
    connection.
    """
    conn = g.pop("db", None)
    if conn is not None:
        current_app.logger.info("Closing connection to %r on %d", conn.info.dbname, conn.info.port)
        conn.close()
        if conn.closed:
            current_app.logger.debug("Closed connection successfully")


def init_db() -> None:
    """Clear existing data and create new tables."""
    conn = get_db()
    with current_app.open_resource("schema.sql") as f:
        contents = f.read().decode("utf8")
        print(contents)
        with conn.cursor() as cur:
            print(conn.info.dbname, conn.info.port, conn.info.user)
            cur.execute(contents)
        conn.commit()  # This is required to make changes persistent, otherwise the tables don't get created


@current_app.cli.command("init-db")
def init_db_command():
    """Clear existing data and create new tables."""
    # Note: this requires that you pip-install the project.
    init_db()


def init_app(app: Flask) -> None:
    """Register database functions with the Flask app. This is called by
    the application factory.
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
