from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django import forms
# TRANG LOGIN
class LoginForm(forms.Form):
    username = forms.CharField(label="Tên đăng nhập")
    password = forms.CharField(label="Mật khẩu", widget=forms.PasswordInput)

def login_view(request):
    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            form.add_error(None, "Tên đăng nhập hoặc mật khẩu không đúng.")
    return render(request, 'login.html', {'form': form})

def dangnhap_sai(request):
    return render(request, 'loginerro.html')

def taikhoan_bikhoa(request):
    return render(request, 'loginkey.html')

# TRANG CHỦ
def dashboard_TP(request):
    return render(request, 'trangchu_TP.html')
def dashboard_GD(request):
    return render(request, 'trangchu_GD.html')
def dashboard_NV(request):
    return render(request, 'trangchu_NV.html')
def dashboard_NVNS(request):
    return render(request, 'trangchu_NVNS.html')

# DANH SÁCH NHÂN VIÊN
def dsnv_nvns(request):
    return render(request, "DSNV_NVNS.html")
def dsnv_tp(request):
    return render(request, "DSNV_TP.html")
def dsnv_gd(request):
    return render(request, "DSNV_GD.html")

# TRANG CHI TIẾT HỒ SƠ NHÂN VIÊN
def chitiet_hoso_nvns(request):
    return render(request, "chitiet_hoso_NVNS.html")
def chitiet_hoso_tp(request):
    return render(request, "chitiet_hoso_TP.html")
def chitiet_hoso_gd(request):
    return render(request, "chitiet_hoso_GD.html")

# TRANG ADD VÀ EDIT
def add_hoso(request):
    return render(request, 'add_hoso.html')
def edit_hoso(request):
    return render(request, 'edit_hoso.html')

def delete_hoso(request):
    return render(request, 'delete_hoso.html')

def qlhd_nvns(request):
    return render(request, "QLHD_NVNS.html", {'active_page': 'hopdong'})

def qlhd_tp(request):
    return render(request, "QLHD_TP.html", {'active_page': 'hopdong'})

def them_hopdong(request):
    return render(request, "them_hopdong.html", {'active_page': 'hopdong'})

def chinhsua_hopdong(request):
    return render(request, "chinhsua_hopdong.html", {'active_page': 'hopdong'})

def chitiet_hopdong(request):
    return render(request, "chitiet_hopdong.html", {'active_page': 'hopdong'})

def xoa_hopdong(request):
    return render(request, "xoa_hopdong.html", {'active_page': 'hopdong'})

# # sau ni bỏ database thì đặt id
# # def chitiet_hoso_tp(request, id):
# #     nhanvien = get_object_or_404(NhanVien, id=id)
# #     return render(request, 'chitiet_hoso_tp.html', {'nhanvien': nhanvien})
#
# from django.contrib.auth import authenticate, login
# from django.shortcuts import render, redirect
# from django import forms
#
# # ========== TRANG LOGIN ==========
# class LoginForm(forms.Form):
#     username = forms.CharField(label="Tên đăng nhập")
#     password = forms.CharField(label="Mật khẩu", widget=forms.PasswordInput)
#
# def login_view(request):
#     form = LoginForm(request.POST or None)
#     if request.method == 'POST' and form.is_valid():
#         username = form.cleaned_data['username']
#         password = form.cleaned_data['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('home')
#         else:
#             form.add_error(None, "Tên đăng nhập hoặc mật khẩu không đúng.")
#     return render(request, 'login.html', {'form': form})
#
# # ========== TRANG CHỦ ==========
# def dashboard_TP(request):
#     return render(request, 'trangchu_TP.html', {'active_page': 'home'})
# def dashboard_GD(request):
#     return render(request, 'trangchu_GD.html', {'active_page': 'home'})
# def dashboard_NV(request):
#     return render(request, 'trangchu_NV.html', {'active_page': 'home'})
# def dashboard_NVNS(request):
#     return render(request, 'trangchu_NVNS.html', {'active_page': 'home'})
#
# # ========== DANH SÁCH NHÂN VIÊN ==========
# def dsnv_nvns(request):
#     return render(request, "DSNV_NVNS.html", {'active_page': 'nhanvien'})
# def dsnv_tp(request):
#     return render(request, "DSNV_TP.html", {'active_page': 'nhanvien'})
# def dsnv_gd(request):
#     return render(request, "DSNV_GD.html", {'active_page': 'nhanvien'})
#
# # ========== TRANG CHI TIẾT HỒ SƠ NHÂN VIÊN ==========
# def chitiet_hoso_nvns(request):
#     return render(request, "chitiet_hoso_NVNS.html", {'active_page': 'nhanvien'})
# def chitiet_hoso_tp(request):
#     return render(request, "chitiet_hoso_TP.html", {'active_page': 'nhanvien'})
# def chitiet_hoso_gd(request):
#     return render(request, "chitiet_hoso_GD.html", {'active_page': 'nhanvien'})
