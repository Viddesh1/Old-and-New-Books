# Generated by Django 3.2.4 on 2021-08-08 15:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Books', '0020_alter_orderplaced_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='username',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Books.customer'),
        ),
        migrations.AlterField(
            model_name='orderplaced',
            name='status',
            field=models.CharField(choices=[('Delivered', 'Delivered'), ('Accepted', 'Accepted'), ('Cancel', 'Cancel'), ('On the way', 'On the way'), ('Packed', 'Packed')], default='Pending', max_length=50),
        ),
    ]