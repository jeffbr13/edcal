#!python3
"""Web API/interface."""
import json
import os

from flask import Flask, render_template, request
from wtforms import Form, TextField, validators, FieldList

from edcal import EdCal
from edcal.ted.courses import CourseEncoder


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
    """JSON list of course identifiers for regex matches."""
    try:
        return ('{"identifiers": ' +
            json.dumps(edcal.identifier_filter(request.args.get('q', '')), cls=CourseEncoder)
            + '}')
    except KeyError:
        return ''


@app.route('/courses')
def course_search():
    """JSON list of course objects."""
    return ('{"courses": ' +
        json.dumps(edcal.course_filter(request.args.get('q', '')), cls=CourseEncoder)
        + '}')


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    edcal = EdCal()
    app.run(host='0.0.0.0', port=port, debug=True)

