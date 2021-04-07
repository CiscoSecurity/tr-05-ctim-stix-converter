from functools import partial

from flask import Blueprint, jsonify, request

from api import translator
from api.schemas import ArgumentsSchema
from api.utils import get_json, get_tr_client

translate_api = Blueprint('translate', __name__)

get_arguments = partial(get_json, schema=ArgumentsSchema())


@translate_api.route('/translate', methods=['POST'])
def translate():
    arguments = get_arguments()
    tr_client = get_tr_client(
        request.authorization.username,
        request.authorization.password,
        region=request.args.get('region')

    )
    bundle = translator.translate(arguments, tr_client)
    return jsonify(bundle.json)
