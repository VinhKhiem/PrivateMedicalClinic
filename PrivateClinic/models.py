from sqlalchemy import Column, Integer, Float, ForeignKey, String, Boolean, DATE, Text, Enum
from sqlalchemy.orm import relationship, backref
from datetime import datetime, date
from PrivateClinic import db, app
from enum import Enum as UserEnum
from flask_login import UserMixin


class UserRole(UserEnum):
    ADMIN = 1
    DOCTOR = 2
    NURSE = 3
    EMPLOYEE = 4
    PATIENT = 5


class Nguoi(db.Model):
    __tablename__ = 'nguoi'
    id = Column(String(10), primary_key=True)
    hoTen = Column(String(50), nullable=False)
    ngaySinh = Column(DATE, nullable=False)
    gioiTinh = Column(Boolean, nullable=False)
    diaChi = Column(String(100), nullable=False)
    soDienThoai = Column(String(20), nullable=False)
    email = Column(String(100), nullable=False)
    # Các mối quan hệ
    taiKhoan = relationship('TaiKhoan', backref='Nguoi', lazy=True)
    bacsi = relationship('BacSi', backref='Nguoi', uselist=False)
    yta = relationship('YTa', backref='Nguoi', uselist=False)
    benhnhan = relationship('BenhNhan', backref='Nguoi', uselist=False)
    nhanvien = relationship('NhanVien', backref='Nguoi', uselist=False)
    quantri = relationship('QuanTriVien', backref='Nguoi', uselist=False)


class TaiKhoan(db.Model, UserMixin):
    __tablename__ = 'tai_khoan'
    id = Column(String(10), primary_key=True, unique=True)
    ten = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    trangThai = Column(Boolean, nullable=True)
    user_role = Column(Enum(UserRole), default=UserRole.PATIENT)
    # Các mối quan hệ
    id_nguoidung = Column(String(10), ForeignKey(Nguoi.id), nullable=False, unique=True)


class DanhSachKham(db.Model):
    __tablename__ = 'danh_sach_kham'
    id = Column(String(10), primary_key=True)
    ngayKham = Column(DATE, nullable=False)
    chi_tiet_ds = relationship('ChiTietDanhSach', backref='danh_sach_kham', lazy=True)
    ds_dk = relationship('DanhSachDangKy', backref='danh_sach_kham', lazy=True)


class DanhSachDangKy(db.Model):
    __tablename__ = 'danh_sach_dang_ky'
    id = Column(String(10), primary_key=True)
    ngayDK = Column(DATE, default=datetime.now())
    trangThai = Column(Boolean, default=True)
    ds_kham_id = Column(String(10), ForeignKey(DanhSachKham.id))
    benh_nhan = relationship('BenhNhan', backref='danh_sach_dang_ky', lazy=True)


class BenhNhan(db.Model):
    __tablename__ = 'benh_nhan'
    id = Column(String(10), ForeignKey(Nguoi.id), primary_key=True, unique=True)
    #
    ds_dk_id = Column(String(10), ForeignKey(DanhSachDangKy.id))
    phieu_kham = relationship('PhieuKham', backref='benh_nhan', uselist=False)
    lich_su_kham = relationship('LichSuKham', back_populates='benh_nhan', uselist=False)
    ct_ds_kham = relationship('ChiTietDanhSach', backref='benh_nhan', lazy=True)


class YTa(db.Model):
    __tablename__ = 'y_ta'
    id = Column(String(10), ForeignKey(Nguoi.id), primary_key=True)
    bangCap = Column(String(150), nullable=False)


class BacSi(db.Model):
    __tablename__ = 'bac_si'
    id = Column(String(10), ForeignKey(Nguoi.id), primary_key=True)
    chungChi = Column(String(150), nullable=False)
    chuyenKhoa = Column(String(150), nullable=True)


class NhanVien(db.Model):
    __tablename__ = 'nhan_vien'
    id = Column(String(10), ForeignKey(Nguoi.id), primary_key=True, unique=True)
    bangCap = Column(String(150), nullable=False)


class QuanTriVien(db.Model):
    __tablename__ = 'quan_tri'
    id = Column(String(10), ForeignKey(Nguoi.id), primary_key=True, unique=True)


