# views.py
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .models import Upload, User, Categories, Upload
from django.http import FileResponse, HttpResponseBadRequest, Http404, HttpResponse
from datetime import datetime
from urllib.parse import unquote
from .converters import FileNameConverter
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import Upload, Categories
from django.shortcuts import get_object_or_404
from django.http import HttpResponseNotFound


def renderIndex(request):
    users = User.objects.all()
    categories = Categories.objects.all()
    files = Upload.objects.all()
    return render(request, 'index.html', { 
        'users' : users, 
        'categories' : categories ,
        'files': files,
    })

def renderDocuments(request, category_id):
    try:
        category = get_object_or_404(Categories, id=category_id)
        documents = Upload.objects.filter(category=category)
        return render(request, 'documents.html', {
            'documents': documents,
            'category_name': category.name
        })
    except Categories.DoesNotExist:
        return render(request, 'error.html', {'message': 'Categoria no encontrada'})

def upload_file(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        if file:
            # Validar el formato del archivo
            allowed_extensions = ['pdf']
            extension = file.name.split('.')[-1].lower()
            if extension not in allowed_extensions:
                raise ValidationError(_('Solo se admiten archivos PDF.'))

            # Crear un nuevo registro en el modelo Upload
            try:
                category_id = request.POST.get('category')
                category = Categories.objects.get(id=category_id)
            except Categories.DoesNotExist:
                return HttpResponse("Categoria no encontrada.")

            nuevo_upload = Upload.objects.create(
                file_name=file.name,
                file_path=file,
                uploaded_at=datetime.now(),
                category=category
            )

            # return HttpResponse(f"Archivo {nuevo_upload.file_name} subido exitosamente")
            return redirect('index')
        else:
            return HttpResponse("No se ha seleccionado ningún archivo.")
    return render(request, 'index.html')

def download_file(request, id):
    try:
        upload = get_object_or_404(Upload, pk=id)
        
        # Abrir el archivo y enviarlo como respuesta
        with open(upload.file_path.path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename={upload.file_name}'
        
        return response
    except Upload.DoesNotExist:
        return HttpResponseNotFound('Archivo no encontrado')