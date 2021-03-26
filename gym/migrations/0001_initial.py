# Generated by Django 3.1.7 on 2021-03-25 10:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exercise_name', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Gym',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gym_name', models.CharField(max_length=30)),
                ('gym_address', models.CharField(max_length=80)),
                ('gym_limitation', models.IntegerField(default=0)),
                ('gym_coordinate_lat', models.FloatField()),
                ('gym_coordinate_long', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Park',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('park_name', models.CharField(max_length=30)),
                ('park_address', models.CharField(max_length=80)),
                ('park_coordinate_lat', models.FloatField()),
                ('park_coordinate_long', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Playground',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('playground_name', models.CharField(max_length=30)),
                ('playground_address', models.CharField(max_length=80)),
                ('playground_coordinate_lat', models.FloatField()),
                ('playground_coordinate_long', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='SafeTips',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(max_length=10)),
                ('subTitle', models.CharField(max_length=30)),
                ('content', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='playgroundImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_name', models.CharField(max_length=10)),
                ('playground', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gym.playground')),
            ],
        ),
        migrations.CreateModel(
            name='ParkImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_name', models.CharField(max_length=10)),
                ('park', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gym.park')),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_name', models.CharField(max_length=10)),
                ('gym', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gym.gym')),
            ],
        ),
        migrations.CreateModel(
            name='ExerciseTips',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=20)),
                ('exercise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gym.exercise')),
            ],
        ),
    ]
