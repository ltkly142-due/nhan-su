from django.db import models
from django.core.validators import MinValueValidator, RegexValidator, EmailValidator
from django.core.exceptions import ValidationError
from django.utils import timezone

GIOITINH_CHOICES = [
    ('NAM', 'Nam'),
    ('NU', 'Nữ'),
    ('KHAC', 'Khác'),
]

NHANVIEN_TRANGTHAI = [
    ('DANG_LAM', 'Đang làm'),
    ('THU_VIEC', 'Thử việc'),
    ('TAM_NGHI', 'Tạm nghỉ'),
    ('DA_NGHI', 'Đã nghỉ'),
]

HOPDONG_TRANGTHAI = [
    ('HIEU_LUC', 'Hiệu lực'),
    ('HET_HAN', 'Hết hạn'),
    ('LUU_TRU', 'Lưu trữ'),
]

NGHIPHEP_LOAI = [
    ('PHEP_NAM', 'Phép năm'),
    ('NGHI_OM', 'Nghỉ ốm'),
    ('NGHI_THAI_SAN', 'Nghỉ Thai Sản'),
    ('CONG_TAC', 'Công tác'),
    ('KHAC', 'Khác'),
]

DON_TRANGTHAI = [
    ('CHO_DUYET', 'Chờ duyệt'),
    ('DA_DUYET', 'Đã duyệt'),
    ('TU_CHOI', 'Từ chối'),
]


BANGCONG_TRANGTHAI = [
    ('GUI_DUYET', 'Gửi duyệt'),
    ('CHO_DUYET', 'Chờ duyệt'),
    ('DA_DUYET', 'Đã duyệt'),
    ('TU_CHOI', 'Từ chối'),
]


# ----- validators -----
phone_validator = RegexValidator(r'^\d{9,11}$', 'Số điện thoại phải là 9-11 chữ số.')
code_validator = RegexValidator(r'^[A-Za-z0-9_\-]+$', 'Chỉ được dùng chữ, số, gạch ngang/underscore cho mã.')



class PhongBan(models.Model):
    MaPB = models.CharField('Mã Phòng Ban', max_length=20, unique=True, validators=[code_validator])
    TenPhongBan = models.CharField('Tên Phòng Ban', max_length=100)
    VaiTroPB = models.CharField('Mô tả vai trò', max_length=100, null=True, blank=True)
    ChucVu = models.ManyToManyField(
        'ChucVu', through = ‘PhongBan_ChucVu’, on_delete=models.SET_NULL, null=True, blank=True, related_name='phongban')

    def __str__(self):
        return f'{self.TenPhongBan} ({self.MaPB})'


class ChucVu(models.Model):
    ChucVu = models.CharField('Tên Chức Vụ', max_length=100, unique=True)
    MoTa   = models.TextField(‘Mô tả’,blank=True)
    Luong = models.DecimalField('Lương', max_digits=18, decimal_places=2, validators=[MinValueValidator(0)], null=True, blank=True)

    def __str__(self):
        return self.ChucVu
        
class PhongBan_ChucVu(models.Model):
    ChucVu   = models.ForeignKey('ChucVu', on_delete=models.CASCADE)
    PhongBan = models.ForeignKey('PhongBan', on_delete=models.CASCADE)

