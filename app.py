from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from models import db, User, Reservation, MenuItem, Order, Payment, RestaurantDetail
from datetime import datetime

# Initialize the Flask app
app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///restaurant.db'  # SQLite URI for local database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking for performance

# Initialize the database with app
db.init_app(app)

# Extensions
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
CORS(app)  # Enable Cross-Origin Resource Sharing


# Create all tables (you can add this to make sure tables are created when the app starts)
with app.app_context():
    # db.drop_all()
    db.create_all()  # Creates tables for all the models
    db.session.query(Order).delete()  # Delete all rows from the Order table
    db.session.commit()  # Commit the changes

# Import routes (Blueprints)
from routes import customers, staff, admin
app.register_blueprint(customers.bp, url_prefix='/customers')
app.register_blueprint(staff.bp, url_prefix='/staff')
app.register_blueprint(admin.bp, url_prefix='/admin')

# General Routes for API (These can be handled by the Blueprints as well)
@app.route('/reservations', methods=['GET'])
def get_reservations():
    reservations = Reservation.query.all()
    return jsonify([{
        "id": r.id, "user_id": r.user_id, "datetime": str(r.datetime), "status": r.status
    } for r in reservations])

@app.route('/menu', methods=['GET'])
def get_menu():
    menu_items = MenuItem.query.all()
    return jsonify([{
        "id": m.id, "name": m.name, "price": m.price
    } for m in menu_items])

@app.route('/order', methods=['POST'])
def create_order():
    data = request.json
    new_order = Order(user_id=data['user_id'], item_id=data['item_id'],item_name=data['item_name'], quantity=data['quantity'])
    db.session.add(new_order)
    db.session.commit()
    return jsonify({"message": "Order created successfully"}), 201

@app.route('/order/view', methods=['GET'])
def view_order():
    order_items = Order.query.all()
    return jsonify([{
        "user_id": o.user_id, "item_id": o.item_id, "item_name": o.item_name, "quantity": o.quantity
    } for o in order_items])

@app.route('/reservations', methods=['POST'])
def create_reservation():
    data = request.json
    try:
        # Parse the datetime string into a datetime object
        reservation_datetime = datetime.strptime(data['datetime'], "%Y-%m-%d")  # Convert from string to datetime
        
        new_reservation = Reservation(
            user_id=data['user_id'],
            datetime=reservation_datetime,
            status='confirmed'
        )
        
        db.session.add(new_reservation)
        db.session.commit()
        
        # Return the ID of the created reservation along with the success message
        return jsonify({"message": "Reservation created successfully", "reservation_id": new_reservation.id}), 201
    except ValueError:
        return jsonify({"error": "Invalid date format, please use YYYY-MM-DD"}), 400


from datetime import datetime
from flask import request, jsonify

@app.route('/reservations/<int:id>', methods=['PUT'])
def modify_reservation(id):
    data = request.json
    reservation = Reservation.query.get(id)

    # If reservation is not found, return an error
    if not reservation:
        return jsonify({"message": "Reservation not found"}), 404

    # Check if 'datetime' is provided in the request
    if 'datetime' in data:
        try:
            # Convert datetime string from "YYYY-MM-DD" to a datetime object
            new_datetime = datetime.strptime(data['datetime'], "%Y-%m-%d")  # Use the same format as in create
            reservation.datetime = new_datetime
        except ValueError:
            return jsonify({"message": "Invalid datetime format. Please use YYYY-MM-DD"}), 400

    # Update the status if provided
    reservation.status = data.get('status', reservation.status)

    # Commit the changes to the database
    db.session.commit()

    # Return a success message
    return jsonify({"message": "Reservation updated successfully"})


@app.route('/reservations/<int:id>', methods=['DELETE'])
def cancel_reservation(id):
    reservation = Reservation.query.get(id)
    if not reservation:
        return jsonify({"message": "Reservation not found"}), 404
    db.session.delete(reservation)
    db.session.commit()
    return jsonify({"message": "Reservation canceled successfully"})

@app.route('/restaurant_details', methods=['GET', 'PUT'])
def manage_restaurant_details():
    restaurant = RestaurantDetail.query.first()
    if request.method == 'GET':
        if restaurant:
            return jsonify({
                "id": restaurant.id,
                "name": restaurant.name,
                "location": restaurant.location,
                "contact": restaurant.contact
            })
        else:
            return jsonify({"message": "Restaurant details not found"}), 404
    if request.method == 'PUT':
        data = request.json
        if restaurant:
            restaurant.name = data.get('name', restaurant.name)
            restaurant.location = data.get('location', restaurant.location)
            restaurant.contact = data.get('contact', restaurant.contact)
            db.session.commit()
            return jsonify({"message": "Restaurant details updated successfully"})
        else:
            return jsonify({"message": "Restaurant details not found"}), 404

@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    new_user = User(username=data['username'], password_hash=bcrypt.generate_password_hash(data['password']))
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created successfully"}), 201

@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.json
    user = User.query.get(id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    user.username = data.get('username', user.username)
    user.password_hash = bcrypt.generate_password_hash(data.get('password', user.password_hash))
    db.session.commit()
    return jsonify({"message": "User updated successfully"})

@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"})

if __name__ == "__main__":
    app.run(debug=True)
