# Generated by Django 3.2.4 on 2021-08-06 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Books', '0004_alter_orderplaced_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='sub_category',
            field=models.CharField(choices=[('AA', 'Action_and_Adventure'), ('C', 'Classics'), ('CG', 'Comic_Book_or_Graphic_Novel'), ('DM', 'Detective_and_Mystery'), ('F', 'Fantasy'), ('HF', 'Historical Fiction'), ('H', 'Horror'), ('LF', 'Literary_Fiction')], default='0000000', max_length=2),
        ),
        migrations.AlterField(
            model_name='orderplaced',
            name='status',
            field=models.CharField(choices=[('Packed', 'Packed'), ('Delivered', 'Delivered'), ('Cancel', 'Cancel'), ('Accepted', 'Accepted'), ('On the way', 'On the way')], default='Pending', max_length=50),
        ),
    ]
