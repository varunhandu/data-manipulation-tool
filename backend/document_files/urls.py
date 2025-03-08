from django.urls import path, include
from .views import UploadDocumentView, DownloadDocumentView, DeleteDocumentView, DocumentListView
from .views_pandas import CreateDataframe, DownloadDataframe

urlpatterns = [
    path('upload/', UploadDocumentView.as_view(), name='upload_document'),
    path('download/<int:pk>/', DownloadDocumentView.as_view(), name='download_document'),
    path('delete/<int:pk>/', DeleteDocumentView.as_view(), name='delete_document'),
    path('dataframe/create/<int:pk>/', CreateDataframe.as_view(), name='create_dataframe'),
    path('dataframe/download/', DownloadDataframe.as_view(), name='download_dataframe'),
    path('', DocumentListView.as_view(), name='see_document')
]