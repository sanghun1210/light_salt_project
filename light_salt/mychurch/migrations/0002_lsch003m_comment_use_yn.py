# Generated by Django 2.0.5 on 2018-06-18 02:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mychurch', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lsch003m',
            name='comment_use_yn',
            field=models.CharField(default='Y', max_length=20),
        ),
    ]