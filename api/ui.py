import json
from collections import namedtuple
from copy import deepcopy

from flask import Blueprint, render_template, request, session, redirect, \
    url_for, flash
from threatresponse import ThreatResponse
from threatresponse.exceptions import RegionError

from api import translator
from api.exceptions import InvalidRegionError
from api.schemas import ArgumentsSchema
from api.utils import get_form_data
from forms import TranslateForm, SubmitForm, AuthorizeForm

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


@ui_api.route('/', methods=['GET'])
def main():
    Context = namedtuple('Context',
                         'client_password client_id region content bundle')
    context = Context(
        client_password=session.get('client_password'),
        client_id=session.get('client_id'),
        region=session.get('region'),
        content=session.get('content'),
        bundle=session.get('bundle'),
    )
    return render_template(
        'main.html',
        authorize_form=AuthorizeForm(obj=context),
        translate_form=TranslateForm(obj=context),
        submit_form=SubmitForm(obj=context),
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

            return redirect(url_for('.main'))

    return render_template('authorize.html', authorize_form=form)


@ui_api.route('/ui/translate', methods=['POST'])
def translate():
    form = TranslateForm()
    if form.validate_on_submit():
        tr_client = get_tr_client()

        data = get_form_data(schema=ArgumentsSchema(), data=form.data)
        bundle = translator.translate(deepcopy(data), tr_client)

        session['bundle'] = json.dumps(bundle.json, indent=4, sort_keys=True)
        session['content'] = data['content']

    return redirect(url_for('.main'))


@ui_api.route('/ui/submit', methods=['POST'])
def submit():
    form = SubmitForm()
    if form.validate_on_submit():
        tr_client = get_tr_client()
        bundle = json.loads(request.form.get('bundle'))
        result = tr_client.private_intel.bundle.import_.post(bundle)
        flash(str(result))

    return redirect(url_for('.main'))
