# Generated by Django 4.0.6 on 2022-07-24 01:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('userapp', '0002_alter_userinfo_pwd'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goodsid', models.PositiveIntegerField()),
                ('colorid', models.PositiveIntegerField()),
                ('sizeid', models.PositiveIntegerField()),
                ('count', models.PositiveIntegerField()),
                ('isdelete', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userapp.userinfo')),
            ],
        ),
    ]
