# Generated by Django 4.0.5 on 2022-06-16 15:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('screener', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='screen',
            name='housing_situation',
            field=models.CharField(default='rent', max_length=30),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('frequency', models.CharField(max_length=30)),
                ('screen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='screener.screen')),
            ],
        ),
    ]
