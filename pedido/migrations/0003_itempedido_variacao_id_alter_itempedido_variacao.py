# Generated by Django 4.0 on 2022-03-03 22:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedido', '0002_pedido_qtd_total'),
    ]

    operations = [
        migrations.AddField(
            model_name='itempedido',
            name='variacao_id',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='itempedido',
            name='variacao',
            field=models.CharField(max_length=255),
        ),
    ]
