from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
   path('Project/Bid/Detail', views.ADD_BID_DETAIL,name='add_bid_detail'),
   path('print_asay_notice/<int:id>/', views.print_asay_notice, name='print_asay_notice'),
   path('View/Bid/Detail', views.VIEW_BID_DETAIL,name='view_bid_detail'),
   path('add_pg_requirement/<int:id>/', views.ADD_PG_REQUIREMENT, name='add_pg_requirement'),
   path('view_approved_projects', views.view_approved_projects, name='view_approved_projects'),
   path('print_contract_tippani/<int:id>/', views.print_contract_tippani, name='print_contract_tippani'),
   path('print_contract_invite/<int:id>/', views.print_contract_invite, name='print_contract_invite'),
   path('add_pg_bank_detail/<int:bidding_id>/', views.add_pg_bank_detail, name='add_pg_bank_detail'),
   path('Project/View/Agreement/Projects', views.view_agreement_projects,name='view_agreement_projects'),
   path('print_contract_paper/<int:id>/', views.print_contract_paper, name='print_contract_paper'),
   path('print_bid_work_order/<int:id>/', views.print_bid_work_order, name='print_bid_work_order'),
   path('Project/Advance/Payment/Add', views.add_advance_payment, name='add_advance_payment'),
   path('print_advance_tippani/<int:id>/', views.print_advance_tippani, name='print_advance_tippani'),
   path("get-sealed-bid-contract-info/<int:sealed_bid_id>/",views.get_sealed_bid_contract_info,name="get_sealed_bid_contract_info"),
   path('view_performance_bank_guarantees', views.view_performance_bank_guarantees, name='view_performance_bank_guarantees'),
   path("performance-bond/extend/<int:id>/",views.extend_performance_bond,name="extend_performance_bond"),
   path("performance-bond/extend/update/",views.update_performance_bond_expiry,name="update_performance_bond_expiry"),
   path("print_performance_bond_tippani/<int:id>/",views.print_performance_bond_tippani,name="print_performance_bond_tippani"), 
   path('view_advance_bank_guarantees', views.view_advance_bank_guarantees, name='view_advance_bank_guarantees'),
   path('view_advance_bank_guarantees', views.view_advance_bank_guarantees, name='view_advance_bank_guarantees'),
   
   path('Project/Final/Payment/Add', views.add_final_payment, name='add_final_payment'),
   path('print_final_tippani/<int:id>/', views.print_final_tippani, name='print_final_tippani'),
   path("running-evaluation/add/",views.add_running_evaluation,name="add_running_evaluation"),
   path("print_running_tippani/<int:id>/", views.print_running_tippani, name="print_running_tippani"),
   path('view_advance_payment', views.view_advance_payment, name='view_advance_payment'),
   path('view_running_evaluations', views.view_running_evaluations, name='view_running_evaluations'),
   path("final-payments/",views.view_final_payment, name="view_final_payment"),
]