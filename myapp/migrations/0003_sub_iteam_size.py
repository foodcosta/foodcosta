# Generated by Django 4.0.3 on 2022-04-11 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_iteam_sub_iteam'),
    ]

    operations = [
        migrations.AddField(
            model_name='sub_iteam',
            name='size',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]