class ChiTietDanhSach(db.Model):
    __tablename__ = 'ct_danh_sach'
    id = Column(String(10), primary_key=True)
    danhSachKham_id = Column(String(10), ForeignKey(DanhSachKham.id))
    benhNhan_id = Column(String(10), ForeignKey(BenhNhan.id))


class LichSuKham(db.Model):
    __tablename__ = 'lich_su_kham'
    id = Column(String(10), primary_key=True)
    ngayTao = Column(DATE, nullable=False)
    ngayCapNhat = Column(DATE, nullable=False)
    #
    benhNhan_id = Column(String(10), ForeignKey(BenhNhan.id))
    benh_nhan = relationship('BenhNhan', back_populates="lich_su_kham")


class PhieuKham(db.Model):
    __tablename__ = 'phieu_kham'
    id = Column(String(10), primary_key=True, unique=True)
    chuanDoan = Column(String(250), nullable=False)
    ngayKham = Column(DATE, nullable=False)
    trieuChung = Column(String(250), nullable=False)
    # Các mối quan hệ
    lich_su_kham_id = Column(String(10), ForeignKey(LichSuKham.id))
    benh_nhan_id = Column(String(10), ForeignKey(BenhNhan.id))
    hoa_don = relationship('HoaDon', backref='phieu_kham', lazy=True)
    phieu_thuoc = relationship('PhieuThuoc', backref="phieu_kham", lazy=True)


class HoaDon(db.Model):  # hóa đơn
    __tablename__ = 'hoa_don'
    id = Column(String(10), primary_key=True, unique=True)
    ngayKham = Column(DATE, nullable=False)
    tienKham = Column(Float, nullable=False)
    tienThuoc = Column(Float, nullable=False)

    phieu_kham_id = Column(String(10), ForeignKey(PhieuKham.id))


class DonViThuoc(db.Model):  # đơn vị thuốc
    __tablename__ = 'don_vi_thuoc'
    id = Column(String(10), primary_key=True)
    tenDonVi = Column(String(50), nullable=False)
    moTa = Column(String(300), nullable=False)
    thuoc = relationship('Thuoc', backref='don_vi_thuoc', lazy=True)


class DanhMuc(db.Model):
    __tablename__ = 'danh_muc'
    id = Column(String(10), primary_key=True)
    tenDanhMuc = Column(String(50), nullable=False)
    thuoc = relationship('Thuoc', backref='danh_muc', lazy=True)


class Thuoc(db.Model):  # thuốc
    __tablename__ = 'thuoc'
    id = Column(String(10), primary_key=True)
    tenThuoc = Column(String(50), nullable=False)
    moTa = Column(String(300), nullable=False)
    gia = Column(Float, default=0)
    trangThai = Column(Boolean, nullable=False)
    don_vi_thuoc_id = Column(String(10), ForeignKey(DonViThuoc.id))
    danh_muc_id = Column(String(10), ForeignKey(DanhMuc.id))
    phieu_thuoc = relationship('PhieuThuoc', backref='thuoc', lazy=True)


class PhieuThuoc(db.Model):
    __tablename__ = 'phieu_thuoc'
    id = Column(String(10), primary_key=True)
    soLuong = Column(Integer, nullable=False)
    cachDung = Column(String(300), nullable=False)
    #
    phieu_kham_id = Column(String(10), ForeignKey(PhieuKham.id), nullable=False)
    thuoc_id = Column(String(10), ForeignKey(Thuoc.id), nullable=False)


