# Generated by Django 2.2.5 on 2019-10-18 23:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MenuServe', '0010_auto_20190921_0817'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
            ],
        ),
        migrations.RenameField(
            model_name='employee',
            old_name='name',
            new_name='username',
        ),
        migrations.RenameField(
            model_name='manager',
            old_name='name',
            new_name='username',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='manager',
        ),
        migrations.AddField(
            model_name='employee',
            name='manager',
            field=models.ManyToManyField(to='MenuServe.Manager'),
        ),
    ]
