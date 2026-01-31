from django.urls import path
from . import views

urlpatterns = [
    path('', views.PatientListCreateView.as_view(), name='patient_list_create'),
    path('stats/', views.patient_stats_view, name='patient_stats'),
    path('search/', views.patient_search_view, name='patient_search'),
    # Vues HTML (AVANT l'API)
    path('<int:patient_id>/view/', views.view_patient, name='view_patient'),
    path('<int:patient_id>/edit/', views.edit_patient, name='edit_patient'),
    path('<int:patient_id>/delete/', views.delete_patient, name='delete_patient'),
    # API REST (à la fin)
    path('<int:pk>/', views.PatientDetailView.as_view(), name='patient_detail'),
]
