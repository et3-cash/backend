# Generated by Django 5.1.1 on 2024-10-27 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0005_rename_date_transaction_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otp',
            name='phone_number',
            field=models.CharField(max_length=15),
        ),
    ]
