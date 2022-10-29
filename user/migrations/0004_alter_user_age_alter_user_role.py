# Generated by Django 4.1.2 on 2022-10-28 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_user_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='age',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('admin', 'Администратор'), ('moderator', 'Модератор'), ('member', 'Участник')], default='member', max_length=20),
        ),
    ]
