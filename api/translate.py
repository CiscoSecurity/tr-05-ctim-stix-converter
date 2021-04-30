from flask import Blueprint, jsonify

from api import translator
from api.schemas import ArgumentsSchema
from api.utils import get_json, get_tr_client

translate_api = Blueprint('translate', __name__)


@translate_api.route('/translate', methods=['POST'])
def translate():
    arguments = get_json(schema=ArgumentsSchema())
    tr_client = get_tr_client()
    bundle = translator.translate(arguments, tr_client)
    return jsonify(bundle.json)
