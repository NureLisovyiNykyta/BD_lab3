from flask import Blueprint, request
from app.models import Good

goods_bp = Blueprint('goods', __name__)


@goods_bp.route('/add_good', methods=['POST'])
def add_good():
    data = request.get_json()
    return Good.add_good(data)


@goods_bp.route('/get_all_goods', methods=['GET'])
def get_all_goods():
    return Good.get_all_goods()


@goods_bp.route('/delete_good/<int:good_id>', methods=['DELETE'])
def delete_good(good_id):
    return Good.delete_good(good_id)


@goods_bp.route('/goods_by_department/<int:dept_id>', methods=['GET'])
def get_goods_by_department(dept_id):
    return Good.get_goods_by_department(dept_id)