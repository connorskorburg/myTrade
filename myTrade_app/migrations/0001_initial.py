# Generated by Django 2.2 on 2020-05-19 22:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=100)),
                ('username', models.CharField(max_length=30)),
                ('bio', models.CharField(max_length=255)),
                ('avatar', models.CharField(max_length=25)),
                ('password', models.CharField(max_length=255)),
                ('account_balance', models.FloatField(default=0.0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Trade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(max_length=15)),
                ('price_per_share', models.DecimalField(decimal_places=2, default=0.0, max_digits=15)),
                ('total_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=15)),
                ('shares', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('stock_holder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trades', to='myTrade_app.User')),
            ],
        ),
        migrations.CreateModel(
            name='SoldTrade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price_sold', models.DecimalField(decimal_places=2, default=0.0, max_digits=15)),
                ('shares_sold', models.IntegerField()),
                ('total_price_gained', models.DecimalField(decimal_places=2, default=0.0, max_digits=15)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('stock_holder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sold_trades', to='myTrade_app.User')),
                ('trade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='myTrade_app.Trade')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('poster', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='myTrade_app.User')),
                ('user_who_liked', models.ManyToManyField(related_name='liked_posts', to='myTrade_app.User')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('commenter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='myTrade_app.User')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='myTrade_app.Post')),
            ],
        ),
    ]
