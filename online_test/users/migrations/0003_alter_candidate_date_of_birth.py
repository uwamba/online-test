# Generated by Django 5.1.4 on 2024-12-06 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_candidate_options_alter_candidate_managers_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='date_of_birth',
            field=models.DateField(null=True),
        ),
    ]
