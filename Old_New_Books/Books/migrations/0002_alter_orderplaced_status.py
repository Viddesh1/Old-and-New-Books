# Generated by Django 3.2.4 on 2021-08-06 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Books', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderplaced',
            name='status',
            field=models.CharField(choices=[('Cancel', 'Cancel'), ('Delivered', 'Delivered'), ('Accepted', 'Accepted'), ('Packed', 'Packed'), ('On the way', 'On the way')], default='Pending', max_length=50),
        ),
    ]
