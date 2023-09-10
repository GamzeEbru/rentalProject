from django.contrib import admin
from .models import IHA, Kiralama, KiralamaGecmisi


@admin.register(IHA)
class IHAAdmin(admin.ModelAdmin):
    list_display = ('id','marka', 'model', 'agirlik', 'kategori', 'kiralama_durumu')


@admin.register(Kiralama)
class KiralamaAdmin(admin.ModelAdmin):
    list_display = ('id','kiralama_baslangic', 'kiralama_bitis', 'iha', 'kiralayan')


@admin.register(KiralamaGecmisi)
class KiralamaGecmisi(admin.ModelAdmin):
    list_display = ('id','iha', 'kiralama_baslangic', 'kiralama_bitis', 'kiralayan', 'iptal_edildi','gerceklesti')
