from flask import Blueprint, jsonify

from api.utils import get_json, get_tr_client

submit_api = Blueprint('submit', __name__)


@submit_api.route('/submit', methods=['POST'])
def submit():
    bulk = get_json()
    tr_client = get_tr_client()
    result = tr_client.private_intel.bulk.post(bulk)
    return jsonify(result)
