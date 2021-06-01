from api import converter
from api.utils import get_json
from flask import Blueprint

convert_api = Blueprint('convert', __name__)


@convert_api.route('/convert', methods=['POST'])
def convert():
    arguments = get_json()
    indicators_bulk = converter.convert(arguments)
    response = {'indicators': indicators_bulk}
    return response
