# Generated by Django 4.0.3 on 2022-04-09 07:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Iteam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=13)),
            ],
        ),
        migrations.CreateModel(
            name='Sub_Iteam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subiteam_name', models.CharField(max_length=20)),
                ('price', models.IntegerField(max_length=25)),
                ('main_iteam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.iteam')),
            ],
        ),
    ]
