from PrivateClinic import app, db, admin
from PrivateClinic.models import Nguoi, NhanVien, Thuoc, HoaDon, TaiKhoan, UserRole
from flask import redirect
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose

class PatientView(ModelView):
    pass
class PeopleView(ModelView):
    pass
class MedicineView(ModelView):
    pass
class InvoiceView(ModelView):
    pass
class AccountView(ModelView):
    pass

admin.add_view(PatientView(Nguoi,db.session))
admin.add_view(PeopleView(NhanVien, db.session))
admin.add_view(MedicineView(Thuoc,db.session))
# admin.add_view(InvoiceView(Invoice,db.session))
# admin.add_view(AccountView(Account,db.session))