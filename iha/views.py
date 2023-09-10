from datetime import datetime

from django.contrib import messages
from rest_framework import viewsets
from .forms import IHAEkleForm, IHAEditForm, KiralamaForm
from .models import IHA, Kiralama, KiralamaGecmisi
from .serializers import IHASerializer, KiralamaSerializer
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import IHA
from django.shortcuts import render, redirect
from django.contrib.auth import (
    authenticate,
    login,
    logout,
    get_user_model,
)
from .forms import UserLoginForm, UserRegisterForm


class IHAViewSet(viewsets.ModelViewSet):
    queryset = IHA.objects.all()
    serializer_class = IHASerializer


class KiralamaViewSet(viewsets.ModelViewSet):
    queryset = Kiralama.objects.all()
    serializer_class = KiralamaSerializer


@login_required(login_url='login')
def iha_rental(request, iha_id):
    if request.method == 'POST':
        # Kiralama bilgilerini formdan al
        baslangic_tarihi = request.POST.get('baslangic_tarihi')
        bitis_tarihi = request.POST.get('bitis_tarihi')

        # Tarih dizesini datetime nesnesine dönüştürme
        baslangic_tarihi = datetime.strptime(baslangic_tarihi, '%Y-%m-%dT%H:%M')
        bitis_tarihi = datetime.strptime(bitis_tarihi, '%Y-%m-%dT%H:%M')

        # Yeni bir tarih biçimi oluşturma
        baslangic_tarihi = baslangic_tarihi.strftime('%Y-%m-%d %H:%M')
        bitis_tarihi = bitis_tarihi.strftime('%Y-%m-%d %H:%M')

        try:
            # İHA'yı veritabanından al
            iha = IHA.objects.get(pk=iha_id)

            if iha.kiralama_durumu:
                # İHA zaten kiralanmışsa hata mesajı gönderin
                return JsonResponse({'message': 'Bu İHA zaten kiralanmış.'}, status=400)

            # Kiralama kaydını oluşturun ve kaydedin
            kiralama = Kiralama(iha=iha, kiralama_baslangic=baslangic_tarihi, kiralama_bitis=bitis_tarihi,
                                kiralayan=request.user)
            kiralama.save()

            # Kiralama başarılı mesajını ayarlayın
            messages.success(request, 'İHA kiralama işlemi başarıyla gerçekleştirildi.')
            return redirect('iha-lists')
        except IHA.DoesNotExist:
            # İHA bulunamadı hatası
            messages.error(request, 'İHA bulunamadı.')
            return redirect('iha-lists')

    return render(request, 'rental.html', {'iha_id': iha_id})

#kiralama iptali durumunda ve gerçekleşen kiralamaların kayıtları tutulacak
def finish_rental(request, kiralama_id):
    kiralama = get_object_or_404(Kiralama, id=kiralama_id)

    if not kiralama.iptal_edildi:
        kiralama.iptal_edildi = True
        kiralama.save()

        # Kiralama geçmişi oluştur
        KiralamaGecmisi.objects.create(
            iha=kiralama.iha,
            kiralama_baslangic=kiralama.kiralama_baslangic,
            kiralama_bitis=kiralama.kiralama_bitis,
            kiralayan=kiralama.kiralayan,
            iptal_edildi=True,
            gerceklesti=False
        )

    return redirect('kiralamalar')

@login_required(login_url='login')
def iha_lists(request):
    user = request.user
    iha_list = IHA.objects.all()
    return render(request, 'ihaLists.html', {'iha_list': iha_list})


@login_required(login_url='login')
def iha_details(request, iha_id):
    # iha_name = IHA.objects.get(id=iha_id)
    return render(request, 'ihaDetails.html', {'iha_id': iha_id})


def kiralama_sayfasi(request, iha_id):
    user_id = request.user.id if request.user.is_authenticated else None
    return render(request, 'rental.html', {'iha_id': iha_id, 'user_id': user_id})


