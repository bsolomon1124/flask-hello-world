from flask import Blueprint
from flask import abort, current_app, request
from flask import jsonify

from .db import get_db

bp = Blueprint("api", __name__, url_prefix="/api")


@bp.route("/create", methods=("POST",))
def create():
    if request.method == "POST":
        data = request.get_json()
        title = data.get("title")
        body = data.get("body")
        if not title or not body:
            abort(400)
        conn = get_db()
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO posts (title, body, author_id) VALUES (%s, %s, %s)",
                (title, body, 1),
            )
            current_app.logger.info("Created post: %r", title)
        conn.commit()
        return "OK!"
    else:
        abort(405)  # 405 -> Method Not Allowed
