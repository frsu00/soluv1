# Generated by Django 3.2.3 on 2021-06-08 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_alter_pedido_fechaentrega'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detallepedido',
            name='cantidad',
            field=models.IntegerField(null=True),
        ),
    ]