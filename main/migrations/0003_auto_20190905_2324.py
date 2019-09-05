# Generated by Django 2.2.5 on 2019-09-05 15:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('main', '0002_auto_20190904_1806'),
    ]
    
    operations = [
        migrations.CreateModel(
            name='KeyWord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.TextField()),
                ('idf', models.FloatField()),
            ],
        ),
        migrations.AddField(
            model_name='newspage',
            name='body_key_mod',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='newspage',
            name='title_key_mod',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='newspage',
            name='keywords',
            field=models.ManyToManyField(to='main.KeyWord'),
        ),
    ]