import json
from copy import deepcopy

from flask import (
    Blueprint, render_template, request, session, redirect,
    url_for, flash
)
from threatresponse import ThreatResponse
from threatresponse.exceptions import RegionError

from api import translator
from api.exceptions import InvalidRegionError
from api.schemas import ArgumentsSchema
from api.utils import get_form_data
from forms import AuthorizeForm, ProcessForm

ui_api = Blueprint('ui', __name__)  # ToDo rename!!!!


def get_tr_client():
    try:
        return ThreatResponse(
            client_id=session.get('client_id'),
            client_password=session.get('client_password'),
            region=session.get('region'),
        )

    except RegionError as error:
        raise InvalidRegionError(error)


@ui_api.route('/', methods=['GET', 'POST'])
def process():
    form = ProcessForm()
    if request.method == 'POST' and form.validate_on_submit():
        tr_client = get_tr_client()

        if form.translate.data:
            data = get_form_data(schema=ArgumentsSchema(), data=form.data)
            bundle = translator.translate(deepcopy(data), tr_client)
            form.bundle.data = json.dumps(bundle.json, indent=4, sort_keys=True)

        elif form.submit.data:
            bundle = json.loads(request.form.get('bundle'))
            result = tr_client.private_intel.bundle.import_.post(bundle)
            flash(str(result))

    return render_template(
        'main.html',
        form=form,
        authorized=session.get('authorized')
    )


@ui_api.route('/ui/authorize', methods=['GET', 'POST'])
def authorize():
    form = AuthorizeForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            client_id = form.client_id.data
            client_password = form.client_password.data
            region = form.region.data

            session['client_id'] = client_id
            session['client_password'] = client_password
            session['region'] = region

            get_tr_client()

            session['authorized'] = True

            return redirect(url_for('.process'))

    return render_template('authorize.html', authorize_form=form)
