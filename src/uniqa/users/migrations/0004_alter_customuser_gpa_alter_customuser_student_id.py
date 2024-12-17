# Generated by Django 5.0.6 on 2024-12-09 01:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_customuser_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='gpa',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='student_id',
            field=models.CharField(blank=True, max_length=20, unique=True),
        ),
    ]
