# Generated by Django 4.2.6 on 2023-12-09 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('mobile_number', models.CharField(max_length=13)),
                ('user_id', models.CharField(max_length=13)),
            ],
        ),
    ]
