import streamlit as st
import requests

# Backend API URL
BASE_URL = "http://127.0.0.1:5000"

st.title("Restaurant Management System")

# Customer Reservation Section
st.header("Reservations")

# Create Reservation
with st.expander("Create Reservation"):
    with st.form("create_reservation_form"):
        user_id = st.text_input("User ID (Customer ID)")
        reservation_datetime = st.text_input("Reservation Date(YYYY-MM-DD)")
        create_reservation_submit = st.form_submit_button("Create Reservation")
        
        if create_reservation_submit:
            if not user_id or not reservation_datetime:
                st.error("Please fill out both fields.")
            else:
                try:
                    reservation_data = {
                        "user_id": int(user_id),
                        "datetime": reservation_datetime
                    }
                    response = requests.post(f"{BASE_URL}/reservations", json=reservation_data)
                    if response.status_code == 201:
                        st.success("Reservation created successfully!")
                    else:
                        st.error("Failed to create reservation")
                except ValueError:
                    st.error("Invalid User ID or Date format. Please try again.")

# Modify Reservation
with st.expander("Modify Reservation"):
    reservation_id = st.text_input("Reservation ID to Modify")
    new_datetime = st.text_input("New Date & Time (YYYY-MM-DD HH:MM:SS)")
    new_status = st.selectbox("New Status", ["confirmed", "canceled", "pending"])
    modify_reservation_submit = st.button("Modify Reservation")
    
    if modify_reservation_submit:
        if not reservation_id or not new_datetime:
            st.error("Please fill out both fields.")
        else:
            data = {"datetime": new_datetime, "status": new_status}
            response = requests.put(f"{BASE_URL}/reservations/{reservation_id}", json=data)
            if response.status_code == 200:
                st.success("Reservation modified successfully!")
            else:
                st.error("Failed to modify reservation")

# Cancel Reservation
with st.expander("Cancel Reservation"):
    cancel_reservation_id = st.text_input("Reservation ID to Cancel")
    cancel_reservation_submit = st.button("Cancel Reservation")
    
    if cancel_reservation_submit:
        if not cancel_reservation_id:
            st.error("Please provide a Reservation ID.")
        else:
            response = requests.delete(f"{BASE_URL}/reservations/{cancel_reservation_id}")
            if response.status_code == 200:
                st.success("Reservation canceled successfully!")
            else:
                st.error("Failed to cancel reservation")

# Menu Section
st.header("Menu")
if st.button("View Menu"):
    response = requests.get(f"{BASE_URL}/menu")
    if response.status_code == 200:
        menu = response.json()
        if menu:
            st.write(menu)
        else:
            st.write("No menu items available.")
    else:
        st.error("Failed to fetch menu")

# Order Section
st.header("Place Order")
with st.form("order_form"):
    user_id = st.text_input("User ID")
    item_id = st.text_input("Item ID")
    quantity = st.number_input("Quantity", min_value=1)
    submit = st.form_submit_button("Place Order")

    if submit:
        if not user_id or not item_id:
            st.error("Please provide both User ID and Item ID.")
        else:
            try:
                order_data = {
                    "user_id": int(user_id),
                    "item_id": int(item_id),
                    "quantity": int(quantity)
                }
                response = requests.post(f"{BASE_URL}/order", json=order_data)
                if response.status_code == 201:
                    st.success("Order placed successfully!")
                else:
                    st.error("Failed to place order")
            except ValueError:
                st.error("Invalid input. Please check User ID, Item ID, and Quantity.")

# Staff Section - Manage Restaurant Details
st.header("Staff Panel - Manage Restaurant Details")
with st.expander("View Restaurant Details"):
    response = requests.get(f"{BASE_URL}/restaurant_details")
    if response.status_code == 200:
        details = response.json()
        st.write(f"Restaurant Name: {details['name']}")
        st.write(f"Location: {details['location']}")
        st.write(f"Contact: {details['contact']}")
    else:
        st.error("Failed to fetch restaurant details")

with st.expander("Edit Restaurant Details"):
    name = st.text_input("Restaurant Name", value=details['name'])
    location = st.text_input("Restaurant Location", value=details['location'])
    contact = st.text_input("Contact Number", value=details['contact'])
    
    if st.button("Save Changes"):
        if not name or not location or not contact:
            st.error("Please provide all restaurant details.")
        else:
            data = {
                "name": name,
                "location": location,
                "contact": contact
            }
            response = requests.put(f"{BASE_URL}/restaurant_details", json=data)
            if response.status_code == 200:
                st.success("Restaurant details updated successfully!")
            else:
                st.error("Failed to update restaurant details")

# Admin Section - Manage Users
st.header("Admin Panel - Manage Users")

# Create User
with st.expander("Create User"):
    username = st.text_input("New Username")
    password = st.text_input("New Password", type="password")
    create_user_button = st.button("Create User")

    if create_user_button:
        if not username or not password:
            st.error("Please provide both username and password.")
        else:
            data = {
                "username": username,
                "password": password
            }
            response = requests.post(f"{BASE_URL}/users", json=data)
            if response.status_code == 201:
                st.success("User created successfully!")
            else:
                st.error("Failed to create user")

# Update User
with st.expander("Update User"):
    user_id_to_update = st.text_input("User ID to Update")
    new_username = st.text_input("New Username")
    new_password = st.text_input("New Password", type="password")
    
    if st.button("Update User"):
        if not user_id_to_update or not new_username or not new_password:
            st.error("Please provide User ID, New Username, and New Password.")
        else:
            data = {
                "username": new_username,
                "password": new_password
            }
            response = requests.put(f"{BASE_URL}/users/{user_id_to_update}", json=data)
            if response.status_code == 200:
                st.success("User updated successfully!")
            else:
                st.error("Failed to update user")

# Delete User
with st.expander("Delete User"):
    user_id_to_delete = st.text_input("User ID to Delete")
    delete_user_button = st.button("Delete User")

    if delete_user_button:
        if not user_id_to_delete:
            st.error("Please provide a User ID.")
        else:
            response = requests.delete(f"{BASE_URL}/users/{user_id_to_delete}")
            if response.status_code == 200:
                st.success("User deleted successfully!")
            else:
                st.error("Failed to delete user")
