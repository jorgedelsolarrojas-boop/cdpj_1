from django.db import models


class UploadSet(models.Model):
    creado = models.DateTimeField(auto_now_add=True)
    bruto = models.FileField(upload_to='uploads/', null=True, blank=True)
    suscriptores = models.FileField(upload_to='uploads/', null=True, blank=True)
    main_pier = models.FileField(upload_to='uploads/', null=True, blank=True)
    processed = models.BooleanField(default=False)


    def __str__(self):
        return f"UploadSet {self.id} - {self.creado}"