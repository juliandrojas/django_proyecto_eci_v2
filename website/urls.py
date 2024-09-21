# urls.py
from django.urls import path, register_converter
from .views import renderIndex, renderDocuments, download_file, upload_file
from .converters import FileNameConverter

# Registrar el convertidor personalizado
register_converter(FileNameConverter, 'filename')

urlpatterns = [
    path('', renderIndex, name='index'),
    path('documents/<int:category_id>/', renderDocuments, name='render_documents'),
    path('upload/', upload_file, name='upload_file'),
    path('download/<int:id>/', download_file, name='download_file'),
]
