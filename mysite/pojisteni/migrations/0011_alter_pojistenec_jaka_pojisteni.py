# Generated by Django 4.1.7 on 2023-04-05 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pojisteni', '0010_rename_pojisteni_pojistenec_jaka_pojisteni'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pojistenec',
            name='jaka_pojisteni',
            field=models.ManyToManyField(to='pojisteni.pojisteni', verbose_name='Pojištění'),
        ),
    ]