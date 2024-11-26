import unittest
from app import app, db, Reservation
from datetime import datetime

class ReservationTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # In-memory SQLite database
        self.app = app.test_client()
        self.ctx = app.app_context()
        self.ctx.push()
        # db.create_all()  # Create all tables before each test

    def tearDown(self):
        db.session.remove()
        # db.drop_all()  # Drop all tables after each test
        self.ctx.pop()  # Pop the context after each test

    def test_create_reservation(self):
        reservation_data = {
            "user_id": 1,
            "datetime": "2024-11-26"
        }
        response = self.app.post('/reservations', json=reservation_data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('reservation_id', response.json)

    def test_modify_reservation(self):
        reservation_data = {
            "user_id": 1,
            "datetime": "2024-11-26"
        }
        response = self.app.post('/reservations', json=reservation_data)
        reservation_id = response.json['reservation_id']

        new_data = {
            "datetime": "2024-12-01",
            "status": "confirmed"
        }
        response = self.app.put(f'/reservations/{reservation_id}', json=new_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'Reservation updated successfully')

    def test_create_reservation_invalid_date(self):
        reservation_data = {
            "user_id": 1,
            "datetime": "2024-11-31"  # Invalid date
        }
        response = self.app.post('/reservations', json=reservation_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json)

    def test_modify_reservation_invalid_date(self):
        reservation_data = {
            "user_id": 1,
            "datetime": "2024-11-26"
        }
        response = self.app.post('/reservations', json=reservation_data)
        reservation_id = response.json['reservation_id']

        new_data = {
            "datetime": "2024-02-30",  # Invalid date
            "status": "pending"
        }
        response = self.app.put(f'/reservations/{reservation_id}', json=new_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid datetime format', response.json['message'])

    def test_modify_reservation_not_found(self):
        new_data = {
            "datetime": "2024-12-01",
            "status": "confirmed"
        }
        response = self.app.put('/reservations/999', json=new_data)  # Non-existing reservation ID
        self.assertEqual(response.status_code, 404)
        self.assertIn('Reservation not found', response.json['message'])

if __name__ == '__main__':
    unittest.main()
