# Generated by Django 5.1.6 on 2025-03-13 18:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artlibrary', '0002_alter_customuser_user_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='artsupply',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='artsupply',
            name='status',
            field=models.CharField(choices=[('available', 'Available'), ('checked_out', 'Checked Out')], default='available', max_length=20),
        ),
        migrations.AlterField(
            model_name='artsupply',
            name='added_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='added_items', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='date_joined',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('num_items', models.PositiveIntegerField(default=0)),
                ('is_public', models.BooleanField(default=True)),
                ('users', models.ManyToManyField(blank=True, related_name='collections', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='artsupply',
            name='collection',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='items', to='artlibrary.collection'),
        ),
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveIntegerField()),
                ('comment', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='artlibrary.artsupply')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
