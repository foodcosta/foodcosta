# Generated by Django 4.0.3 on 2022-04-12 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_item_sub_item_remove_sub_iteam_main_iteam_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sub_item',
            name='price',
            field=models.IntegerField(),
        ),
    ]
