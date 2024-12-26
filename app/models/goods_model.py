from flask import jsonify
from app.utils.error_handler import ErrorHandler
from app.models.departments_model import Department
from app import db

class Good(db.Model):
    __tablename__ = 'Goods'

    Id = db.Column(db.Integer, primary_key=True)
    Label = db.Column(db.String(100))
    Manufacturer = db.Column(db.String(50))
    Price = db.Column(db.Float)
    Quantity = db.Column(db.Integer)
    InputDate = db.Column(db.DateTime)
    DeptId = db.Column(db.Integer, db.ForeignKey('Departments.DeptId'))

    @classmethod
    def get_all_goods(cls):
        try:
            goods = cls.query.all()
            goods_list = [
                {
                    "Id": good.Id,
                    "Label": good.Label,
                    "Manufacturer": good.Manufacturer,
                    "Price": good.Price,
                    "Quantity": good.Quantity,
                    "InputDate": good.InputDate.isoformat() if good.InputDate else None,
                    "DeptId": good.DeptId
                } for good in goods
            ]
            return jsonify({"goods": goods_list}), 200

        except Exception as e:
            return ErrorHandler.handle_error(
                e,
                message="Database error while retrieving goods",
                status_code=500
            )

    @classmethod
    def add_good(cls, data):
        try:
            label = data.get('Label')
            manufacturer = data.get('Manufacturer')
            price = data.get('Price')
            quantity = data.get('Quantity')
            input_date = data.get('InputDate')
            dept_id = data.get('DeptId')

            department = db.session.query(Department).filter_by(DeptId=dept_id).first()
            if not department:
                raise ValueError(f"Department with ID {dept_id} does not exist.")

            new_good = cls(
                Label=label,
                Manufacturer=manufacturer,
                Price=price,
                Quantity=quantity,
                InputDate=input_date,
                DeptId=dept_id
            )
            db.session.add(new_good)
            db.session.commit()

            return jsonify({"message": "Good added successfully."}), 201

        except ValueError as ve:
            return ErrorHandler.handle_validation_error(str(ve))
        except Exception as e:
            db.session.rollback()
            return ErrorHandler.handle_error(
                e,
                message="Database error while adding good",
                status_code=500
            )

    @classmethod
    def get_goods_by_department(cls, dept_id):
        try:
            department = Department.query.filter_by(DeptId=dept_id).first()
            if not department:
                return jsonify({"message": f"No department found for Department ID {dept_id}"}), 404

            goods = cls.query.filter_by(DeptId=dept_id).all()
            if not goods:
                return jsonify({"message": f"No goods found for Department ID {dept_id}"}), 404

            department_info = {
                "DeptId": department.DeptId,
                "Name": department.Name,
                "Producer": department.Producer
            }

            goods_list = [
                {
                    "Id": good.Id,
                    "Label": good.Label,
                    "Manufacturer": good.Manufacturer,
                    "Price": good.Price,
                    "Quantity": good.Quantity,
                    "InputDate": good.InputDate.isoformat() if good.InputDate else None,
                    "DeptId": good.DeptId
                } for good in goods
            ]

            return jsonify({"department": department_info, "goods": goods_list}), 200

        except Exception as e:
            return ErrorHandler.handle_error(
                e,
                message="Database error while retrieving goods by department",
                status_code=500
            )

    @classmethod
    def delete_good(cls, good_id):
        try:
            good = cls.query.get(good_id)
            if not good:
                raise ValueError("Good not found.")

            db.session.delete(good)
            db.session.commit()

            return jsonify({"message": "Good deleted successfully."}), 200

        except ValueError as ve:
            return ErrorHandler.handle_validation_error(str(ve))
        except Exception as e:
            db.session.rollback()
            return ErrorHandler.handle_error(
                e,
                message="Database error while deleting good",
                status_code=500
            )
