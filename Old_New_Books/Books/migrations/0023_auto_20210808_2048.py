# Generated by Django 3.2.4 on 2021-08-08 15:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Books', '0022_alter_orderplaced_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='username',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Books.customer'),
        ),
        migrations.AlterField(
            model_name='orderplaced',
            name='status',
            field=models.CharField(choices=[('Cancel', 'Cancel'), ('Accepted', 'Accepted'), ('Packed', 'Packed'), ('On the way', 'On the way'), ('Delivered', 'Delivered')], default='Pending', max_length=50),
        ),
    ]