from flask import Blueprint, request
from app.models import Department

departments_bp = Blueprint('departments', __name__)

@departments_bp.route('/add_department', methods=['POST'])
def add_department():
    data = request.get_json()
    return Department.add_department(data)

@departments_bp.route('/get_all_departments', methods=['GET'])
def get_all_departments():
    return Department.get_all_departments()

@departments_bp.route('/delete_department/<int:dept_id>', methods=['DELETE'])
def delete_department(dept_id):
    return Department.delete_department(dept_id)
