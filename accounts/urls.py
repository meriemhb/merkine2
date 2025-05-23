from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/delete/', views.delete_profile, name='delete_profile'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('signup/vendor/', views.signup_vendor, name='signup_vendor'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-users/', views.admin_users, name='admin_users'),
    path('admin-users/delete/<int:user_id>/', views.admin_user_delete, name='admin_user_delete'),
    path('admin-stats/', views.admin_stats, name='admin_stats'),
    path('patient/dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('patient/publications/', views.kine_publications, name='kine_publications'),
    path('patient/message-kine/', views.patient_message_kine, name='patient_message_kine'),
    path('patient/shop/', views.patient_shop, name='patient_shop'),
    path('patient/search-kine/', views.search_kine, name='search_kine'),
    path('patient/demande-prise-en-charge/', views.demande_prise_en_charge_form, name='demande_prise_en_charge_form'),
    path('patient/demande-prise-en-charge/<int:kine_id>/', views.demande_prise_en_charge, name='demande_prise_en_charge'),
    path('kine/dashboard/', views.kine_dashboard, name='kine_dashboard'),
    path('kine/publications/', views.kine_publications_manage, name='kine_publications_manage'),
    path('kine/messages/', views.kine_messages, name='kine_messages'),
    path('kine/demandes/', views.kine_demandes, name='kine_demandes'),
    path('kine/profile/', views.kine_profile, name='kine_profile'),
    path('profil-vendeur/', views.profile_vendor, name='profile_vendor'),
] 