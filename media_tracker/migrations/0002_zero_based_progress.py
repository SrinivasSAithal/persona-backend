from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("media_tracker", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="media",
            name="current_season",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="media",
            name="current_episode",
            field=models.IntegerField(default=0),
        ),
    ]