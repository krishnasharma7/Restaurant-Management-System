import streamlit as st
import requests
from datetime import datetime

# Backend API URL
BASE_URL = "https://restaurant-management-system-r4vl.onrender.com"

# st.title("Restaurant Management System")

# Title for the navbar
st.markdown("""
    <style>
    .navbar {
        background-color: #0078D4;
        padding: 10px;
        color: white;
        text-align: center;
        font-size: 20px;
        font-weight: bold;
        border-radius: 5px;
    }
    </style>
    <div class="navbar">
        Restaurant Management System 
    </div>
""", unsafe_allow_html=True)

# Sidebar with title
st.sidebar.title("Features")

# Sidebar navigation
menu = st.sidebar.radio("Select Section", ["Reservations", "Order"])

# Customer Reservation Section
if menu == "Reservations":
    st.header("Reservations")

    # Create Reservation
   
    with st.form("create_reservation_form"):
        user_id = st.text_input("User ID (Customer ID)")
        reservation_datetime = st.date_input("Reservation Date (DD-MM-YYYY)")  # Date input widget
        create_reservation_submit = st.form_submit_button("Create Reservation")

        if create_reservation_submit:
            try:
                # Convert the date to a string in 'YYYY-MM-DD' format
                reservation_datetime_obj = reservation_datetime.strftime("%Y-%m-%d")
                
                reservation_data = {
                    "user_id": int(user_id),
                    "datetime": reservation_datetime_obj  # Pass the string
                }
                response = requests.post(f"{BASE_URL}/reservations", json=reservation_data)
                if response.status_code == 201:
                    # Parse the JSON response to get the reservation ID
                    response_json = response.json()
                    reservation_id = response_json.get("reservation_id")  # Get the reservation ID from the response
                    
                    # Display the success message and reservation ID
                    st.success(f"Reservation created successfully! Reservation ID: {reservation_id}")
                else:
                    st.error("Failed to create reservation")
            except ValueError:
                st.error("Invalid date format. Please use DD-MM-YYYY")




    # Modify Reservation
    st.header("Modify Reservation")
    with st.expander("Modify Reservation"):
        with st.form("modify_reservation_form"):
            reservation_id = st.text_input("Reservation ID to Modify")
            new_datetime = st.date_input("New Reservation Date (DD-MM-YYYY)")  # Date input widget
            new_status = st.selectbox("New Status", ["confirmed", "canceled", "pending"])
            modify_reservation_submit = st.form_submit_button("Modify Reservation")

            if modify_reservation_submit:
                try:
                    # Convert the date to a string in 'YYYY-MM-DD' format
                    new_datetime_obj = new_datetime.strftime("%Y-%m-%d")
                    
                    # Prepare the data to send
                    data = {
                        "datetime": new_datetime_obj,  # Pass the string
                        "status": new_status
                    }
                    
                    # Send the PUT request to modify the reservation
                    response = requests.put(f"{BASE_URL}/reservations/{reservation_id}", json=data)
                    
                    if response.status_code == 200:
                        st.success("Reservation modified successfully!")
                    else:
                        st.error("Failed to modify reservation")
                except ValueError:
                    st.error("Invalid date format. Please use DD-MM-YYYY")



    # Cancel Reservation
    st.header("Cancel Reservation")
    with st.expander("Cancel Reservation"):
        cancel_reservation_id = st.text_input("Reservation ID to Cancel")
        cancel_reservation_submit = st.button("Cancel Reservation")
        
        if cancel_reservation_submit:
            response = requests.delete(f"{BASE_URL}/reservations/{cancel_reservation_id}")
            if response.status_code == 200:
                st.success("Reservation canceled successfully!")
            else:
                st.error("Failed to cancel reservation")

elif menu == "Order":
    
    # View Menu (Only in Order Section)
    st.header("Menu")
    if st.button("View Menu"):
        response = requests.get(f"{BASE_URL}/menu")
        if response.status_code == 200:
            menu = response.json()
            if menu:
                for item in menu:
                    st.write(f"{item['id']}. **{item['name']}** - {item['price']}")
            else:
                st.error("Menu is empty.")
        else:
            st.error("Failed to fetch menu")
    
    # Order Section
    st.header("Place Order")
    with st.form("order_form"):
        user_id = st.text_input("User ID")
        item_id = st.text_input("Item ID")
        item_name = st.text_input("Item Name")
        quantity = st.number_input("Quantity", min_value=1)
        submit = st.form_submit_button("Place Order")

        if submit:
            order_data = {
                "user_id": int(user_id),
                "item_id": int(item_id),
                "item_name": str(item_name),
                "quantity": int(quantity)
            }
            response = requests.post(f"{BASE_URL}/order", json=order_data)
            if response.status_code == 201:
                st.success("Order placed successfully!")
            else:
                st.error("Failed to place order")

    st.header("View Order")
    if st.button("View Order"):
        response = requests.get(f"{BASE_URL}/order/view")
        if response.status_code == 200:
            order = response.json()
            if order:
                for item in order:
                    st.write(f"{item['user_id']}: {item['item_id']}. **{item['item_name']}** - {item['quantity']}")
            else:
                st.error("Order is empty.")
        else:
            st.error("Failed to fetch order")

    