class NhanVien(models.Model):
    MaNhanVien = models.CharField('Mã nhân viên', max_length=20, unique=True, validators=[code_validator])
    HoTen = models.CharField('Họ Tên', max_length=100)
    NgaySinh = models.DateField('Ngày Sinh', null=True, blank=True)
    GioiTinh = models.CharField('Giới tính', max_length=10, choices=GIOITINH_CHOICES, null=True, blank=True)
    DiaChi = models.CharField('Địa chỉ', max_length=255, null=True, blank=True)
    SoDienThoai = models.CharField('Số điện thoại', max_length=11, null=True, blank=True, validators=[phone_validator])
    CCCD = models.CharField('CCCD', max_length=20, unique=True, null=True, blank=True)
    Email = models.EmailField('Email', max_length=120, unique=True, null=True, blank=True, validators=[EmailValidator()])
    TrangThai = models.CharField('Trạng Thái, max_length=30, choices=NHANVIEN_TRANGTHAI, default='Đang làm')
    NgayVao = models.DateField('Ngày vào', null=True, blank=True)
    # Liên kết
    TDHV = models.ForeignKey('TrinhDoHocVan', on_delete=models.SET_NULL, null=True, blank=True, related_name='nhanvien_trinhdo')
    PhongBan = models.ForeignKey('PhongBan', on_delete=models.PROTECT, related_name='nhanviens', verbose_name='PhongBan')

    def __str__(self):
        return f'{self.HoTen} ({self.MaNhanVien})'


class TrinhDoHocVan(models.Model):
    TrinhDo = models.CharField('Trình độ, max_length=50, null=True, blank=True)
    ChuyenNganh = models.CharField('Chuyên ngành', max_length=100, null=True, blank=True)
    Truong = models.CharField('Trường', max_length=120, null=True, blank=True)
    NamTotNghiep = models.IntegerField('Năm tốt nghiệp', null=True, blank=True)
    BangCap = models.CharField('Bằng cấp', max_length=100, null=True, blank=True)

    def __str__(self):
        return f'{self.NhanVien.MaNhanVien} - {self.TrinhDo or "Chưa rõ"}'


class LoaiHopDong(models.Model):
    LoaiHopDong = models.CharField('Loại Hợp đồng', max_length=50, unique=True)
    MoTa = models.CharField('Mô tả', max_length=255, null=True, blank=True)

    def __str__(self):
        return self.LoaiHopDong


class HopDong(models.Model):
    MaHopDong = models.CharField('Mã Hợp đồng', max_length=30, unique=True, validators=[code_validator])
    NhanVien = models.ForeignKey('NhanVien', on_delete=models.CASCADE, related_name='hopdong')
    LoaiHopDong = models.ForeignKey('LoaiHopDong', on_delete=models.PROTECT, related_name='hopdongs')
    NgayBatDau = models.DateField('Ngày bắt đầu')
    NgayKetThuc = models.DateField('Ngày kết thúc', null=True, blank=True)
    TrangThai = models.CharField('Trạng thái', max_length=30, choices=HOPDONG_TRANGTHAI)
    NoiDungHopDong = models.TextField('Nội dung Hợp đồng', null=True, blank=True)

    def clean(self):
        if self.NgayKetThuc and self.NgayKetThuc < self.NgayBatDau:
            raise ValidationError({'NgayKetThuc': 'Ngày kết thúc phải lớn hơn hoặc bằng Ngày bắt đầu'})

    def __str__(self):
        return f'{self.MaHopDong} - {self.NhanVien.MaNhanVien}'



class DonNghiPhep(models.Model):
    NhanVien = models.ForeignKey('NhanVien', on_delete=models.CASCADE, related_name='don_nghi_phep')
    NguoiDuyet = models.ForeignKey('NhanVien', on_delete=models.SET_NULL, null=True, blank=True, related_name='duyet_don')
    NgayBatDau = models.DateField('Ngày bắt đầu')
    NgayKetThuc = models.DateField('Ngày kết thúc')
    SoNgayNghi = models.IntegerField('Số ngày nghỉ', validators=[MinValueValidator(0)])
    LyDo = models.CharField('Lý do', max_length=255, null=True, blank=True)
    LoaiNghi = models.CharField('Loại nghỉ', max_length=50, choices=NGHIPHEP_LOAI)
    NgayTao = models.DateTimeField('Ngày tạo', default=timezone.now)
    TrangThai = models.CharField('Trạng thái', max_length=30, choices=DON_TRANGTHAI)
    NgayDuyet = models.DateTimeField('Ngày duyệt', null=True, blank=True)

    def clean(self):
        if self.NgayKetThuc < self.NgayBatDau:
            raise ValidationError({'NgayKetThuc': 'Ngày kết thúc phải lớn hơn hoặc bằng Ngày bắt đầu'})

    def __str__(self):
        return f'Don #{self.id} - {self.NhanVien.MaNhanVien}'


class BangCongThang(models.Model):
    Thang = models.IntegerField('Tháng')
    Nam = models.IntegerField('Năm')
    NgayTao = models.DateField('Ngày tạo', default=timezone.now)
    TongCong = models.DecimalField('Tổng công', max_digits=6, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0)])
    TrangThai = models.CharField('Trạng Thái', max_length=30, choices=BANGCONG_TRANGTHAI)
    NhanVien = models.ForeignKey('NhanVien', on_delete=models.SET_NULL, null=True, blank=True, related_name='bangcong_thang')

    def __str__(self):
        return f'BangCong {self.thang}/{self.nam} - NV:{self.NhanVien.MaNhanVien if self.NhanVien else "N/A"}'

