# Generated by Django 4.0.1 on 2022-08-31 09:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0004_comment_reply_alter_comment_post_alter_comment_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='reply',
            new_name='parent',
        ),
    ]