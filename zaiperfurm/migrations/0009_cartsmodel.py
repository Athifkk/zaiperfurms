# Generated by Django 4.1.5 on 2023-02-09 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zaiperfurm', '0008_remove_userregmodel_pimage_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='cartsmodel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cartname', models.CharField(max_length=25)),
                ('cartprice', models.IntegerField()),
                ('cartdes', models.CharField(max_length=40)),
                ('cartimage', models.ImageField(upload_to='zaiperfurm/static')),
            ],
        ),
    ]
