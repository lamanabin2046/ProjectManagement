from django.urls import path
from .import views
from . import views_budget, views_deductions, views_guarantees, views_outputs, views_sectors
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    
    path('add/', views.add_project, name='add_project'),
    path('view_projects/', views.view_projects, name='view_projects'),
    path('edit_project/<int:id>/', views.edit_project, name='edit_project'),
    path('import_excel/', views.import_excel, name='import_excel'),
    path('update_project/', views.update_project, name='update_project'),
    path('delete/<int:pk>/', views.delete_project, name='delete_project'),
    path('project-timeline/<int:project_id>/', views.project_timeline, name='project_timeline'),
    path('<int:project_id>/outputs/', views_outputs.project_outputs, name='project_outputs'),
    path('Reports/Outputs/', views_outputs.outputs_report, name='outputs_report'),
    path('Settings/Outputs/', views_outputs.output_settings, name='output_settings'),
    path('Settings/Sectors/', views_sectors.sector_settings, name='sector_settings'),

    # ================= सेटिङ — लुकअप व्यवस्थापन =================
    path('Settings/FiscalYear/', views.manage_fiscal_years, name='manage_fiscal_years'),
    path('Settings/FiscalYear/Edit/<int:id>/', views.edit_fiscal_year, name='edit_fiscal_year'),
    path('Settings/FiscalYear/Delete/<int:id>/', views.delete_fiscal_year, name='delete_fiscal_year'),

    path('Settings/BudgetType/', views.manage_budget_types, name='manage_budget_types'),
    path('Settings/BudgetType/Edit/<int:id>/', views.edit_budget_type, name='edit_budget_type'),
    path('Settings/BudgetType/Delete/<int:id>/', views.delete_budget_type, name='delete_budget_type'),

    path('Settings/ProcurementType/', views.manage_procurement_types, name='manage_procurement_types'),
    path('Settings/ProcurementType/Edit/<int:id>/', views.edit_procurement_type, name='edit_procurement_type'),
    path('Settings/ProcurementType/Delete/<int:id>/', views.delete_procurement_type, name='delete_procurement_type'),
    # ================= कर तथा धरौटी कट्टी / धरौटी फिर्ता =================
    path('Reports/Deductions/', views_deductions.deduction_register, name='deduction_register'),
    path('Retention/', views_deductions.retention_list, name='retention_list'),
    path('Retention/<int:project_id>/recommend/', views_deductions.retention_recommend, name='retention_recommend'),
    path('Retention/<int:project_id>/tippani/', views_deductions.retention_tippani, name='retention_tippani'),
    path('Retention/<int:project_id>/release/', views_deductions.retention_release, name='retention_release'),
    # ================= बजेट नियन्त्रण =================
    path('Budget/', views_budget.budget_status, name='budget_status'),
    path('Budget/Heads/', views_budget.budget_heads, name='budget_heads'),
    path('Budget/Amendments/', views_budget.amendments, name='budget_amendments'),
    path('Budget/Amendments/new/', views_budget.amendment_new, name='budget_amendment_new'),
    # ================= बैंक ग्यारेन्टी =================
    path('Guarantees/Performance/', views_guarantees.performance_guarantees, name='performance_guarantees'),
    path('Guarantees/Advance/', views_guarantees.advance_guarantees, name='advance_guarantees'),
]