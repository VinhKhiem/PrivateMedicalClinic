from sqlalchemy import Column, Integer, Float, ForeignKey, String, Boolean, DATE, Text
from sqlalchemy.orm import relationship, backref
from PrivateClinic import db, app
from enum import Enum as UserEnum
from flask_login import UserMixin


class People(db.Model):
    __tablename__ = 'people'
    id = Column(String(10), primary_key=True)
    name = Column(String(50), nullable=False)
    dateOfBirth = Column(DATE, nullable=False)
    gender = Column(Boolean, nullable=False)
    address = Column(String(100), nullable=False)
    phoneNumber = Column(String(20), nullable=False)
    email = Column(String(100), nullable=False)
    # Các mối quan hệ
    account = relationship('Account', backref='people', lazy=True)
    doctor = relationship('Doctor', backref='people', uselist=False)
    nurse = relationship('Nurse', backref='people', uselist=False)
    patient = relationship('Patient', backref='people', uselist=False)
    employee = relationship('Employee', backref='people', uselist=False)
    administrator = relationship('Administrator', backref='people', uselist=False)


class UserRole(UserEnum):
    ADMIN = 1
    DOCTOR = 2
    NURSE = 3
    EMPLOYEE = 4
    PATIENT = 5


class Account(db.Model, UserMixin):
    __tablename__ = 'account'
    idAccount = Column(String(10), primary_key=True, unique=True)
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    isActive = Column(Boolean, nullable=True)
    #user_role = Column(Enum(UserRole), default=UserRole.PATIENT)
    # Các mối quan hệ
    id_people = Column(String(10), ForeignKey(People.id), nullable=False, unique=True)


class Patient(db.Model):
    __tablename__ = 'patient'
    idPatient = Column(String(10), ForeignKey(People.id), primary_key=True, unique=True)
    #
    exam_form = relationship('ExamForm', backref='patient', uselist=False)
    medical_history = relationship('MedicalHistory', back_populates='medical_history', uselist=False)
    exam_details = relationship('ExamDetails', backref='patient', lazy=True)


class Nurse(db.Model):
    __tablename__ = 'nurse'
    idNurse = Column(String(10), ForeignKey(People.id), primary_key=True, unique=True)
    degree = Column(String(150), nullable=False)


class Doctor(db.Model):
    __tablename__ = 'doctor'
    idDoctor = Column(String(10), ForeignKey(People.id), primary_key=True, unique=True)
    certificate = Column(String(150), nullable=False)
    expertise = Column(String(150), nullable=True)


class Employee(db.Model):
    __tablename__ = 'employee'
    idEmployee = Column(String(10), ForeignKey(People.id), primary_key=True, unique=True)
    degree = Column(String(150), nullable=False)


class Administrator(db.Model):
    __tablename__ = 'administrator'
    idAdmin = Column(String(10), ForeignKey(People.id), primary_key=True, unique=True)


class ExamList(db.Model):
    __tablename__ = 'exam_list'
    idList = Column(String(10), primary_key=True)
    examinationDate = Column(DATE, nullable=False)
    exam_details = relationship('ExamDetails', backref='exam_list', lazy=True)


class ExamDetails(db.Model):
    id = Column(String(10), primary_key=True)
    examList_id = Column(String(10), ForeignKey(ExamList.idList))
    patient_id = Column(String(10), ForeignKey(Patient.idPatient))


class MedicalHistory(db.Model):
    __tablename__ = 'medicalHistory'
    idMedicalHistory = Column(String(10), primary_key=True)
    creationDate = Column(DATE, nullable=False)
    updateDate = Column(DATE, nullable=False)
    #
    id_patient = Column(String(10), ForeignKey(Patient.idPatient))
    patient = relationship('Patient', back_populates='patient')


class MedicalExamination(db.Model):
    __tablename__ = 'medical_examination'
    idExamForm = Column(String(10), primary_key=True, unique=True)
    diagnosis = Column(String(250), nullable=False)
    appointment_date = Column(DATE, nullable=False)
    symptoms = Column(String(250), nullable=False)
    # Các mối quan hệ
    id_medicalHistory = Column(String(10), ForeignKey(MedicalHistory.idMedicalHistory))
    id_patient = Column(String(10), ForeignKey(Patient.idPatient))
    invoice = relationship('Invoice', backref='medical_examination', lazy=True)
    prescription = relationship('Prescription', backref="medical_examination", lazy=True)


class Invoice(db.Model):  # hóa đơn
    __tablename__ = 'invoice'
    idInvoice = Column(String(10), primary_key=True, unique=True)
    appointment_date = Column(DATE, nullable=False)
    examination_fee = Column(Float, nullable=False)
    medication_cost = Column(Float, nullable=False)

    id_exam_medicine = Column(String(10), ForeignKey(MedicalExamination.idExamForm))


class DrugUnit(db.Model):  # đơn vị thuốc
    __tablename__ = 'drug_unit'
    idUnit = Column(String(10), primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(String(300), nullable=False)
    medicine = relationship('Medicine', backref='drug_unit', lazy=True)


class Medicine(db.Model):  # thuốc
    __tablename__ = 'medicine'
    idMedicine = Column(String(10), primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(String(300), nullable=False)
    price = Column(Float, default=0)
    is_active = Column(Boolean, nullable=False)

    id_drugUnit = Column(String(10), ForeignKey(DrugUnit.idUnit))
    prescription = relationship('Prescription', backref='medicine', lazy=True)
    cate_medicine = relationship('Cate_Medicine', backref='medicine', lazy=True)


class Prescription(db.Model):
    __tablename__ = 'prescription'
    idPrescription = Column(String(10), primary_key=True)
    amount = Column(Integer, nullable=False)
    usage = Column(String(300), nullable=False)
    #
    id_ExamForm = Column(String(10), ForeignKey(MedicalExamination.idExamForm), nullable=False)
    id_medicine = Column(String(10), ForeignKey(Medicine.idMedicine), nullable=False)


class DrugCategory(db.Model):
    __tablename__ = 'drug_category'
    idCate = Column(String(10), primary_key=True)
    name = Column(String(50), nullable=False)
    cate_medicine = relationship('Cate_Medinice', backref='drug_category', lazy=True)


class Cate_Medicine(db.Model):
    __tablename__ = 'drugCate_medicine'
    id = Column(Integer, autoincrement=True, primary_key=True)
    drugCate_id = Column(String(10), ForeignKey(DrugCategory.idCate))
    medicine_id = Column(String(10), ForeignKey(Medicine.idMedicine))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
