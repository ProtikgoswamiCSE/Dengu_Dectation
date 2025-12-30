# Generated manually for SignsWarning symptom fields

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analyzer', '0003_signswarning'),
    ]

    operations = [
        migrations.AddField(
            model_name='signswarning',
            name='symptom_mild_fever',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='signswarning',
            name='symptom_eyelid_pain',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='signswarning',
            name='symptom_headache',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='signswarning',
            name='symptom_body_aches',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='signswarning',
            name='symptom_nausea',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='signswarning',
            name='symptom_skin_rash',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='signswarning',
            name='symptom_fatigue',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='signswarning',
            name='symptom_stomach_pain',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='signswarning',
            name='symptom_dry_throat',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='signswarning',
            name='symptom_lightheadedness',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='signswarning',
            name='symptom_chest_pain',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='signswarning',
            name='symptom_bleeding',
            field=models.IntegerField(default=0),
        ),
    ]

