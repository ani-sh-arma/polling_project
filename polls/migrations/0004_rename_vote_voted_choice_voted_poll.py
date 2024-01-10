# Generated by Django 4.2.3 on 2024-01-10 09:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_voted'),
    ]

    operations = [
        migrations.RenameField(
            model_name='voted',
            old_name='vote',
            new_name='choice',
        ),
        migrations.AddField(
            model_name='voted',
            name='poll',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='polls.poll'),
            preserve_default=False,
        ),
    ]