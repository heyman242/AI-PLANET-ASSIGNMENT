# Generated by Django 4.2.2 on 2023-06-21 15:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hackathon_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hackathon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('background_image', models.ImageField(upload_to='hackathon/images')),
                ('hackathon_image', models.ImageField(upload_to='hackathon/images')),
                ('submission_type', models.CharField(choices=[('image', 'Image'), ('file', 'File'), ('link', 'Link')], max_length=10)),
                ('start_datetime', models.DateTimeField()),
                ('end_datetime', models.DateTimeField()),
                ('reward_prize', models.DecimalField(decimal_places=2, max_digits=8)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
