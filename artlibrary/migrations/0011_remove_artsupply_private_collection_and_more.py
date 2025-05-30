# Generated by Django 5.1.6 on 2025-03-27 02:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artlibrary', '0010_remove_artsupply_collection_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='artsupply',
            name='private_collection',
        ),
        migrations.RemoveField(
            model_name='artsupply',
            name='public_collections',
        ),
        migrations.AddField(
            model_name='artsupply',
            name='collection',
            field=models.ManyToManyField(blank=True, null=True, related_name='items', to='artlibrary.collection'),
        ),
    ]
