# Generated by Django 4.0.3 on 2022-03-07 12:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('web', '0008_rename_available_recommendation_visible'),
    ]

    operations = [
        migrations.CreateModel(
            name='AvailableSeat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField()),
                ('remain', models.IntegerField(default=-1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.restaurant')),
                ('table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.restauranttable')),
            ],
            options={
                'unique_together': {('restaurant', 'table', 'datetime')},
            },
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_number', models.CharField(max_length=20)),
                ('pg_transaction_number', models.CharField(default=None, max_length=50, null=True)),
                ('method', models.CharField(choices=[('CARD', '카드')], default='CARD', max_length=4)),
                ('status', models.CharField(choices=[('READY', '결제대기'), ('PAID', '결제완료'), ('FAILED', '예약실패'), ('CANCELED', '예약취소')], default='READY', max_length=10)),
                ('price', models.DecimalField(decimal_places=2, max_digits=12)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('paid_at', models.DateTimeField(default=None, null=True)),
                ('canceled_at', models.DateTimeField(default=None, null=True)),
                ('booker_name', models.CharField(default=None, max_length=20, null=True)),
                ('booker_phone', models.CharField(default=None, max_length=20, null=True)),
                ('booker_comment', models.CharField(default=None, max_length=200, null=True)),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.restaurant')),
                ('seat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.availableseat')),
                ('table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.restauranttable')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PayHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('booking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.booking')),
            ],
        ),
    ]
