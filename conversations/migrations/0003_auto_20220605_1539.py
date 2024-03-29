# Generated by Django 2.2.5 on 2022-06-05 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conversations', '0002_auto_20220605_1537'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conversation',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='conversation',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='message',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='message',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
