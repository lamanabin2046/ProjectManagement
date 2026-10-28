from django.urls import path
from .import views
from . import views_outputs
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
]