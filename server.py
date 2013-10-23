#!python3
"""Web API/interface."""
import json
import os

from flask import Flask, render_template, request
from wtforms import Form, TextField, validators, FieldList

from edcal import EdCal


app = Flask(__name__)
edcal = None

class CourseCodeForm(Form):
    """Takes and validates a bunch of UoE course codes."""
    course_codes = FieldList(
        TextField(label='course-code',
                  validators=[validators.Regexp('[\w]{4}[\d]{5}')]),
        min_entries=3)


@app.route('/')
def homepage():
    form = CourseCodeForm(request.form)
    return render_template('course-code-form.html', form=form)


@app.route('/identifiers')
def identifier_search():
    """List of identifiers for courses matching query regex.

    Get identifiers for all Informatics courses:
        GET /identifiers?q=INFR.*
    """
    return json.dumps(edcal.identifier_search(request.args.get('q', '')))


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    edcal = EdCal()
    app.run(host='0.0.0.0', port=port, debug=True)

