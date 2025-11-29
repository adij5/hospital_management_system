from app import create_app
from models import db, User, Patient, Appointment
from datetime import datetime, timedelta
import os

app = create_app()
with app.app_context():
    print('Creating database tables...')
    db.create_all()

    # Seed sample data if tables empty
    if User.query.count() == 0:
        u = User(username='admin', full_name='Admin User', password_hash='admin')  # replace with hashed pw in prod
        db.session.add(u)
    if Patient.query.count() == 0:
        p1 = Patient(first_name='John', last_name='Doe', phone='1234567890', email='john@example.com')
        p2 = Patient(first_name='Jane', last_name='Smith', phone='0987654321', email='jane@example.com')
        db.session.add_all([p1, p2])
        db.session.commit()
        a1 = Appointment(patient_id=p1.id, doctor='Dr. A', scheduled_at=datetime.utcnow() + timedelta(days=1), reason='Checkup')
        a2 = Appointment(patient_id=p2.id, doctor='Dr. B', scheduled_at=datetime.utcnow() + timedelta(days=2), reason='Follow-up')
        db.session.add_all([a1, a2])
    db.session.commit()
    print('Database initialized and sample data added.')
