# Generated by Django 4.1.2 on 2022-11-04 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_user_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='location',
            field=models.ManyToManyField(related_name='rel_skills', to='user.location', verbose_name='Location list'),
        ),
    ]
