# Generated by Django 5.0.2 on 2024-03-08 02:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPostTag',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=128, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=256)),
                ('content', models.TextField()),
                ('banner', models.FileField(upload_to='blog')),
                ('thumbnail', models.FileField(upload_to='blog')),
                ('tags', models.ManyToManyField(to='blog.blogposttag')),
            ],
            options={
                'ordering': ['updated'],
            },
        ),
    ]
