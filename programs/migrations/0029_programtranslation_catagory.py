# Generated by Django 4.0.5 on 2023-01-30 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('programs', '0028_alter_navigator_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='programtranslation',
            name='catagory',
            field=models.CharField(default='no catagory', max_length=120),
            preserve_default=False,
        ),
    ]
