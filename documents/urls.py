from django.urls import path
from . import views

urlpatterns = [
    path('', views.DocumentListCreateView.as_view(), name='document_list_create'),
    path('stats/', views.document_stats_view, name='document_stats'),
    path('search/', views.document_search_view, name='document_search'),
    # Vue HTML pour voir un document (AVANT l'API)
    path('<int:document_id>/view/', views.view_document, name='view_document'),
    path('<int:document_id>/edit/', views.edit_document, name='edit_document'),
    path('<int:document_id>/delete/', views.delete_document, name='delete_document'),
    path('<int:document_id>/download/', views.download_document, name='download_document'),
    # API REST (à la fin)
    path('<int:pk>/', views.DocumentDetailView.as_view(), name='document_detail'),
]
