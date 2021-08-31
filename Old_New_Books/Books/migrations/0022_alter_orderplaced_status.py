# Generated by Django 3.2.4 on 2021-08-08 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Books', '0021_auto_20210808_2045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderplaced',
            name='status',
            field=models.CharField(choices=[('On the way', 'On the way'), ('Accepted', 'Accepted'), ('Cancel', 'Cancel'), ('Delivered', 'Delivered'), ('Packed', 'Packed')], default='Pending', max_length=50),
        ),
    ]
