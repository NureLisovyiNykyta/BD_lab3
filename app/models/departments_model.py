from flask import jsonify
from app.utils.error_handler import ErrorHandler
from app import db

class Department(db.Model):
    __tablename__ = 'Departments'

    DeptId = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(50), nullable=False)
    Producer = db.Column(db.String(50), nullable=False)

    @classmethod
    def get_all_departments(cls):
        try:
            departments = cls.query.all()
            departments_list = [
                {
                    "DeptId": department.DeptId,
                    "Name": department.Name,
                    "Producer": department.Producer
                } for department in departments
            ]
            return jsonify({"departments": departments_list}), 200

        except Exception as e:
            return ErrorHandler.handle_error(
                e,
                message="Database error while retrieving departments",
                status_code=500
            )

    @classmethod
    def add_department(cls, data):
        try:
            name = data.get('Name')
            producer = data.get('Producer')

            if not name or not producer:
                raise ValueError("Name and Producer are required.")

            new_department = cls(Name=name, Producer=producer)
            db.session.add(new_department)
            db.session.commit()

            return jsonify({"message": "Department added successfully."}), 201

        except ValueError as ve:
            return ErrorHandler.handle_validation_error(str(ve))
        except Exception as e:
            db.session.rollback()
            return ErrorHandler.handle_error(
                e,
                message="Database error while adding department",
                status_code=500
            )

    @classmethod
    def delete_department(cls, dept_id):
        try:
            department = cls.query.get(dept_id)
            if not department:
                raise ValueError("Department not found.")

            db.session.delete(department)
            db.session.commit()

            return jsonify({"message": "Department deleted successfully."}), 200

        except ValueError as ve:
            return ErrorHandler.handle_validation_error(str(ve))
        except Exception as e:
            db.session.rollback()
            return ErrorHandler.handle_error(
                e,
                message="Database error while deleting department",
                status_code=500
            )