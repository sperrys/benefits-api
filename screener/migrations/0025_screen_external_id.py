# Generated by Django 4.0.5 on 2022-08-22 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('screener', '0024_alter_message_cell_alter_message_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='screen',
            name='external_id',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]
