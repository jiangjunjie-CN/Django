# Generated by Django 3.1.4 on 2021-03-29 09:11

from django.db import migrations, models
import polls.models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_test'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to=polls.models.user_directory_path, validators=[polls.models.validate_imgFormat], verbose_name='图片'),
        ),
    ]