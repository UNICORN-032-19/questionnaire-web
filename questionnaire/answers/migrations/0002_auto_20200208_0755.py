# Generated by Django 3.0.2 on 2020-02-08 07:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('answers', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='answers',
            old_name='quiestion_id',
            new_name='question_id',
        ),
    ]