class ChiTietBangCong(models.Model):
    NhanVien = models.ForeignKey('NhanVien', on_delete=models.CASCADE, related_name='chitiet_cong')
    NgayLamViec = models.DateField('Ngày làm việc')
    GioVao = models.TimeField('Giờ vào', null=True, blank=True)
    GioRa = models.TimeField('Giờ ra', null=True, blank=True)
    Cong = models.FloatField('Công', validators=[MinValueValidator(0.0)])  # có thể 0, 0.5, 1 ...
    GhiChu = models.CharField('Ghi chú', max_length=255, null=True, blank=True)
    GioLamThem = models.FloatField('Giờ làm thêm', null=True, blank=True, validators=[MinValueValidator(0.0)])
    BangCongThang = models.ForeignKey('BangCongThang', on_delete=models.SET_NULL, null=True, blank=True, related_name='chi_tiet_cong')

    def clean(self):
        if self.GioVao and self.GioRa:
            if self.GioRa < self.GioVao:
                raise ValidationError({'GioRa': 'Giờ ra phải lớn hơn hoặc bằng Giờ vào nếu cả hai có giá trị'})

    def __str__(self):
        return f'{self.NhanVien.MaNhanVien} - {self.NgayLamViec} ({self.Cong})'


class BangLuongThangt(models.Model):
    Thang = models.IntegerField('Tháng', validators=[MinValueValidator(1)])
    Nam = models.IntegerField('Năm', validators=[MinValueValidator(1900)])
    NgayTao = models.DateField('Ngày Tạo', default=timezone.now)
    TongLuong = models.DecimalField('Tổng lương', max_digits=18, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0)])
    BangCongThang = models.ForeignKey('BangCongThang', on_delete=models.PROTECT, related_name='bangluong_thang')

    def __str__(self):
        return f'BangLuong {self.thang}/{self.nam}'


class ChiTietLuong(models.Model):
    BangLuongThang = models.ForeignKey('BangLuongThang', on_delete=models.CASCADE, related_name='chi_tiet_luong')
    NhanVien = models.ForeignKey('NhanVien', on_delete=models.CASCADE, related_name='chi_tiet_luong')
    LuongCoBan = models.DecimalField('Lương cơ bản', max_digits=16, decimal_places=2, validators=[MinValueValidator(0)])
    PhuCap = models.DecimalField('Phụ cấp', max_digits=16, decimal_places=2, validators=[MinValueValidator(0)])
    Thuong = models.DecimalField('Thưởng', max_digits=16, decimal_places=2, validators=[MinValueValidator(0)])
    KhauTru = models.DecimalField('Khấu trừ', max_digits=16, decimal_places=2, validators=[MinValueValidator(0)])
    TongLuong = models.DecimalField('Tổng lương', max_digits=16, decimal_places=2, null = True, blank = True, validators=[MinValueValidator(0)])
    NgayPhatHanh = models.DateField('Ngày phát hành', null=True, blank=True)

    def __str__(self):
        return f'Luong NV:{self.NhanVien.MaNhanVien} - {self.BangLuongThang.thang}/{self.BangLuongThang.nam}'

