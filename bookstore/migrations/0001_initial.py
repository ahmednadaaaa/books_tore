# Generated by Django 4.1 on 2024-02-09 11:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=190, null=True)),
                ('author', models.CharField(max_length=190, null=True)),
                ('price', models.FloatField(null=True)),
                ('category', models.CharField(choices=[('Classics', 'Classics'), ('Comic Book', 'Comic Book'), ('Fantasy', 'Fantasy'), ('Horror', 'Horror'), ('فلسفه', 'فلسفه'), ('روايات معاصرة', 'روايات معاصرة'), ('Horror', 'Horror')], max_length=190, null=True)),
                ('description', models.CharField(max_length=200, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('image', models.ImageField(blank=True, default='preson.png', null=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_date', models.DateTimeField()),
                ('is_finished', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=190, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('quantity', models.IntegerField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookstore.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookstore.book')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.AddField(
            model_name='order',
            name='details',
            field=models.ManyToManyField(through='bookstore.OrderDetail', to='bookstore.book'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=190, null=True)),
                ('email', models.CharField(max_length=190, null=True)),
                ('phone', models.CharField(max_length=190, null=True)),
                ('age', models.CharField(max_length=190, null=True)),
                ('avatar', models.ImageField(blank=True, default='preson.png', null=True, upload_to='')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='tags',
            field=models.ManyToManyField(to='bookstore.tag'),
        ),
    ]
