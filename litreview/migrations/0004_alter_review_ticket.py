# Generated by Django 3.2.5 on 2021-08-03 21:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('litreview', '0003_alter_ticket_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='ticket',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='review', to='litreview.ticket'),
        ),
    ]