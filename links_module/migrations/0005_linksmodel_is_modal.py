# Generated by Django 4.0.6 on 2023-04-28 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('links_module', '0004_linksmodel_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='linksmodel',
            name='is_modal',
            field=models.BooleanField(default=False, verbose_name='نمایش به صورت مدال'),
        ),
    ]
