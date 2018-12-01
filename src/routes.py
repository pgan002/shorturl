import random
import string

from flask import abort, jsonify, redirect, request, Response

from . import app
from .db.sqlite import SqliteDB


AUTH_TOKEN_LEN = app.config.get('AUTH_TOKEN_LEN')
MAX_ID_LEN = app.config.get('MAX_ID_LEN')
ID_ALPHABET = string.ascii_letters + string.digits


def _create_id():
    """Create a new ID (short URL) at random (as per specification).
    Repeatedly try short strings and increase the length if there are collisions
    with existing IDs. This function can take a long time when most short
    IDs are already allocated.

    Return:
        New unique URL ID
    """
    db = SqliteDB()
    for length in range(1, MAX_ID_LEN):
        for _ in range(len(ID_ALPHABET) ** length):
            id_ = ''.join(random.choice(ID_ALPHABET) for _ in range(length))
            url, _ = db.get_url_and_token(id_)
            if not url:
                return id_


def _authorize(id_):
    """Verify that the given URL ID is in the database and matches the
    authorization token given in the HTTP request header.

    Returns:
        A flask.Response with HTTP status code 404 (Not found) if the ID is not
        in the database

        A flask.Response with HTTP status code 400 (Bad request) if no
        authorization header was provided

        A flask.Response with HTTP status code 403 (Forbidden) if the
        authorization token does not match the token corresponding to the ID

        None otherwise

    Args:
        id_ (str): URL ID to check
    """
    db = SqliteDB()
    url, token = db.get_url_and_token(id_)
    if not url:
        abort(404, 'No such ID')

    supplied_token = request.headers.get('Authorization')
    if not supplied_token:
        abort(400, 'Required authorization header')

    if supplied_token != token:
        abort(403, 'Incorrect authorization token')


def _validate_new_id(id_):
    """Check that the given URL ID has appropriate length and character set
    and does not already exist in the database.

    Returns:
        A flask.Response with HTTP status 400 (Bad requrest) if the ID is too
        long or includes forbidden characters


        Aflask.Response with HTTP status code 409 (Conflict) if the ID already
        exists

        None otherwise
    respond with the appropriate HTTP response code.
    """
    db = SqliteDB()
    if not 1 <= len(id_) <= MAX_ID_LEN:
        abort(400, 'ID must be 1 to %s characters long' % MAX_ID_LEN)

    if any(c not in ID_ALPHABET for c in id_):
        abort(400, 'ID can contain only characters from %s' % ID_ALPHABET)

    url, _ = db.get_url_and_token(id_)
    if url:
        abort(409, 'ID already exists')


@app.route('/<urlId>', methods=['GET'])
def redirect_(urlId):
    """ Redirect to the full, target URL for the given `urlId`.

    Args:
        urlId (str): String ID of a valid shortened URL

    Returns:
        flask.Response: On success, a reponse with status code `301` and a
            `Location` header corresponding to the target URL. Otherwise, a
            response with status code `404` and a plain text error message.
    """
    db = SqliteDB()
    url, _ = db.get_url_and_token(urlId)
    if not url:
        abort(404, 'No such ID')

    db.update_stats(urlId, request.remote_addr)
    return redirect(url, code=301)


@app.route('/<urlId>/stats', methods=['GET'])
def stats(urlId):
    """ Return per-client stats about successful redirects for a given `urlId`.

    Args:
        urlId (str): String ID of a valid shortened URL

    Returns:
        flask.Response: On success, a reponse with status code `200` and a JSON
            object with numeric counts of successful redirects, per unique
            client IP address. Otherwise, a response with status code `403` or
            `404` and a plain text error message.
    """
    _authorize(urlId)
    return jsonify(SqliteDB().get_stats(urlId))


@app.route('/<urlId>', methods=['DELETE'])
def delete(urlId):
    """ Delete an existing shortened URL.

    Args:
        urlId (str): String ID of a valid shortened URL

    Returns:
        flask.Response: On success, an empty reponse with status code `204`.
            Otherwise, a response with status code `403` or `404` and a plain
            text error message.
    """
    _authorize(urlId)
    SqliteDB().delete_url(urlId)
    return Response(status=204)


@app.route('/create', methods=['POST'])
def create():
    """ Generate a new, unique shortened URL.

    Returns:
        flask.Response: On success, a reponse with status code `200` and a JSON
            object with valid `urlId`, `shortUrl`, and `authToken` values.
            Otherwise, a response with status code `400` and a plain text error
            message.
    """
    id_ = request.json.get('id')
    if id_ is not None:
        _validate_new_id(id_)
    else:
        id_ = _create_id()

    url = request.json.get('url')
    if not url:
        abort('400', 'Required body key "url"')

    token = ''.join(random.choice(string.printable)
                    for _ in range(AUTH_TOKEN_LEN))

    SqliteDB().add_url(id_, url, token)
    return Response()
