# Generated by Django 5.0 on 2024-10-24 01:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0006_category_parent_category_favoritetopic_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publication',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='categories', to='article.category'),
        ),
    ]
