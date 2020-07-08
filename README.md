# flask-hello-world

Ported from [flaskr](https://github.com/pallets/flask/tree/master/examples/tutorial) so that I can experiment with stuff.

Make db:

```bash
$ createdb blog
```

Install it:

```bash
$ python -m pip install -e .
$ flask init-db
```

Run it:

```bash
FLASK_APP=blog FLASK_DEBUG=1 flask run
```

Request it:

```bash
$ curl \
    --header "Content-Type: application/json" \
    --request POST \
    --data '{"title": "foo", "body": "foobar"}' \
    localhost:5000/api/create
```
