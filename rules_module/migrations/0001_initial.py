# Generated by Django 4.0.6 on 2023-04-29 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='rulesModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='نام قانون')),
                ('description', models.CharField(max_length=300, verbose_name='توضیخ')),
                ('is_show', models.BooleanField(default=True, verbose_name='نمایش داده شود / نشود')),
            ],
        ),
    ]
