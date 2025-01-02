from datetime import datetime
from flask import Blueprint, request
from app.models import Sale

sales_bp = Blueprint('sales', __name__)


@sales_bp.route('/add_sale', methods=['POST'])
def add_sale():
    data = request.get_json()
    return Sale.add_sale(data)


@sales_bp.route('/get_all_sales', methods=['GET'])
def get_all_sales():
    return Sale.get_all_sales()


@sales_bp.route('/delete_sale/<int:sale_id>', methods=['DELETE'])
def delete_sale(sale_id):
    return Sale.delete_sale(sale_id)


@sales_bp.route('/sales_by_good/<int:good_id>', methods=['GET'])
def sales_by_good(good_id):
    return Sale.get_sales_by_good(good_id)


@sales_bp.route('/sales_summary_by_good/<int:good_id>', methods=['GET'])
def sales_summary_by_good(good_id):
    return Sale.get_sales_summary_by_good(good_id)


@sales_bp.route('/add_sale_procedure', methods=['POST'])
def add_sale_procedure():
    data = request.get_json()
    return Sale.add_sale_procedure(data)


@sales_bp.route('/get_most_expensive_good', methods=['GET'])
def most_expensive_good():
    data = request.get_json()
    return Sale.get_most_expensive_good_on_date(data)

