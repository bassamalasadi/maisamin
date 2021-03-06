# Generated by Django 3.1.4 on 2021-05-08 16:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=200)),
                ('category', models.CharField(choices=[('cake', 'cake'), ('pastry', 'pastry'), ('cheesecake', 'cheesecake'), ('manakish', 'manakish'), ('meze', 'meze')], max_length=20)),
                ('contents', models.TextField()),
                ('is_gluteen_free', models.BooleanField(default=False)),
                ('is_loctose_free', models.BooleanField(default=False)),
                ('description', models.TextField()),
                ('additional_info', models.TextField()),
                ('feedback', models.TextField(blank=True, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('slug', models.SlugField()),
                ('image1', models.ImageField(upload_to='')),
                ('size', multiselectfield.db.fields.MultiSelectField(choices=[('6 People', '6 People'), ('8 People', '8 People'), ('12 People', '12 People'), ('16 People', '16 People'), ('20 People', '20 People')], max_length=47)),
            ],
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('address', models.TextField()),
                ('order', models.TextField()),
                ('create', models.DateTimeField()),
                ('phone', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=100)),
                ('delivery', models.DateTimeField()),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Variation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('size', models.CharField(max_length=30)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.product')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('one_click_purchasing', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordered', models.BooleanField(default=False)),
                ('quantity', models.IntegerField(default=1)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordered', models.BooleanField(default=False)),
                ('create', models.DateTimeField(auto_now_add=True)),
                ('products', models.ManyToManyField(to='main.OrderItem')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstName', models.CharField(max_length=100)),
                ('lastName', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('street_address', models.CharField(max_length=100)),
                ('apartment_address', models.CharField(blank=True, max_length=100, null=True)),
                ('postal', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=200)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.order')),
            ],
            options={
                'verbose_name_plural': 'Addresses',
            },
        ),
    ]
