# Generated by Django 3.2.3 on 2021-06-08 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_alter_detallepedido_cantidad'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detallepedido',
            name='subtotal',
            field=models.FloatField(null=True),
        ),
    ]