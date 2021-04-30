from flask import Blueprint, jsonify

from api import convertor
from api.schemas import ArgumentsSchema
from api.utils import get_json, get_tr_client

convert_api = Blueprint('convert', __name__)


@convert_api.route('/convert', methods=['POST'])
def convert():
    arguments = get_json(schema=ArgumentsSchema())
    tr_client = get_tr_client()
    bundle = convertor.convert(arguments, tr_client)
    return jsonify(bundle.json)
