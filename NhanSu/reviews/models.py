# hr/models.py
from django.db import models
from django.core.validators import MinValueValidator, RegexValidator, EmailValidator
from django.core.exceptions import ValidationError
from django.utils import timezone


# ----- choices -----
GIOITINH_CHOICES = [
    ('Nam', 'Nam'),
    ('Nữ', 'Nữ'),
    ('Khác', 'Khác'),
]

NHANVIEN_TRANGTHAI = [
    ('Đang làm', 'Đang làm'),
    ('Thử việc', 'Thử việc'),
    ('Tạm nghỉ', 'Tạm nghỉ'),
    ('Đã nghỉ', 'Đã nghỉ'),
]

HOPDONG_TRANGTHAI = [
    ('Hiệu lực', 'Hiệu lực'),
    ('Hết hạn', 'Hết hạn'),
    ('Lưu trữ', 'Lưu trữ'),
]

NGHIPHEP_LOAI = [
    ('Phep nam', 'Phep nam'),
    ('Nghi om', 'Nghi om'),
    ('Nghi Thai San', 'Nghi Thai San'),
    ('Cong Tac', 'Cong Tac'),
    ('Khac', 'Khac'),
]

DON_TRANGTHAI = [
    ('Cho duyet', 'Cho duyet'),
    ('Da duyet', 'Da duyet'),
    ('Tu choi', 'Tu choi'),
]

TAIKHOAN_ROLES = [
    ('Admin', 'Admin'),
    ('HR', 'HR'),
    ('GiamDoc', 'GiamDoc'),
    ('NhanVien', 'NhanVien'),
]

BANGCONG_TRANGTHAI = [
    ('Gui duyet', 'Gui duyet'),
    ('Cho duyet', 'Cho duyet'),
    ('Da duyet', 'Da duyet'),
    ('Tu choi', 'Tu choi'),
]


# ----- validators -----
phone_validator = RegexValidator(r'^\d{9,11}$', 'Số điện thoại phải là 9-11 chữ số.')
code_validator = RegexValidator(r'^[A-Za-z0-9_\-]+$', 'Chỉ được dùng chữ, số, gạch ngang/underscore cho mã.')


# ----- Models -----
class PhongBan(models.Model):
    maPB = models.CharField('MaPB', max_length=20, unique=True, validators=[code_validator])
    tenPhongBan = models.CharField('TenPhongBan', max_length=100)
    vaiTroPB = models.CharField('VaiTroPB', max_length=100, null=True, blank=True)
    truongPhong = models.ForeignKey(
        'NhanVien',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='phongban_lam_truong',
        verbose_name='TruongPhong'
    )

    class Meta:
        db_table = 'PhongBan'

    def __str__(self):
        return f'{self.tenPhongBan} ({self.maPB})'


class ChucVu(models.Model):
    tenChucVu = models.CharField('TenChucVu', max_length=100, unique=True)
    luong = models.DecimalField('Luong', max_digits=18, decimal_places=2, validators=[MinValueValidator(0)], null=True, blank=True)

    class Meta:
        db_table = 'ChucVu'

    def __str__(self):
        return self.tenChucVu


class NhanVien(models.Model):
    maNhanVien = models.CharField('MaNhanVien', max_length=20, unique=True, validators=[code_validator])
    hoTen = models.CharField('HoTen', max_length=100)
    ngaySinh = models.DateField('NgaySinh', null=True, blank=True)
    gioiTinh = models.CharField('GioiTinh', max_length=10, choices=GIOITINH_CHOICES, null=True, blank=True)
    diaChi = models.CharField('DiaChi', max_length=255, null=True, blank=True)
    soDienThoai = models.CharField('SoDienThoai', max_length=11, null=True, blank=True, validators=[phone_validator])
    cccd = models.CharField('CCCD', max_length=20, unique=True, null=True, blank=True)
    email = models.EmailField('Email', max_length=120, unique=True, null=True, blank=True, validators=[EmailValidator()])
    trangThai = models.CharField('TrangThai', max_length=30, choices=NHANVIEN_TRANGTHAI, default='Đang làm')
    ngayVao = models.DateField('NgayVao', null=True, blank=True)
    # Liên kết
    trinhDo = models.ForeignKey('TrinhDoHocVan', on_delete=models.SET_NULL, null=True, blank=True, related_name='nhanvien_trinhdo')
    phongBan = models.ForeignKey('PhongBan', on_delete=models.PROTECT, related_name='nhanviens', verbose_name='PhongBan')
    chucVu = models.ForeignKey('ChucVu', on_delete=models.PROTECT, related_name='nhanviens', verbose_name='ChucVu')

    class Meta:
        db_table = 'NhanVien'

    def __str__(self):
        return f'{self.hoTen} ({self.maNhanVien})'


