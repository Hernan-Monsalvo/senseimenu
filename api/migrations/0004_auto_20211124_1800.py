# Generated by Django 3.2.9 on 2021-11-24 18:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20211124_1726'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='weekmenu',
            name='name',
        ),
        migrations.AddField(
            model_name='dish',
            name='owner',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='dishes', to='api.myuser'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='weekmenu',
            name='owner',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='menus', to='api.myuser'),
            preserve_default=False,
        ),
    ]
