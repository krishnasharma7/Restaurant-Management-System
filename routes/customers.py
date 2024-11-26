from flask import Blueprint, request, jsonify
from models import db, Reservation, Order, MenuItem

bp = Blueprint('customers', __name__)

# Create Reservation (POST method)
@bp.route('/reservations', methods=['POST'])
def create_reservation():
    data = request.json
    new_reservation = Reservation(
        user_id=data['user_id'],
        datetime=data['datetime']
    )
    db.session.add(new_reservation)
    db.session.commit()
    return jsonify({"message": "Reservation created successfully"}), 201

# Modify Reservation (PUT method)
@bp.route('/reservations/<int:reservation_id>', methods=['PUT'])
def modify_reservation(reservation_id):
    reservation = Reservation.query.get(reservation_id)
    if not reservation:
        return jsonify({"error": "Reservation not found"}), 404

    data = request.json
    
    # Update reservation datetime
    if 'datetime' in data:
        reservation.datetime = data['datetime']
    
    db.session.commit()
    return jsonify({"message": "Reservation modified successfully"}), 200

# Cancel Reservation (DELETE method)
@bp.route('/reservations/<int:reservation_id>', methods=['DELETE'])
def cancel_reservation(reservation_id):
    reservation = Reservation.query.get(reservation_id)
    if not reservation:
        return jsonify({"error": "Reservation not found"}), 404

    db.session.delete(reservation)
    db.session.commit()
    return jsonify({"message": "Reservation canceled successfully"}), 200

# View Reservations for a Customer (GET method)
@bp.route('/reservations/<int:user_id>', methods=['GET'])
def view_reservations(user_id):
    reservations = Reservation.query.filter_by(user_id=user_id).all()
    if not reservations:
        return jsonify({"message": "No reservations found"}), 404

    return jsonify([
        {"id": r.id, "user_id": r.user_id, "datetime": str(r.datetime), "status": r.status}
        for r in reservations
    ]), 200

# Place Order (POST method)
@bp.route('/order', methods=['POST'])
def create_order():
    data = request.json

    # Ensure the item exists
    menu_item = MenuItem.query.get(data['item_id'])
    if not menu_item:
        return jsonify({"error": "Menu item not found"}), 404

    new_order = Order(
        user_id=data['user_id'],
        item_id=data['item_id'],
        quantity=data['quantity']
    )
    db.session.add(new_order)
    db.session.commit()

    return jsonify({"message": "Order created successfully"}), 201
