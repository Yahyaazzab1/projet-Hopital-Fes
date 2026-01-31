# Generated migration to remove technician role
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(
                choices=[
                    ('admin', 'Administrateur'),
                    ('doctor', 'Médecin'),
                    ('nurse', 'Infirmier/Infirmière')
                ],
                default='doctor',
                max_length=20,
                verbose_name='Rôle'
            ),
        ),
    ]
