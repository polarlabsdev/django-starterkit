# Generated by Django 5.0.4 on 2024-04-12 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_blogpost_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='tags',
            field=models.ManyToManyField(related_name='posts', to='blog.blogposttag'),
        ),
    ]
