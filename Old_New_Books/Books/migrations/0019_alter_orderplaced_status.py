# Generated by Django 3.2.4 on 2021-08-07 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Books', '0018_alter_orderplaced_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderplaced',
            name='status',
            field=models.CharField(choices=[('Packed', 'Packed'), ('On the way', 'On the way'), ('Accepted', 'Accepted'), ('Cancel', 'Cancel'), ('Delivered', 'Delivered')], default='Pending', max_length=50),
        ),
    ]
