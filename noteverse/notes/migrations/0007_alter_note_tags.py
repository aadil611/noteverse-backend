# Generated by Django 4.2.3 on 2024-08-20 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0006_note_created_at_note_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='notes', to='notes.tag'),
        ),
    ]
