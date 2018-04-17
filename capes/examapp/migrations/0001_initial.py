# Generated by Django 2.0.1 on 2018-01-20 18:22

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('qid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('question_text', models.TextField(default=None)),
                ('marks', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Question_Descriptive',
            fields=[
                ('qid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='examapp.Question')),
                ('keywords', models.TextField(default=None)),
            ],
        ),
        migrations.CreateModel(
            name='Question_Fillup',
            fields=[
                ('qid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='examapp.Question')),
                ('correct_ans', models.TextField(default=None)),
            ],
        ),
        migrations.CreateModel(
            name='Question_Mcq_Multiple',
            fields=[
                ('qid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='examapp.Question')),
                ('correct_ans_indices', models.TextField(default=None)),
                ('options', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Question_Mcq_Single',
            fields=[
                ('qid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='examapp.Question')),
                ('correct_ans_index', models.TextField(default=None)),
                ('options', models.TextField()),
            ],
        ),
    ]
