# validator/forms.py
from django import forms


class UploadFilesForm(forms.Form):
    bruto = forms.FileField(label='Documento a filtrar (bruto)', required=True)
    main_pier = forms.FileField(label='Documento MAIN PIER', required=True)
    suscriptores = forms.FileField(label='Documento SUSCRIPTORES PIER', required=True)


def clean(self):
    cleaned = super().clean()
    for fkey in ['bruto', 'main_pier', 'suscriptores']:
        f = cleaned.get(fkey)
        if f:
            if f.size > 5 * 1024 * 1024:
                raise forms.ValidationError(f"El archivo {fkey} supera 5MB")
    return cleaned