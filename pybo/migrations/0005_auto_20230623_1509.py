# Generated by Django 3.1.3 on 2023-06-23 06:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pybo', '0004_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='user_address',
            new_name='address',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='user_email',
            new_name='email',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='user_name',
            new_name='nickname',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='user_pw',
            new_name='password',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='user_phone',
            new_name='phone',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='user_id',
            new_name='username',
        ),
    ]