class TrinhDoHocVan(models.Model):
    # Note: ERD có NhanVien_id ở TrinhDoHocVan, nhưng để tránh vòng lặp lồng nhau
    nhanVien = models.ForeignKey('NhanVien', on_delete=models.CASCADE, related_name='trinhdo_hocvan')
    trinhDo = models.CharField('TrinhDo', max_length=50, null=True, blank=True)
    chuyenNganh = models.CharField('ChuyenNganh', max_length=100, null=True, blank=True)
    truong = models.CharField('Truong', max_length=120, null=True, blank=True)
    namTotNghiep = models.IntegerField('NamTotNghiep', null=True, blank=True)
    bangCap = models.CharField('BangCap', max_length=100, null=True, blank=True)

    class Meta:
        db_table = 'TrinhDoHocVan'

    def __str__(self):
        return f'{self.nhanVien.maNhanVien} - {self.trinhDo or "Chưa rõ"}'


class LoaiHopDong(models.Model):
    loaiHopDong = models.CharField('LoaiHopDong', max_length=50, unique=True)
    moTa = models.CharField('MoTa', max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'LoaiHopDong'

    def __str__(self):
        return self.loaiHopDong


class HopDong(models.Model):
    maHopDong = models.CharField('MaHopDong', max_length=30, unique=True, validators=[code_validator])
    nhanVien = models.ForeignKey('NhanVien', on_delete=models.CASCADE, related_name='hopdongs')
    loaiHopDong = models.ForeignKey('LoaiHopDong', on_delete=models.PROTECT, related_name='hopdongs')
    ngayBatDau = models.DateField('NgayBatDau')
    ngayKetThuc = models.DateField('NgayKetThuc', null=True, blank=True)
    trangThai = models.CharField('TrangThai', max_length=30, choices=HOPDONG_TRANGTHAI)
    noiDungHopDong = models.TextField('NoiDungHopDong', null=True, blank=True)

    class Meta:
        db_table = 'HopDong'

    def clean(self):
        # NgayKetThuc >= NgayBatDau (nếu có)
        if self.ngayKetThuc and self.ngayKetThuc < self.ngayBatDau:
            raise ValidationError({'ngayKetThuc': 'NgayKetThuc phải lớn hơn hoặc bằng NgayBatDau'})

    def __str__(self):
        return f'{self.maHopDong} - {self.nhanVien.maNhanVien}'


class TaiKhoan(models.Model):
    tenDangNhap = models.CharField('TenDangNhap', max_length=50, unique=True)
    matKhau = models.CharField('MatKhau', max_length=255)
    phanQuyen = models.CharField('PhanQuyen', max_length=30, choices=TAIKHOAN_ROLES)
    trangThai = models.BooleanField('TrangThai', default=True)
    nhanVien = models.ForeignKey('NhanVien', on_delete=models.SET_NULL, null=True, blank=True, related_name='taikhoans')

    class Meta:
        db_table = 'TaiKhoan'

    def __str__(self):
        return self.tenDangNhap


class DonNghiPhep(models.Model):
    nhanVien = models.ForeignKey('NhanVien', on_delete=models.CASCADE, related_name='donnghipheps')
    nguoiDuyet = models.ForeignKey('NhanVien', on_delete=models.SET_NULL, null=True, blank=True, related_name='duyet_don')
    ngayBatDau = models.DateField('NgayBatDau')
    ngayKetThuc = models.DateField('NgayKetThuc')
    soNgayNghi = models.IntegerField('SoNgayNghi', validators=[MinValueValidator(0)])
    lyDo = models.CharField('LyDo', max_length=255, null=True, blank=True)
    loaiNghi = models.CharField('LoaiNghi', max_length=50, choices=NGHIPHEP_LOAI)
    ngayTao = models.DateTimeField('NgayTao', default=timezone.now)
    trangThai = models.CharField('TrangThai', max_length=30, choices=DON_TRANGTHAI)
    ngayDuyet = models.DateTimeField('NgayDuyet', null=True, blank=True)

    class Meta:
        db_table = 'DonNghiPhep'

    def clean(self):
        if self.ngayKetThuc < self.ngayBatDau:
            raise ValidationError({'ngayKetThuc': 'NgayKetThuc phải lớn hơn hoặc bằng NgayBatDau'})
        # SoNgayNghi consistency check (optional)
        delta_days = (self.ngayKetThuc - self.ngayBatDau).days + 1
        if self.soNgayNghi is not None and self.soNgayNghi < 0:
            raise ValidationError({'soNgayNghi': 'SoNgayNghi phải >= 0'})
        # Không ép buộc equality với delta_days để linh hoạt (có nửa ngày, ca tối etc.)

    def __str__(self):
        return f'Don #{self.id} - {self.nhanVien.maNhanVien}'


class BangCongTongQuat(models.Model):
    thang = models.IntegerField('Thang')
    nam = models.IntegerField('Nam')
    ngayTao = models.DateField('NgayTao', default=timezone.now)
    tongCong = models.DecimalField('TongCong', max_digits=6, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0)])
    trangThai = models.CharField('TrangThai', max_length=30, choices=BANGCONG_TRANGTHAI)
    nhanVien = models.ForeignKey('NhanVien', on_delete=models.SET_NULL, null=True, blank=True, related_name='bangcong_tongquats')

    class Meta:
        db_table = 'BangCongTongQuat'
        verbose_name = 'BangCongTongQuat'

    def __str__(self):
        return f'BangCong {self.thang}/{self.nam} - NV:{self.nhanVien.maNhanVien if self.nhanVien else "N/A"}'


