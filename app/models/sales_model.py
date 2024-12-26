from datetime import datetime
from flask import jsonify
from app.utils.error_handler import ErrorHandler
from app.models.goods_model import Good
from app import db

class Sale(db.Model):
    __tablename__ = 'Sales'

    SaleId = db.Column(db.Integer, primary_key=True)
    GoodId = db.Column(db.Integer, db.ForeignKey('Goods.Id'))
    SaleDate = db.Column(db.DateTime)
    QuantitySold = db.Column(db.Integer)
    CheckNumber = db.Column(db.Integer, nullable=False)

    @classmethod
    def get_all_sales(cls):
        try:
            sales = cls.query.all()
            sales_list = [
                {
                    "SaleId": sale.SaleId,
                    "GoodId": sale.GoodId,
                    "SaleDate": sale.SaleDate.isoformat() if sale.SaleDate else None,
                    "QuantitySold": sale.QuantitySold,
                    "CheckNumber": sale.CheckNumber
                } for sale in sales
            ]
            return jsonify({"sales": sales_list}), 200

        except Exception as e:
            return ErrorHandler.handle_error(
                e,
                message="Database error while retrieving sales",
                status_code=500
            )

    @classmethod
    def get_sales_by_good(cls, good_id):
        try:
            good = Good.query.filter_by(Id=good_id).first()
            if not good:
                return jsonify({"message": f"No good found for Good ID {good_id}"}), 404

            sales = cls.query.filter_by(GoodId=good_id).all()
            if not sales:
                return jsonify({"message": f"No sales found for Good ID {good_id}"}), 404

            good_info = {
                "Id": good.Id,
                "Label": good.Label,
                "Manufacturer": good.Manufacturer,
                "Price": good.Price,
                "Quantity": good.Quantity,
                "InputDate": good.InputDate.isoformat() if good.InputDate else None,
                "DeptId": good.DeptId
            }

            sales_list = [
                {
                    "SaleId": sale.SaleId,
                    "QuantitySold": sale.QuantitySold,
                    "SaleDate": sale.SaleDate.isoformat() if sale.SaleDate else None,
                    "CheckNumber": sale.CheckNumber
                } for sale in sales
            ]

            return jsonify({"good": good_info, "sales": sales_list}), 200

        except Exception as e:
            return ErrorHandler.handle_error(
                e,
                message="Database error while retrieving sales for good",
                status_code=500
            )

    @classmethod
    def get_sales_summary_by_good(cls, good_id):
        try:
            good = Good.query.filter_by(Id=good_id).first()
            if not good:
                return jsonify({"message": f"No good found for Good ID {good_id}"}), 404

            sales = cls.query.filter_by(GoodId=good_id).all()
            if not sales:
                return jsonify({"message": f"No sales found for Good ID {good_id}"}), 404

            total_quantity_sold = 0
            total_revenue = 0.0

            for sale in sales:
                total_quantity_sold += sale.QuantitySold
                total_revenue += sale.QuantitySold * good.Price  # Multiply quantity sold by the price of the good

            sales_summary = {
                "GoodId": good.Id,
                "Label": good.Label,
                "TotalQuantitySold": total_quantity_sold,
                "TotalRevenue": total_revenue
            }

            return jsonify(sales_summary), 200

        except Exception as e:
            return ErrorHandler.handle_error(
                e,
                message="Database error while calculating sales summary for good",
                status_code=500
            )

    @classmethod
    def add_sale(cls, data):
        try:
            good_id = data.get('GoodId')
            sale_date = data.get('SaleDate')
            quantity_sold = data.get('QuantitySold')
            check_number = data.get('CheckNumber')

            good = Good.query.filter_by(Id=good_id).first()
            if not good:
                raise ValueError(f"Good with ID {good_id} does not exist.")

            if good.Quantity is None or good.Quantity < quantity_sold:
                raise ValueError(
                    f"Insufficient quantity for Good ID {good_id}. Available: {good.Quantity}, Requested: {quantity_sold}"
                )

            if not check_number:
                max_check = cls.query.with_entities(db.func.max(cls.CheckNumber)).scalar()
                if max_check is None:
                    check_number = 1
                else:
                    check_number = max_check + 1

            new_sale = cls(
                GoodId=good_id,
                SaleDate=sale_date,
                QuantitySold=quantity_sold,
                CheckNumber=check_number
            )
            db.session.add(new_sale)

            good.Quantity -= quantity_sold

            db.session.commit()

            return jsonify({"message": f"Sale added successfully. Left amount: {good.Quantity}"}), 201

        except ValueError as ve:
            return ErrorHandler.handle_validation_error(str(ve))
        except Exception as e:
            db.session.rollback()
            return ErrorHandler.handle_error(
                e,
                message="Database error while adding sale",
                status_code=500
            )

    @classmethod
    def delete_sale(cls, sale_id):
        try:
            sale = cls.query.get(sale_id)
            if not sale:
                raise ValueError("Sale not found.")

            db.session.delete(sale)
            db.session.commit()

            return jsonify({"message": "Sale deleted successfully."}), 200

        except ValueError as ve:
            return ErrorHandler.handle_validation_error(str(ve))
        except Exception as e:
            db.session.rollback()
            return ErrorHandler.handle_error(
                e,
                message="Database error while deleting sale",
                status_code=500
            )
