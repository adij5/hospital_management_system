from flask import Flask, render_template, request, redirect, url_for, flash
from config import Config
from models import db, User, Patient, Appointment
from datetime import datetime
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    @app.route('/')
    def index():
        patients = Patient.query.order_by(Patient.created_at.desc()).limit(10).all()
        appointments = Appointment.query.order_by(Appointment.scheduled_at.desc()).limit(10).all()
        return render_template('index.html', patients=patients, appointments=appointments)

    # Patients
    @app.route('/patients')
    def patients_list():
        patients = Patient.query.order_by(Patient.last_name).all()
        return render_template('patients.html', patients=patients)

    @app.route('/patients/add', methods=['GET', 'POST'])
    def add_patient():
        if request.method == 'POST':
            first = request.form.get('first_name')
            last = request.form.get('last_name')
            dob = request.form.get('dob') or None
            phone = request.form.get('phone')
            email = request.form.get('email')
            address = request.form.get('address')
            p = Patient(first_name=first, last_name=last, phone=phone, email=email, address=address)
            if dob:
                try:
                    p.dob = datetime.strptime(dob, '%Y-%m-%d').date()
                except:
                    pass
            db.session.add(p)
            db.session.commit()
            flash('Patient added.', 'success')
            return redirect(url_for('patients_list'))
        return render_template('add_patient.html')

    @app.route('/patients/<int:patient_id>/edit', methods=['GET', 'POST'])
    def edit_patient(patient_id):
        p = Patient.query.get_or_404(patient_id)
        if request.method == 'POST':
            p.first_name = request.form.get('first_name')
            p.last_name = request.form.get('last_name')
            dob = request.form.get('dob') or None
            if dob:
                try:
                    p.dob = datetime.strptime(dob, '%Y-%m-%d').date()
                except:
                    pass
            p.phone = request.form.get('phone')
            p.email = request.form.get('email')
            p.address = request.form.get('address')
            db.session.commit()
            flash('Patient updated.', 'success')
            return redirect(url_for('patients_list'))
        return render_template('edit_patient.html', patient=p)

    @app.route('/patients/<int:patient_id>/delete', methods=['POST'])
    def delete_patient(patient_id):
        p = Patient.query.get_or_404(patient_id)
        db.session.delete(p)
        db.session.commit()
        flash('Patient deleted.', 'info')
        return redirect(url_for('patients_list'))

    # Appointments
    @app.route('/appointments')
    def appointments_list():
        appts = Appointment.query.order_by(Appointment.scheduled_at.desc()).all()
        return render_template('appointments.html', appointments=appts)

    @app.route('/appointments/add', methods=['GET', 'POST'])
    def add_appointment():
        patients = Patient.query.order_by(Patient.last_name).all()
        if request.method == 'POST':
            patient_id = request.form.get('patient_id')
            doctor = request.form.get('doctor')
            scheduled = request.form.get('scheduled_at')
            reason = request.form.get('reason')
            try:
                scheduled_dt = datetime.strptime(scheduled, '%Y-%m-%dT%H:%M')
            except:
                flash('Invalid date/time format.', 'danger')
                return redirect(url_for('add_appointment'))
            ap = Appointment(patient_id=patient_id, doctor=doctor, scheduled_at=scheduled_dt, reason=reason)
            db.session.add(ap)
            db.session.commit()
            flash('Appointment scheduled.', 'success')
            return redirect(url_for('appointments_list'))
        return render_template('add_appointment.html', patients=patients)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