class ChiTietBangCong(models.Model):
    nhanVien = models.ForeignKey('NhanVien', on_delete=models.CASCADE, related_name='chitiet_congs')
    ngayLamViec = models.DateField('NgayLamViec')
    gioVao = models.TimeField('GioVao', null=True, blank=True)
    gioRa = models.TimeField('GioRa', null=True, blank=True)
    cong = models.FloatField('Cong', validators=[MinValueValidator(0.0)])  # có thể 0, 0.5, 1 ...
    ghiChu = models.CharField('GhiChu', max_length=255, null=True, blank=True)
    gioLamThem = models.FloatField('GioLamThem', null=True, blank=True, validators=[MinValueValidator(0.0)])
    bangCongTongQuat = models.ForeignKey('BangCongTongQuat', on_delete=models.SET_NULL, null=True, blank=True, related_name='chi_tiet_cong')

    class Meta:
        db_table = 'ChiTietBangCong'
        unique_together = ('nhanVien', 'ngayLamViec')  # tránh trùng ngày chấm công

    def clean(self):
        if self.gioVao and self.gioRa:
            # gioRa >= gioVao check by comparing times - if day wrap-around not considered
            if self.gioRa < self.gioVao:
                raise ValidationError({'gioRa': 'GioRa phải lớn hơn hoặc bằng GioVao nếu cả hai có giá trị'})

        # công phải là một trong các giá trị hợp lệ (0, 0.5, 1, etc.)
        # Không bắt buộc cứng, nhưng kiểm tra non-negative đã có

    def __str__(self):
        return f'{self.nhanVien.maNhanVien} - {self.ngayLamViec} ({self.cong})'


class BangLuongTongQuat(models.Model):
    thang = models.IntegerField('Thang', validators=[MinValueValidator(1)])
    nam = models.IntegerField('Nam', validators=[MinValueValidator(1900)])
    ngayTao = models.DateField('NgayTao', default=timezone.now)
    tongLuong = models.DecimalField('TongLuong', max_digits=18, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0)])
    bangCongTongQuat = models.ForeignKey('BangCongTongQuat', on_delete=models.PROTECT, related_name='bangluong_tongquats')

    class Meta:
        db_table = 'BangLuongTongQuat'

    def __str__(self):
        return f'BangLuong {self.thang}/{self.nam}'


class ChiTietLuong(models.Model):
    bangLuongTongQuat = models.ForeignKey('BangLuongTongQuat', on_delete=models.CASCADE, related_name='chi_tiet_luongs')
    nhanVien = models.ForeignKey('NhanVien', on_delete=models.CASCADE, related_name='chi_tiet_luongs')
    luongCoBan = models.DecimalField('LuongCoBan', max_digits=16, decimal_places=2, validators=[MinValueValidator(0)])
    phuCap = models.DecimalField('PhuCap', max_digits=16, decimal_places=2, validators=[MinValueValidator(0)])
    thuong = models.DecimalField('Thuong', max_digits=16, decimal_places=2, validators=[MinValueValidator(0)])
    khauTru = models.DecimalField('KhauTru', max_digits=16, decimal_places=2, validators=[MinValueValidator(0)])
    tongLuong = models.DecimalField('TongLuong', max_digits=16, decimal_places=2, validators=[MinValueValidator(0)])
    ngayPhatHanh = models.DateField('NgayPhatHanh', null=True, blank=True)

    class Meta:
        db_table = 'ChiTietLuong'
        unique_together = ('bangLuongTongQuat', 'nhanVien')

    def clean(self):
        # Tổng lương phải >= 0 (validator đã có). Bạn cũng có thể enforce:
        calc = (self.luongCoBan or 0) + (self.phuCap or 0) + (self.thuong or 0) - (self.khauTru or 0)
        # nếu muốn bắt buộc tính bằng phép tính này:
        # if self.tongLuong != calc:
        #     raise ValidationError({'tongLuong': 'TongLuong không khớp tổng thành phần'})
        # Mình không tự ép, chỉ để tham khảo.
        pass

    def __str__(self):
        return f'Luong NV:{self.nhanVien.maNhanVien} - {self.bangLuongTongQuat.thang}/{self.bangLuongTongQuat.nam}'
