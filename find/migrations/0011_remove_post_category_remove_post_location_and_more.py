# Generated by Django 4.2.7 on 2023-11-28 01:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('find', '0010_delete_findcomment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='category',
        ),
        migrations.RemoveField(
            model_name='post',
            name='location',
        ),
        migrations.DeleteModel(
            name='FindCategory',
        ),
        migrations.DeleteModel(
            name='FindLocation',
        ),
    ]
