from flask import Blueprint, request, jsonify
from models import db, RestaurantDetail

bp = Blueprint('staff', __name__)

# Get Restaurant Details (GET method)
@bp.route('/restaurant', methods=['GET'])
def get_restaurant_details():
    details = RestaurantDetail.query.first()
    if not details:
        return jsonify({"error": "Restaurant details not found"}), 404
    return jsonify({
        "name": details.name,
        "address": details.address,
        "contact_info": details.contact_info
    }), 200

# Update Restaurant Details (PUT method)
@bp.route('/restaurant', methods=['PUT'])
def update_restaurant_details():
    data = request.json
    details = RestaurantDetail.query.first()
    
    if not details:
        # If no details exist, create new ones
        details = RestaurantDetail(
            name=data.get('name', 'Unknown'),
            address=data.get('address', 'Unknown'),
            contact_info=data.get('contact_info', 'Unknown')
        )
        db.session.add(details)
    else:
        # If details exist, update the fields
        details.name = data.get('name', details.name)
        details.address = data.get('address', details.address)
        details.contact_info = data.get('contact_info', details.contact_info)
    
    db.session.commit()
    return jsonify({"message": "Restaurant details updated successfully"}), 200
