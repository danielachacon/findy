from django.db import migrations

def populate_user_profiles(apps, schema_editor):
    User = apps.get_model('accounts', 'CustomUser')
    UserProfile = apps.get_model('userprofile', 'UserProfile')

    for user in User.objects.all():
        UserProfile.objects.get_or_create(user=user)

class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_user_profiles),
    ]