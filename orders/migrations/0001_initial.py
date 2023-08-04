# Generated by Django 4.2.3 on 2023-08-04 20:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_paid', models.BooleanField(default=False, verbose_name='Is it Paid?')),
                ('first_name', models.CharField(max_length=100, verbose_name='First Name')),
                ('last_name', models.CharField(max_length=100, verbose_name='Last Name')),
                ('phone_number', models.CharField(max_length=15, verbose_name='Phone Number')),
                ('address', models.CharField(max_length=700, verbose_name='Address')),
                ('order_notes', models.CharField(blank=True, max_length=700)),
                ('datetime_created', models.DateTimeField(auto_now_add=True, verbose_name='datetime_created')),
                ('datetime_modified', models.DateTimeField(auto_now=True, verbose_name='datetime_modified')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
