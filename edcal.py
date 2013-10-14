#!python3
"""REST interface to edcal."""
import json
import os

from flask import Flask, request

from edcal import edcal_instance as edcal


app = Flask(__name__)

@app.route('/')
def homepage():
    return 'Hello, world!'


@app.route('/identifiers')
def identifier_search():
    return json.dumps(edcal.identifier_search(request.args.get('q', '')))


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
