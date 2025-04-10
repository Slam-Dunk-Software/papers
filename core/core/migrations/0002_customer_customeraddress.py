# Generated by Django 4.2.20 on 2025-04-07 00:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('note', models.TextField(blank=True, null=True)),
                ('state', models.CharField(choices=[('disabled', 'Disabled'), ('enabled', 'Enabled'), ('other', 'Other')], default='enabled', max_length=50)),
                ('currency', models.CharField(max_length=10)),
                ('tax_exempt', models.BooleanField(default=False)),
                ('verified_email', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='CustomerAddress',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False, unique=True)),
                ('address1', models.CharField(max_length=255)),
                ('address2', models.CharField(blank=True, max_length=255, null=True)),
                ('city', models.CharField(max_length=100)),
                ('province', models.CharField(max_length=100)),
                ('zip', models.CharField(max_length=20)),
                ('country', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=200)),
                ('default', models.BooleanField(default=False)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='addresses', to='core.customer')),
            ],
        ),
    ]
