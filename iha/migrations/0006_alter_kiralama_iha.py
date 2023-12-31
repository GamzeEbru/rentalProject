# Generated by Django 4.2.5 on 2023-09-09 22:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("iha", "0005_iha_kiralama_durumu"),
    ]

    operations = [
        migrations.AlterField(
            model_name="kiralama",
            name="iha",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="kiralama",
                to="iha.iha",
            ),
        ),
    ]
