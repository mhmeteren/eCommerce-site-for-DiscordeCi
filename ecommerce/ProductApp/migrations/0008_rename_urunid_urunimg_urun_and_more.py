# Generated by Django 4.1.3 on 2022-12-12 13:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ProductApp', '0007_rename_altkategoriid_urun_altkategori_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='urunimg',
            old_name='UrunID',
            new_name='Urun',
        ),
        migrations.RenameField(
            model_name='urunozellik',
            old_name='UrunID',
            new_name='Urun',
        ),
    ]