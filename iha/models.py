from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class IHA(models.Model):
    marka = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    agirlik = models.FloatField()
    kategori = models.CharField(max_length=50)
    kiralama_durumu = models.BooleanField(default=False)

    def __str__(self):
        return self.marka


class KiralamaGecmisi(models.Model):
    iha = models.ForeignKey(IHA, on_delete=models.CASCADE)
    kiralama_baslangic = models.DateTimeField()
    kiralama_bitis = models.DateTimeField()
    kiralayan = models.ForeignKey(User, on_delete=models.CASCADE)
    iptal_edildi = models.BooleanField(default=False)
    gerceklesti = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.kiralayan.username} tarafından {self.iha.marka} kiralama geçmişi"


class Kiralama(models.Model):
    iha = models.OneToOneField(IHA, on_delete=models.CASCADE, related_name='kiralama', null=True, blank=True)
    kiralama_baslangic = models.DateTimeField()
    kiralama_bitis = models.DateTimeField()
    kiralayan = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.iha.kiralama_durumu:
            raise ValidationError("Bu IHA cihazı zaten kiralama işlemine sahip.")
        super(Kiralama, self).save(*args, **kwargs)
        self.iha.kiralama_durumu = True
        self.iha.save()

    def __str__(self):
        return f"{self.kiralayan.username} tarafından {self.iha.marka} kiralama"

    def iptal_et(self):
        # Kiralama iptal edildiğinde burada işlemleri gerçekleştirin
        self.iptal_edildi = True
        self.save()

        # Kiralama geçmişi oluştur
        KiralamaGecmisi.objects.create(
            iha=self.iha,
            kiralama_baslangic=self.kiralama_baslangic,
            kiralama_bitis=self.kiralama_bitis,
            kiralayan=self.kiralayan,
            iptal_edildi=True,
            gerceklesti=False
        )
