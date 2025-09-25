# validator/views.py
import uuid
from pathlib import Path
from django.conf import settings
from django.shortcuts import render
from .forms import UploadFilesForm
from validator.validacion_report import run_validation


def upload_view(request):
    context = {}

    if request.method == 'POST':
        form = UploadFilesForm(request.POST, request.FILES)
        if form.is_valid():
            # Carpeta única por proceso
            run_id = uuid.uuid4().hex
            out_dir = Path(settings.MEDIA_ROOT) / 'processing' / run_id
            out_dir.mkdir(parents=True, exist_ok=True)

            # Guardar archivos subidos
            bruto_path = out_dir / request.FILES['bruto'].name
            with open(bruto_path, 'wb+') as dest:
                for chunk in request.FILES['bruto'].chunks():
                    dest.write(chunk)

            main_path = out_dir / request.FILES['main_pier'].name
            with open(main_path, 'wb+') as dest:
                for chunk in request.FILES['main_pier'].chunks():
                    dest.write(chunk)

            sus_path = out_dir / request.FILES['suscriptores'].name
            with open(sus_path, 'wb+') as dest:
                for chunk in request.FILES['suscriptores'].chunks():
                    dest.write(chunk)

            # Ejecutar validación
            try:
                outputs = run_validation(bruto_path, main_path, sus_path, out_dir=out_dir)
                media_url = settings.MEDIA_URL.rstrip('/')
                base_web = f"{media_url}/processing/{run_id}"

                context['download_links'] = {
                    'validos_xlsx': f"{base_web}/validos.xlsx",
                    'rechazados_xlsx': f"{base_web}/rechazados.xlsx",
                    'validos_csv': f"{base_web}/validos.csv",
                    'rechazados_csv': f"{base_web}/rechazados.csv",
                    'pdf': f"{base_web}/reporte_validacion.pdf",
                }
                context['success'] = True
            except Exception as e:
                context['error'] = str(e)

            context['form'] = form
            return render(request, 'validator/upload.html', context)

        else:
            context['form'] = form
            return render(request, 'validator/upload.html', context)

    else:
        # GET
        form = UploadFilesForm()
        context['form'] = form
        return render(request, 'validator/upload.html', context)