# İHA İŞLEMLERİ HAKKINDA EDİT; DELETE ; LİST İŞLEMLERİ

def add_iha(request):
    if request.method == 'POST':
        form = IHAEkleForm(request.POST)
        if form.is_valid():
            # Form doğruysa, yeni bir IHA nesnesi oluşturun ve kaydedin
            yeni_iha = form.save()
            return redirect('iha-lists')
    else:
        form = IHAEkleForm()

    return render(request, 'add_iha.html', {'form': form})


def delete_iha(request, iha_id):
    iha = get_object_or_404(IHA, pk=iha_id)

    # İzin kontrolü yapılabilir
    if not request.user.is_authenticated:
        # Kullanıcı oturum açmamışsa işlemi engelle
        return redirect('login')  # Oturum açma sayfasına yönlendir

    # İzinleri geçtiyse İHA'yı sil
    iha.delete()

    return redirect('iha-lists')


def edit_iha(request, iha_id):
    iha = get_object_or_404(IHA, pk=iha_id)  # IHA nesnesini ID'ye göre alın

    if request.method == 'POST':
        form = IHAEditForm(request.POST,
                           instance=iha)  # POST verilerini ve mevcut IHA nesnesini kullanarak formu oluşturun
        if form.is_valid():
            form.save()
            return redirect(
                'iha-lists')  # IHA listesine yönlendirme (iha_list adında bir URL pattern'i oluşturmalısınız)
    else:
        form = IHAEditForm(instance=iha)  # Mevcut IHA nesnesini kullanarak formu oluşturun

    return render(request, 'edit_iha.html', {'form': form, 'iha': iha})


# KİRALAMA İŞLEMLERİ HAKKINDA EDİT; DELETE ; LİST İŞLEMLERİ

from django.shortcuts import redirect, render, get_object_or_404
from .models import Kiralama, KiralamaGecmisi

def delete_rental(request, kiralama_id):
    kiralama = get_object_or_404(Kiralama, id=kiralama_id)

    if request.method == 'POST':
        # Kiralama geçmişi oluştur
        KiralamaGecmisi.objects.create(
            iha=kiralama.iha,
            kiralama_baslangic=kiralama.kiralama_baslangic,
            kiralama_bitis=kiralama.kiralama_bitis,
            kiralayan=kiralama.kiralayan,
            iptal_edildi=True,
            gerceklesti=False
        )

        # İlgili IHA'nın kiralama durumunu False yap
        iha = kiralama.iha
        iha.kiralama_durumu = False
        iha.save()

        # Kiralamayı sil
        kiralama.delete()

        return JsonResponse({'message': 'Kiralama başarıyla iptal edildi'})

    return render(request, 'iha-lists.html', {'kiralama': kiralama})


def edit_rental(request, kiralama_id):
    kiralama = get_object_or_404(Kiralama, pk=kiralama_id)
    if request.method == 'POST':
        form = KiralamaForm(request.POST, instance=kiralama)
        if form.is_valid():
            form.save()
            return redirect('iha-lists')  # İHA listesine geri dön
    else:
        form = KiralamaForm(instance=kiralama)

    return render(request, 'edit_rental.html', {'form': form, 'kiralama': kiralama})


# Kullanıcının satın almalarını görüntüleme

def orders(request, user_id):
    # Kullanıcının kendi siparişlerini alın
    user_orders = Kiralama.objects.filter(kiralayan_id=user_id)
    return render(request, 'orders.html', {'kiralamalar': user_orders})

# iha kiralama işlemleri


def login_view(request):
    form1 = UserLoginForm(request.POST or None)
    if form1.is_valid():
        username = form1.cleaned_data.get("username")
        password = form1.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        if not request.user.is_staff:
            login(request, user)
            return redirect("/iha-lists/")
    return render(request, "login.html", {"form": form1, "title": "Login"})


def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Kayıt başarılıysa giriş sayfasına yönlendirme yapabilirsiniz
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

def logout_view(request):
    logout(request)
    return render(request, "ihaLists.html", {})

