# Generated by Django 4.1 on 2024-02-11 00:08

import creditcards.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bookstore', '0002_remove_book_tags'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shipment_address', models.CharField(max_length=150)),
                ('shipment_phone', models.CharField(max_length=50)),
                ('card_number', creditcards.models.CardNumberField(max_length=25)),
                ('expire', creditcards.models.CardExpiryField()),
                ('security_code', creditcards.models.SecurityCodeField(max_length=4)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookstore.order')),
            ],
        ),
    ]
