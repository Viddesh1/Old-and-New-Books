# Generated by Django 3.2.4 on 2021-08-06 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Books', '0002_alter_orderplaced_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderplaced',
            name='status',
            field=models.CharField(choices=[('Cancel', 'Cancel'), ('Delivered', 'Delivered'), ('On the way', 'On the way'), ('Accepted', 'Accepted'), ('Packed', 'Packed')], default='Pending', max_length=50),
        ),
    ]
