# Generated by Django 2.2.5 on 2019-09-06 03:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('main', '0003_auto_20190905_2324'),
    ]
    
    operations = [
        migrations.AlterField(
            model_name='keyword',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