if __name__ == '__main__':
    with app.app_context():
        # db.drop_all()
        db.create_all()
        # dữ liệu bảng Nguoi, 30 dòng-----------------------------------------------------------------------
        # ds_nguoi = [
        #     Nguoi(id='P1', hoTen="Nguyễn Văn An", ngaySinh=date(2000, 1, 10), gioiTinh=True,
        #           diaChi="123 Đường Lê Lợi, Quận 1, TP.Hồ Chí Minh", soDienThoai='0123456789',
        #           email='nguyen.van.an@gmail.com'),
        #     Nguoi(id='P2', hoTen="Trần Thị Bảo", ngaySinh=date(1995, 5, 20), gioiTinh=False,
        #           diaChi="456 Đường Nguyễn Huệ, Quận 3, TP.Hồ Chí Minh", soDienThoai='0987654321',
        #           email='tran.thi.bao@gmail.com'),
        #     Nguoi(id='P3', hoTen="Phạm Văn Cường", ngaySinh=date(1988, 8, 5), gioiTinh=True,
        #           diaChi="789 Đường Võ Văn Tần, Quận 10, TP.Hồ Chí Minh", soDienThoai='0123987654',
        #           email='pham.van.cuong@gmail.com'),
        #     Nguoi(id='P4', hoTen="Lê Minh Dương", ngaySinh=date(2002, 2, 15), gioiTinh=True,
        #           diaChi="101 Đường Phan Chu Trinh, Quận 5, TP.Hồ Chí Minh", soDienThoai='0345678901',
        #           email='le.minh.duong@gmail.com'),
        #     Nguoi(id='P5', hoTen="Hoàng Thị Em", ngaySinh=date(1990, 10, 25), gioiTinh=False,
        #           diaChi="202 Đường Bùi Viện, Quận 1, TP.Hồ Chí Minh", soDienThoai='0765432109',
        #           email='hoang.thi.em@gmail.com'),
        #     Nguoi(id='P6', hoTen="Ngô Văn Phúc", ngaySinh=date(1985, 3, 8), gioiTinh=True,
        #           diaChi="303 Đường Lý Tự Trọng, Quận 3, TP.Hồ Chí Minh", soDienThoai='0912345678',
        #           email='ngo.van.phuc@gmail.com'),
        #     Nguoi(id='P7', hoTen="Vũ Thị Hoa", ngaySinh=date(1998, 7, 17), gioiTinh=False,
        #           diaChi="404 Đường Trần Hưng Đạo, Quận 1, TP.Hồ Chí Minh", soDienThoai='0654321098',
        #           email='vu.thi.hoa@gmail.com'),
        #     Nguoi(id='P8', hoTen="Đinh Văn Giang", ngaySinh=date(1993, 4, 30), gioiTinh=True,
        #           diaChi="505 Đường Cách Mạng Tháng Tám, Quận 3, TP.Hồ Chí Minh", soDienThoai='0123456789',
        #           email='dinh.van.giang@gmail.com'),
        #     Nguoi(id='P9', hoTen="Bùi Thị Hồng", ngaySinh=date(1996, 6, 11), gioiTinh=False,
        #           diaChi="606 Đường Võ Thị Sáu, Quận 3, TP.Hồ Chí Minh", soDienThoai='0987654321',
        #           email='bui.thi.hong@gmail.com'),
        #     Nguoi(id='P10', hoTen="Lý Văn Anh", ngaySinh=date(1991, 9, 3), gioiTinh=True,
        #           diaChi="707 Đường Nguyễn Đình Chính, Quận Phú Nhuận, TP.Hồ Chí Minh", soDienThoai='0123987654',
        #           email='ly.van.anh@gmail.com'),
        #     Nguoi(id='P11', hoTen="Mai Thị Kim", ngaySinh=date(1989, 11, 22), gioiTinh=False,
        #           diaChi="808 Đường Huỳnh Khương Ninh, Quận 1, TP.Hồ Chí Minh", soDienThoai='0345678901',
        #           email='mai.thi.kim@gmail.com'),
        #     Nguoi(id='P12', hoTen="Hồ Văn Long", ngaySinh=date(2001, 12, 7), gioiTinh=True,
        #           diaChi="909 Đường Thống Nhất, Quận Gò Vấp, TP.Hồ Chí Minh", soDienThoai='0765432109',
        #           email='ho.van.long@gmail.com'),
        #     Nguoi(id='P13', hoTen="Trương Thị Mỹ", ngaySinh=date(1986, 2, 19), gioiTinh=False,
        #           diaChi="1010 Đường Hồ Bieu Chanh, Quận 10, TP.Hồ Chí Minh", soDienThoai='0912345678',
        #           email='truong.thi.my@gmail.com'),
        #     Nguoi(id='P14', hoTen="Đặng Văn Nam", ngaySinh=date(1997, 5, 29), gioiTinh=True,
        #           diaChi="1111 Đường Văn Cao, Quận Bình Thạnh, TP.Hồ Chí Minh", soDienThoai='0654321098',
        #           email='dang.van.nam@gmail.com'),
        #     Nguoi(id='P15', hoTen="Lưu Thị Phương", ngaySinh=date(1994, 8, 14), gioiTinh=False,
        #           diaChi="1212 Đường Nguyễn Công Trứ, Quận 4, TP.Hồ Chí Minh", soDienThoai='0123456789',
        #           email='luu.thi.phuong@gmail.com'),
        #     Nguoi(id='P16', hoTen="Nguyễn Thị Bình", ngaySinh=date(2000, 6, 15), gioiTinh=False,
        #           diaChi="456 Đường Hai Bà Trưng, Quận 1, TP.Hồ Chí Minh", soDienThoai='0123456789',
        #           email='nguyen.thi.binh@gmail.com'),
        #     Nguoi(id='P17', hoTen="Trần Văn Cường", ngaySinh=date(1995, 10, 20), gioiTinh=True,
        #           diaChi="789 Đường Lê Duẩn, Quận 3, TP.Hồ Chí Minh", soDienThoai='0987654321',
        #           email='tran.van.cuong@gmail.com'),
        #     Nguoi(id='P18', hoTen="Phạm Thị Diệu", ngaySinh=date(1988, 12, 5), gioiTinh=False,
        #           diaChi="101 Đường Nguyễn Thị Minh Khai, Quận 10, TP.Hồ Chí Minh", soDienThoai='0123987654',
        #           email='pham.thi.dieu@gmail.com'),
        #     Nguoi(id='P19', hoTen="Lê Văn Đức", ngaySinh=date(2002, 3, 25), gioiTinh=True,
        #           diaChi="202 Đường Cách Mạng Tháng Tám, Quận 5, TP.Hồ Chí Minh", soDienThoai='0345678901',
        #           email='le.van.duc@gmail.com'),
        #     Nguoi(id='P20', hoTen="Hoàng Thị Hà", ngaySinh=date(1990, 11, 5), gioiTinh=False,
        #           diaChi="303 Đường Trần Hưng Đạo, Quận 1, TP.Hồ Chí Minh", soDienThoai='0765432109',
        #           email='hoang.thi.ha@gmail.com'),
        #     Nguoi(id='P21', hoTen="Ngô Văn Hải", ngaySinh=date(1985, 7, 8), gioiTinh=True,
        #           diaChi="404 Đường Đinh Công Tráng, Quận 3, TP.Hồ Chí Minh", soDienThoai='0912345678',
        #           email='ngo.van.hai@gmail.com'),
        #     Nguoi(id='P22', hoTen="Vũ Thị Lan", ngaySinh=date(1998, 4, 17), gioiTinh=False,
        #           diaChi="505 Đường Huỳnh Khương Ninh, Quận 1, TP.Hồ Chí Minh", soDienThoai='0654321098',
        #           email='vu.thi.lan@gmail.com'),
        #     Nguoi(id='P23', hoTen="Đinh Văn Khánh", ngaySinh=date(1993, 2, 28), gioiTinh=True,
        #           diaChi="606 Đường Cao Thắng, Quận 3, TP.Hồ Chí Minh", soDienThoai='0123456789',
        #           email='dinh.van.khanh@gmail.com'),
        #     Nguoi(id='P24', hoTen="Bùi Thị Lan Anh", ngaySinh=date(1996, 6, 11), gioiTinh=False,
        #           diaChi="707 Đường Võ Thị Sáu, Quận 3, TP.Hồ Chí Minh", soDienThoai='0987654321',
        #           email='bui.thi.lan.anh@gmail.com'),
        #     Nguoi(id='P25', hoTen="Lý Thị Mai", ngaySinh=date(1991, 9, 13), gioiTinh=True,
        #           diaChi="808 Đường Bùi Viện, Quận 1, TP.Hồ Chí Minh", soDienThoai='0123987654',
        #           email='ly.thi.mai@gmail.com'),
        #     Nguoi(id='P26', hoTen="Mai Thị Ngọc", ngaySinh=date(1989, 11, 22), gioiTinh=False,
        #           diaChi="909 Đường Lê Thánh Tôn, Quận Gò Vấp, TP.Hồ Chí Minh", soDienThoai='0345678901',
        #           email='mai.thi.ngoc@gmail.com'),
        #     Nguoi(id='P27', hoTen="Hồ Văn Phú", ngaySinh=date(2001, 12, 7), gioiTinh=True,
        #           diaChi="1010 Đường Nguyễn Đình Chính, Quận Phú Nhuận, TP.Hồ Chí Minh", soDienThoai='0765432109',
        #           email='ho.van.phu@gmail.com'),
        #     Nguoi(id='P28', hoTen="Trương Thị Quỳnh", ngaySinh=date(1986, 2, 19), gioiTinh=False,
        #           diaChi="1111 Đường Lê Văn Sỹ, Quận Tân Bình, TP.Hồ Chí Minh", soDienThoai='0912345678',
        #           email='truong.thi.quynh@gmail.com'),
        #     Nguoi(id='P29', hoTen="Đặng Văn Sơn", ngaySinh=date(1997, 5, 29), gioiTinh=True,
        #           diaChi="1212 Đường Điện Biên Phủ, Quận Bình Thạnh, TP.Hồ Chí Minh", soDienThoai='0654321098',
        #           email='dang.van.son@gmail.com'),
        #     Nguoi(id='P30', hoTen="Lưu Thị Thảo", ngaySinh=date(1994, 8, 14), gioiTinh=False,
        #           diaChi="1313 Đường Võ Văn Kiệt, Quận 4, TP.Hồ Chí Minh", soDienThoai='0123456789',
        #           email='luu.thi.thao@gmail.com')
        # ]
        # db.session.add_all(ds_nguoi)
        # db.session.commit()
        # # dữ liệu bệnh nhân, 12 dòng---------------------------------------------------------------------------
        # ds_benhnhan = [
        #     BenhNhan(id='P1'),
        #     BenhNhan(id='P2'),
        #     BenhNhan(id='P3'),
        #     BenhNhan(id='P4'),
        #     BenhNhan(id='P5'),
        #     BenhNhan(id='P6'),
        #     BenhNhan(id='P7'),
        #     BenhNhan(id='P8'),
        #     BenhNhan(id='P9'),
        #     BenhNhan(id='P10'),
        #     BenhNhan(id='P11'),
        #     BenhNhan(id='P12'),
        # ]
        # db.session.add_all(ds_benhnhan)
        # db.session.commit()
        # # # dữ liệu bác sĩ , 7 dòng-------------------------------------------------------------------
        # ds_bacsi = [
        #     BacSi(id='P13', chungChi='Bác Sĩ Y Khoa', chuyenKhoa='Tim Mạch'),
        #     BacSi(id='P14', chungChi='Bác Sĩ Y Học Thực Hành', chuyenKhoa='Cơ Xương Khớp'),
        #     BacSi(id='P15', chungChi='Bác Sĩ Y Khoa', chuyenKhoa='Thần Kinh'),
        #     BacSi(id='P16', chungChi='Bác Sĩ Y Học Thực Hành', chuyenKhoa='Da Liễu'),
        #     BacSi(id='P17', chungChi='Bác Sĩ Y Khoa', chuyenKhoa='Nội Tiêu Hóa'),
        #     BacSi(id='P18', chungChi='Bác Sĩ Y Học Thực Hành', chuyenKhoa='Mắt Học'),
        #     BacSi(id='P19', chungChi='Bác Sĩ Y Khoa', chuyenKhoa='Hô Hấp'),
        # ]
        # db.session.add_all(ds_bacsi)
        # db.session.commit()
        # # y tá------------------------------------------------------------------------------
        # ds_yta = [
        #     YTa(id='P20', bangCap='Đại học'),
        #     YTa(id='P21', bangCap='Thạc sĩ'),
        #     YTa(id='P22', bangCap='Đại học'),
        #     YTa(id='P23', bangCap='Thạc sĩ'),
        #     YTa(id='P24', bangCap='Đại học')
        # ]
        # db.session.add_all(ds_yta)
        # db.session.commit()
        # # # nhan vien---------------------------------------------------------------------------
        # ds_nhanvien=[
        #     NhanVien(id='P25', bangCap='Đại học'),
        #     NhanVien(id='P26', bangCap='Thạc sĩ'),
        #     NhanVien(id='P27', bangCap='Đại học'),
        # ]
        # db.session.add_all(ds_nhanvien)
        # db.session.commit()
        # # #quan tri--------------------------------------------------------------------------------
        # ds_admin = [
        #     NhanVien(id='P28', bangCap='Đại học'),
        #     NhanVien(id='P29', bangCap='Thạc sĩ'),
        #     NhanVien(id='P30', bangCap='Đại học'),
        # ]
        # db.session.add_all(ds_admin)
        # db.session.commit()
        #
        # dv1= DonViThuoc(id="DV1", tenDonVi='chai', moTa='chai ')
        # dv2 = DonViThuoc(id="DV2", tenDonVi='lọ',moTa='lọ')
        # dv3 = DonViThuoc(id="DV3", tenDonVi='vỉ', moTa='vỉ')
        # db.session.add_all([dv1,dv2,dv3])
        # db.session.commit()
        # ds_danhmuc=[
        #     DanhMuc(id='DM1', tenDanhMuc='Giảm đau và Giảm sốt'),
        #     DanhMuc(id='DM2', tenDanhMuc='Chống viêm'),
        #     DanhMuc(id='DM3', tenDanhMuc='Kháng sinh'),
        #     DanhMuc(id='DM4', tenDanhMuc='Chống dị ứng'),
        #     DanhMuc(id='DM5', tenDanhMuc='Chống axit dạ dày'),
        #     DanhMuc(id='DM6', tenDanhMuc='Giảm cholesterol'),
        #     DanhMuc(id='DM7', tenDanhMuc='Thuốc đối kháng đường huyết'),
        #     DanhMuc(id='DM8', tenDanhMuc='Thuốc lợi tiểu'),
        #     DanhMuc(id='DM9', tenDanhMuc='Thuốc nội tiết'),
        #     DanhMuc(id='DM10', tenDanhMuc='Corticosteroid'),
        #     DanhMuc(id='DM11', tenDanhMuc='Chống đông máu'),
        #     DanhMuc(id='DM12', tenDanhMuc='Thuốc an thần'),
        #     DanhMuc(id='DM13', tenDanhMuc='Chống tăng huyết áp'),
        #     DanhMuc(id='DM14', tenDanhMuc='Thuốc chống nấm'),
        #
        # ]
        # db.session.add_all(ds_danhmuc)
        # db.session.commit()
        # # thuóc
        # ds_thuoc = [
        #     Thuoc(id='1', tenThuoc='Paracetamol', moTa='Giảm sốt', gia=91770, trangThai=True, don_vi_thuoc_id='DV3',danh_muc_id='DM1'),
        #     Thuoc(id='2', tenThuoc='Aspirin', moTa='Giảm đau', gia=137770, trangThai=True, don_vi_thuoc_id='DV1',danh_muc_id='DM1'),
        #     Thuoc(id='3', tenThuoc='Ibuprofen', moTa='Chống viêm', gia=183770, trangThai=True, don_vi_thuoc_id='DV3',danh_muc_id='DM2'),
        #     Thuoc(id='4', tenThuoc='Amoxicillin', moTa='Kháng sinh', gia=298770, trangThai=True, don_vi_thuoc_id='DV2',danh_muc_id='DM3'),
        #     Thuoc(id='5', tenThuoc='Cetirizine', moTa='Chống dị ứng', gia=206770, trangThai=True,
        #           don_vi_thuoc_id='DV1',danh_muc_id='DM4'),
        #     Thuoc(id='6', tenThuoc='Loratadine', moTa='Chống dị ứng', gia=229770, trangThai=True,
        #           don_vi_thuoc_id='DV3',danh_muc_id='DM4'),
        #     Thuoc(id='7', tenThuoc='Omeprazole', moTa='Chống axit dạ dày', gia=367770, trangThai=True,
        #           don_vi_thuoc_id='DV1',danh_muc_id='DM5'),
        #     Thuoc(id='8', tenThuoc='Simvastatin', moTa='Giảm cholesterol', gia=275770, trangThai=True,
        #           don_vi_thuoc_id='DV3',danh_muc_id='DM6'),
        #     Thuoc(id='9', tenThuoc='Metformin', moTa='Thuốc đối kháng đường huyết', gia=252770, trangThai=True,
        #           don_vi_thuoc_id='DV2',danh_muc_id='DM7'),
        #     Thuoc(id='10', tenThuoc='Hydrochlorothiazide', moTa='Thuốc lợi tiểu', gia=344770, trangThai=True,
        #           don_vi_thuoc_id='DV2',danh_muc_id='DM8'),
        #     Thuoc(id='11', tenThuoc='Ibuprofen-vs2', moTa='Chống viêm', gia=183770, trangThai=True, don_vi_thuoc_id='DV3',danh_muc_id='DM2'),
        #     Thuoc(id='12', tenThuoc='Cephalosporin', moTa='Kháng sinh', gia=394770, trangThai=True,
        #           don_vi_thuoc_id='DV3',danh_muc_id='DM3'),
        #     Thuoc(id='13', tenThuoc='Efferalgan', moTa='Chống dị ứng', gia=406770, trangThai=True,
        #           don_vi_thuoc_id='DV2',danh_muc_id='DM4'),
        #     Thuoc(id='14', tenThuoc='Corticoid', moTa='Chống dị ứng', gia=319770, trangThai=True,
        #           don_vi_thuoc_id='DV2',danh_muc_id='DM4'),
        #     Thuoc(id='15', tenThuoc='Lansoprazole', moTa='Chống axit dạ dày', gia=351470, trangThai=True,
        #           don_vi_thuoc_id='DV1',danh_muc_id='DM5'),
        #     Thuoc(id='16', tenThuoc='Lipitor', moTa='Giảm cholesterol', gia=275770, trangThai=True,
        #           don_vi_thuoc_id='DV3',danh_muc_id='DM6'),
        #     Thuoc(id='17', tenThuoc='Thiazolidinedione', moTa='Thuốc đối kháng đường huyết', gia=252770, trangThai=True,
        #           don_vi_thuoc_id='DV3',danh_muc_id='DM7'),
        #     Thuoc(id='18', tenThuoc='Spironolactone', moTa='Thuốc lợi tiểu', gia=454770, trangThai=True,
        #           don_vi_thuoc_id='DV1',danh_muc_id='DM8'),
        #     Thuoc(id='19', tenThuoc='Atorvastatin', moTa='Giảm cholesterol', gia=321770, trangThai=True,
        #           don_vi_thuoc_id='DV3'),
        #     Thuoc(id='20', tenThuoc='Levothyroxine', moTa='Thuốc nội tiết', gia=389770, trangThai=True,
        #           don_vi_thuoc_id='DV2',danh_muc_id='DM9'),
        #     Thuoc(id='21', tenThuoc='Prednisone', moTa='Corticosteroid', gia=436770, trangThai=True,
        #           don_vi_thuoc_id='DV1',danh_muc_id='DM10'),
        #     Thuoc(id='22', tenThuoc='Warfarin', moTa='Chống đông máu', gia=481770, trangThai=True,
        #           don_vi_thuoc_id='DV1',danh_muc_id='DM11'),
        #     Thuoc(id='23', tenThuoc='Ciprofloxacin', moTa='Kháng sinh', gia=528770, trangThai=True,
        #           don_vi_thuoc_id='DV3',danh_muc_id='DM3'),
        #     Thuoc(id='24', tenThuoc='Diazepam', moTa='Thuốc an thần', gia=573770, trangThai=True, don_vi_thuoc_id='DV3',danh_muc_id='DM12'),
        #     Thuoc(id='25', tenThuoc='Enalapril', moTa='Chống tăng huyết áp', gia=618770, trangThai=True,
        #           don_vi_thuoc_id='DV2',danh_muc_id='DM13'),
        #     Thuoc(id='26', tenThuoc='Gabapentin', moTa='Thuốc an thần', gia=663770, trangThai=True,
        #           don_vi_thuoc_id='DV3',danh_muc_id='DM12'),
        #     Thuoc(id='27', tenThuoc='Hydralazine', moTa='Chống tăng huyết áp', gia=708770, trangThai=True,
        #           don_vi_thuoc_id='DV2',danh_muc_id='DM13'),
        #     Thuoc(id='28', tenThuoc='Isoniazid', moTa='Kháng sinh', gia=753770, trangThai=True, don_vi_thuoc_id='DV3',danh_muc_id='DM3'),
        #     Thuoc(id='29', tenThuoc='Ketoconazole', moTa='Thuốc chống nấm', gia=798770, trangThai=True,
        #           don_vi_thuoc_id='DV1',danh_muc_id='DM14'),
        #     Thuoc(id='30', tenThuoc='Lisinopril', moTa='Chống tăng huyết áp', gia=843770, trangThai=True,
        #           don_vi_thuoc_id='DV2',danh_muc_id='DM13')
        #
        # ]
        # db.session.add_all(ds_thuoc)
        # db.session.commit()
