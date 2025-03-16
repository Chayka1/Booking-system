# Generated by Django 5.1.7 on 2025-03-16 10:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Barber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name="Ім'я майстра")),
                ('is_active_today', models.BooleanField(default=True, verbose_name='Активний сьогодні')),
            ],
            options={
                'verbose_name': 'Майстер',
                'verbose_name_plural': 'Майстри',
            },
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Назва посади')),
            ],
            options={
                'verbose_name': 'Посада',
                'verbose_name_plural': 'Посади',
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Назва послуги')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Опис послуги')),
            ],
            options={
                'verbose_name': 'Послуга',
                'verbose_name_plural': 'Послуги',
            },
        ),
        migrations.CreateModel(
            name='BarberSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_of_week', models.CharField(choices=[('0', 'Понеділок'), ('1', 'Вівторок'), ('2', 'Середа'), ('3', 'Четвер'), ('4', 'П’ятниця'), ('5', 'Субота'), ('6', 'Неділя')], max_length=1, verbose_name='День тижня')),
                ('start_time', models.TimeField(verbose_name='Початок роботи')),
                ('end_time', models.TimeField(verbose_name='Кінець роботи')),
                ('barber', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.barber', verbose_name='Майстер')),
            ],
            options={
                'verbose_name': 'Розклад майстра',
                'verbose_name_plural': 'Розклади майстрів',
            },
        ),
        migrations.AddField(
            model_name='barber',
            name='position',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.position', verbose_name='Посада'),
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100, verbose_name='Ім’я клієнта')),
                ('last_name', models.CharField(max_length=100, verbose_name='Прізвище клієнта')),
                ('phone', models.CharField(max_length=15, verbose_name='Телефон')),
                ('date', models.DateField(verbose_name='Дата')),
                ('time', models.TimeField(verbose_name='Час')),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Ціна')),
                ('barber', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.barber', verbose_name='Майстер')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.service', verbose_name='Послуга')),
            ],
            options={
                'verbose_name': 'Бронювання',
                'verbose_name_plural': 'Бронювання',
            },
        ),
        migrations.CreateModel(
            name='BarberService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Ціна')),
                ('barber', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.barber', verbose_name='Майстер')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.service', verbose_name='Послуга')),
            ],
            options={
                'verbose_name': 'Послуга майстра',
                'verbose_name_plural': 'Послуги майстрів',
            },
        ),
        migrations.AddField(
            model_name='barber',
            name='services',
            field=models.ManyToManyField(through='booking.BarberService', to='booking.service', verbose_name='Послуги'),
        ),
    ]
