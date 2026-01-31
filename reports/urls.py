from django.urls import path
from . import views

urlpatterns = [
    path('', views.ReportListCreateView.as_view(), name='report_list_create'),
    path('stats/', views.report_stats_view, name='report_stats'),
    path('search/', views.report_search_view, name='report_search'),
    # URL frontend pour ajouter un rapport
    path('report/add/', views.report_add_view, name='report_add'),
    # URLs pour voir, éditer et supprimer (AVANT l'API pour éviter les conflits)
    path('<int:report_id>/view/', views.view_report, name='view_report'),
    path('<int:report_id>/edit/', views.edit_report, name='edit_report'),
    path('<int:report_id>/delete/', views.delete_report, name='delete_report'),
    # Export PDF
    path('<int:report_id>/export-pdf/', views.export_report_pdf, name='export_report_pdf'),
    path('export-list-pdf/', views.export_reports_list_pdf, name='export_reports_list_pdf'),
    # API REST (doit être à la fin)
    path('<int:pk>/', views.ReportDetailView.as_view(), name='report_detail'),
]
