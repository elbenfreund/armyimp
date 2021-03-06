# Generated by Django 2.0.2 on 2018-02-21 14:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FactionKeyword',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('comment', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ItemSlot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('min_amount', models.PositiveIntegerField(blank=True, default=1, help_text='Min. amount of eligible items this slot takes.', null=True)),
                ('max_amount', models.PositiveIntegerField(blank=True, default=1, help_text='Max. amount of eligible items this slot takes.', null=True)),
                ('default', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='slot_defaults', to='w40k.Item')),
            ],
        ),
        migrations.CreateModel(
            name='ModelProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('movement', models.PositiveIntegerField(blank=True, null=True)),
                ('weapon_skill', models.PositiveIntegerField()),
                ('balistic_skill', models.PositiveIntegerField(blank=True, null=True)),
                ('strength', models.PositiveIntegerField()),
                ('toughness', models.PositiveIntegerField()),
                ('wounds', models.PositiveIntegerField()),
                ('attacks', models.PositiveIntegerField(blank=True, null=True)),
                ('leadership', models.PositiveIntegerField()),
                ('saves', models.PositiveIntegerField()),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='OrganizationItemIntermediate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.PositiveIntegerField(help_text="This is the price (per point list) that the item costs for this organization. Please take note that a UnitModel's default items are not included in the models price. And need to be paid for just as any other item.")),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='w40k.Item')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='w40k.Organization')),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('category', models.CharField(choices=[('HQ', 'HQ'), ('Elites', 'Elites'), ('Troops', 'Troops'), ('Fast Attack', 'Fast Attack'), ('Heavy Support', 'Heavy Support'), ('Flyers', 'Flyers'), ('Dedicated Transport', 'Dedicated Transport')], max_length=20)),
                ('is_named_character', models.BooleanField(help_text='Set to true if this is a named Character. This changes how equipped items get handled.')),
                ('power_rating', models.PositiveIntegerField()),
                ('model_price', models.PositiveIntegerField(help_text='Points per model')),
                ('max_per_army', models.PositiveIntegerField(blank=True, help_text='How many of this unit an army may include at max.', null=True)),
                ('models_min', models.PositiveIntegerField(default=1, help_text='Minimal amount of models this unit needs to include')),
                ('models_max', models.PositiveIntegerField(help_text='Maximum amount of models this unit may include')),
                ('transport', models.TextField(blank=True, help_text='If this unit has transportation capabilities, specify details here.')),
                ('comment', models.TextField(blank=True)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='UnitAbility',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField()),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='UnitKeyword',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='UnitModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='w40k.ModelProfile')),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='models_included', to='w40k.Unit')),
            ],
        ),
        migrations.CreateModel(
            name='WargearList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('Ranged', 'Ranged'), ('Special', 'Special'), ('Heavy', 'Heavy'), ('Melee', 'Melee')], max_length=10)),
                ('items', models.ManyToManyField(related_name='wargear_lists', to='w40k.Item')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='w40k.Organization')),
            ],
        ),
        migrations.CreateModel(
            name='WeaponProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('category', models.CharField(choices=[('Ranged', 'Ranged'), ('Melee', 'Melee')], max_length=20)),
                ('min_range', models.PositiveIntegerField(blank=True, null=True)),
                ('max_range', models.PositiveIntegerField(blank=True, null=True)),
                ('attack_type', models.CharField(choices=[('Rapid Fire', 'Rapid Fire'), ('Melee', 'Melee'), ('Assault', 'Assault'), ('Grenade', 'Grenade'), ('Pistol', 'Pistol'), ('Heavy', 'Heavy')], help_text='This specifies which attack specific extra rules apply.', max_length=20)),
                ('number_of_attacks', models.CharField(max_length=5)),
                ('_strength_value', models.IntegerField(blank=True, help_text='Fix STRENGTH value.', null=True)),
                ('_strength_multiplier', models.IntegerField(blank=True, help_text='Multiplier for effective STRENGTH value.', null=True)),
                ('_strength_user', models.BooleanField(help_text='Set to TRUE if the STRENGTH is determined by the USER.')),
                ('armor_penetration', models.IntegerField(blank=True, null=True)),
                ('_damage_value', models.IntegerField(blank=True, help_text='Use this if the profile deals a fixed amount of DAMAGE.', null=True)),
                ('_damage_die_type', models.IntegerField(blank=True, choices=[(3, 'W3'), (6, 'W6')], help_text='Use his to specify which type of die is used, if any.', null=True)),
                ('_damage_dice_amount', models.IntegerField(blank=True, help_text='Use thisi to specify how many die are used, if any.', null=True)),
                ('comments', models.TextField(blank=True)),
                ('weapon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='weapon_profiles', to='w40k.Item')),
            ],
        ),
        migrations.AddField(
            model_name='unit',
            name='abilities',
            field=models.ManyToManyField(blank=True, to='w40k.UnitAbility'),
        ),
        migrations.AddField(
            model_name='unit',
            name='faction_keywords',
            field=models.ManyToManyField(blank=True, to='w40k.FactionKeyword'),
        ),
        migrations.AddField(
            model_name='unit',
            name='keywords',
            field=models.ManyToManyField(blank=True, to='w40k.UnitKeyword'),
        ),
        migrations.AddField(
            model_name='unit',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='units', to='w40k.Organization'),
        ),
        migrations.AddField(
            model_name='organization',
            name='items',
            field=models.ManyToManyField(blank=True, help_text='These are all items accessible to any unit of that organization.', related_name='organizations', through='w40k.OrganizationItemIntermediate', to='w40k.Item'),
        ),
        migrations.AddField(
            model_name='itemslot',
            name='model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='item_slots', to='w40k.UnitModel'),
        ),
        migrations.AddField(
            model_name='itemslot',
            name='option_from_list',
            field=models.ManyToManyField(blank=True, to='w40k.WargearList'),
        ),
        migrations.AddField(
            model_name='itemslot',
            name='options',
            field=models.ManyToManyField(blank=True, related_name='slot_options', to='w40k.Item'),
        ),
        migrations.AlterUniqueTogether(
            name='organizationitemintermediate',
            unique_together={('organization', 'item')},
        ),
    ]
