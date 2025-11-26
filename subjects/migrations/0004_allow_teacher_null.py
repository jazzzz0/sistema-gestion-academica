# Generated manually to allow teacher to be nullable
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("subjects", "0003_alter_subject_description_alter_subject_teacher"),
    ]

    operations = [
        migrations.AlterField(
            model_name="subject",
            name="teacher",
            field=models.ForeignKey(
                to="users.teacher",
                on_delete=django.db.models.deletion.PROTECT,
                related_name="subjects",
                verbose_name="Docente",
                help_text="Docente encargado de la materia",
                null=True,
                blank=True,
            ),
        ),
    ]
