# Generated by Django 4.2.5 on 2023-09-09 14:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("iha", "0003_alter_kiralama_kiralama_baslangic_saati_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="kiralama",
            old_name="kiralama_baslangic_saati",
            new_name="kiralama_baslangic",
        ),
        migrations.RenameField(
            model_name="kiralama",
            old_name="kiralama_bitis_saati",
            new_name="kiralama_bitis",
        ),
        migrations.RemoveField(
            model_name="kiralama",
            name="tarih",
        ),
    ]
