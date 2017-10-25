import flask

from . import app


@app.route('/<urlId>', methods=['GET'])
def redirect(urlId):
    """ Redirect to the full, target URL for the given `urlId`.

    Args:
        urlId (str): String ID of a valid shortened URL

    Returns:
        flask.Response: On success, a reponse with status code `301` and a
            `Location` header corresponding to the target URL. Otherwise, a
            response with status code `404` and a plain text error message.
    """
    flask.abort(501, 'Not Implemented!')


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
    flask.abort(501, 'Not Implemented!')


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
    flask.abort(501, 'Not Implemented!')


@app.route('/create', methods=['POST'])
def create():
    """ Generate a new, unique shortened URL.

    Returns:
        flask.Response: On success, a reponse with status code `200` and a JSON
            object with valid `urlId`, `shortUrl`, and `authToken` values.
            Otherwise, a response with status code `400` and a plain text error
            message.
    """
    flask.abort(501, 'Not Implemented!')
