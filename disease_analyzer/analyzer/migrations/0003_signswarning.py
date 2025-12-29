# Generated manually for SignsWarning model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analyzer', '0002_analysisresult_age_analysisresult_area_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SignsWarning',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('gender', models.CharField(default='Male', max_length=10)),
                ('age', models.IntegerField(default=0)),
                ('division', models.CharField(default='Dhaka', max_length=100)),
                ('area', models.CharField(default='-', max_length=255)),
                ('house_type', models.IntegerField(default=0)),
                ('ns1', models.BooleanField(default=False)),
                ('igm', models.BooleanField(default=False)),
                ('igg', models.BooleanField(default=False)),
                ('warning_prediction', models.BooleanField(default=False)),
                ('warning_confidence', models.FloatField(default=0.0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]

