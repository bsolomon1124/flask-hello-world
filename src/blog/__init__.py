import logging
import os

from flask import Flask

# Set loglevel to info by default so that we get info logs even when FLASK_DEBUG is off
# See https://github.com/pallets/flask/blob/master/src/flask/logging.py
logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s in %(module)s: %(message)s")


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE="blog",
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        # if silent=False (default), raise if file does not exist
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # register the database commands

    with app.app_context():
        from blog import db
        db.init_app(app)

    # apply the blueprints to the app
    # from blog import blog
    from blog import api

    # app.register_blueprint(auth.bp)
    # app.register_blueprint(blog.bp)
    app.register_blueprint(api.bp)

    # make url_for('index') == url_for('blog.index')
    # in another app, you might define a separate main index here with
    # app.route, while giving the blog blueprint a url_prefix, but for
    # the tutorial the blog will be the main index
    # app.add_url_rule("/", endpoint="index")

    return app
