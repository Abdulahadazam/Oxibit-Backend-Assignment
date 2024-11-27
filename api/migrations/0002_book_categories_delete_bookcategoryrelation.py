# Generated by Django 5.1.3 on 2024-11-25 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='categories',
            field=models.ManyToManyField(related_name='books', to='api.bookcategory'),
        ),
        migrations.DeleteModel(
            name='BookCategoryRelation',
        ),
    ]
