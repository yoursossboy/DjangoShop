# Generated by Django 5.1.3 on 2024-12-04 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
