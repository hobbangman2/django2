# Generated by Django 3.1.4 on 2021-01-03 06:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_auto_20210103_1420'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookinstance',
            options={'ordering': ['due_back'], 'permissions': [('can_mark_returned', 'set book as returned')]},
        ),
    ]