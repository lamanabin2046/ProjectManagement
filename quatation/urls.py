
from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('Add/Suchi/add_suchikrit_list', views.ADD_SUCHIKRIT_LIST,name='add_suchikrit_list'),
    path('View/Suchi/view_suchikrit_list', views.VIEW_SUCHIKRIT_LIST,name='view_suchikrit_list'),
    path('Invite/Quation', views.INVITE_QUATATION,name='invite_quatation'),
    path('Invite/Quatation/Project', views.VIEW_QUATATION_PROJECTS,name='view_quatation_projects'),
    path('View/All/Project', views.VIEW_QUATATION_ALL_PROJECTS,name='view_quatation_all_projects'),
    path('Add/Quatation/Amount/<str:id>', views.ADD_QUATATION_AMOUNT,name='add_quatation_amount'),
    path('Print/Quatation/<str:id>', views.PRINT_QUATATION_TIPPANI,name='print_quatation_tippani'),
    path('Send/Letter/<str:id>', views.SEND_QUATATION_LETTER,name='send_quatation_letter'),
    path('Approved/Tippani/<str:id>', views.APPROVED_QUATATION_TIPPANI,name='approved_quatation_tippani'),
    path('Add/Agreement/<str:id>', views.ADD_QUATATION_AGREEMENT,name='add_quatation_agreement'),
    path('Print/Agreement/<str:id>', views.PRINT_QUATATION_AGREEMENT,name='print_quatation_agreement'),
    path('Print/Work/Order/<str:id>', views.PRINT_QUATATION_WORK_ORDE,name='print_quatation_work_order'),
    path('Add/Final/Payment/<str:id>', views.ADD_QUATATION_FINAL_PAYMENT,name='add_quatation_final_payment'),
    path('Add/Final/Payments/', views.ADD_QUATATION_FINAL_PAYMENT_SIDEBAR,name='add_quatation_final_payment_sidebar'),
    path('View/Final/Payments/', views.VIEW_QUATATION_FINAL_PAYMENT_SIDEBAR,name='view_quatation_final_payment_sidebar'),
    path('Print/Final/Payments/Tippani/<str:id>', views.PRINT_QUATATION_FINAL_PAYMENT_TIPPANI,name='print_quatation_final_payment_tippani'),
    
]



