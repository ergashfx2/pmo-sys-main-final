# Generated by Django 4.2.13 on 2024-06-16 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loyihalar', '0009_phase_phase_deadline_task_task_deadline_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='task_manager',
            field=models.CharField(max_length=150),
        ),
    ]
