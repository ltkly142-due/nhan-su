from django.urls import path
from .views import (login_view, dangnhap_sai, taikhoan_bikhoa,
                    dashboard_TP, dashboard_GD, dashboard_NV, dashboard_NVNS,
                    dsnv_nvns, dsnv_tp, dsnv_gd,
                    chitiet_hoso_nvns, chitiet_hoso_tp, chitiet_hoso_gd,
                    add_hoso, edit_hoso, delete_hoso,
                    qlhd_tp, qlhd_nvns,
                    them_hopdong, chinhsua_hopdong, chitiet_hopdong, xoa_hopdong)

urlpatterns = [
    path('login/', login_view, name='login'),
    path('login/erro', dangnhap_sai, name='dangnhap_sai'),
    path('login/key', taikhoan_bikhoa, name='taikhoan_bikhoa'),
    path('TP/', dashboard_TP, name='TP_dashboard'),
    path('GD/', dashboard_GD, name='GD_dashboard'),
    path('NV/', dashboard_NV, name='NV_dashboard'),
    path('NVNS/', dashboard_NVNS, name='NVNS_dashboard'),

    path('NVNS/danhsach/', dsnv_nvns, name='NVNS_dsnv'),
    path('TP/danhsach/', dsnv_tp, name='TP_dsnv'),
    path('GD/danhsach/', dsnv_gd, name='GD_dsnv'),

    # path('nhanvien/<str:ma_nv>/', chitiet_hoso_nvns, name='chitiet_hoso_nvns'),
    path('NVNS/hoso/', chitiet_hoso_nvns, name='chitiet_hoso_nvns'),
    path('TP/hoso/', chitiet_hoso_tp, name='chitiet_hoso_tp'),
    path('GD/hoso/', chitiet_hoso_gd, name='chitiet_hoso_gd'),

    path('NVNS/add/', add_hoso, name='add_hoso'),
    path('NVNS/edit/', edit_hoso, name='edit_hoso'),

    path('NVNS/delete/', delete_hoso, name='delete_hoso'),

    path('TP/hopdong/', qlhd_tp, name='qlhd_tp'),
    path('NVNS/hopdong/', qlhd_nvns, name='qlhd_nvns'),

    path('NVNS/hopdong/them/', them_hopdong, name='them_hopdong'),
    path('NVNS/hopdong/sua/', chinhsua_hopdong, name='chinhsua_hopdong'),
    path('NVNS/hopdong/chitiet/', chitiet_hopdong, name='chitiet_hopdong'),
    path('NVNS/hopdong/xoa/', xoa_hopdong, name='xoa_hopdong'),

    # path('nhanvien/<str:ma_nv>/delete/', delete_hoso, name='delete_hoso'),

    # path('NVNS/hoso/<int:id>/', chitiet_hoso_nvns, name='chitiet_hoso_nvns'),
    # path('TP/hoso/<int:id>/', chitiet_hoso_tp, name='chitiet_hoso_tp'),
    # path('GD/hoso/<int:id>/', chitiet_hoso_gd, name='chitiet_hoso_gd'),
]
