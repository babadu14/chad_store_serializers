# Generated by Django 5.1.2 on 2025-02-19 19:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0002_rename_product_categoryimage_categories'),
    ]

    operations = [
        migrations.RenameField(
            model_name='categoryimage',
            old_name='categories',
            new_name='category',
        ),
    ]
