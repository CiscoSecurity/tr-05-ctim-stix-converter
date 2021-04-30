import json

from flask import (
    Blueprint, render_template, request, session, redirect, url_for, flash
)
from markupsafe import Markup

from api import convertor
from api.schemas import ArgumentsSchema
from api.utils import get_tr_client, load
from forms import AuthorizeForm, MainForm

ui = Blueprint('ui', __name__)


@ui.route('/', methods=['GET', 'POST'])
def process():
    form = MainForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            tr_client = get_tr_client(session_=session)

            if form.convert.data:
                data = load(prepare_form(form), schema=ArgumentsSchema())
                bundle = convertor.convert(data, tr_client)
                form.bundle.data = json.dumps(
                    bundle.json, indent=4, sort_keys=True
                )

            elif form.submit.data:
                bundle = json.loads(request.form.get('bundle'))
                flash_submit_result(
                    tr_client.private_intel.bundle.import_.post(bundle)
                )

    return render_template(
        'main.html',
        form=form,
        authorized=session.get('authorized')
    )


@ui.route('/authorize', methods=['GET', 'POST'])
def authorize():
    form = AuthorizeForm()

    if request.method == 'POST':
        if form.validate_on_submit():

            session['client_id'] = form.client_id.data
            session['client_password'] = form.client_password.data
            session['region'] = form.region.data

            _ = get_tr_client(session_=session)
            session['authorized'] = True

            return redirect(url_for('.process'))

    return render_template('authorize.html', form=form)


def prepare_form(form):
    def remove_empty_fields(input_dict):
        return {k: v for k, v in input_dict.items() if v}

    data = {
        'indicator': remove_empty_fields(form.data.pop('indicator', {})),
        'sighting': remove_empty_fields(form.data.pop('sighting', {})),
        'exclude': form.data.get('exclude', '').split()
    }
    return {**form.data, **data}


def flash_submit_result(result):
    flash("Bundle is submitted to Private Intelligence:")
    for r in result['results']:
        flash(
            Markup(
                '<a href="{id_}">{type}</a> {result}'.format(
                    type=r['type'], id_=r['id'], result=r['result']
                )
            )
        )
