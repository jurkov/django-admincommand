# Django-AdminCommand 

Django-AdminCommand is a Django application that makes it possible
to run Django management commands from the admin.

## Contributions

This is an enhanced fork, see the original: https://github.com/BackMarket/django-admincommand

Starting from this fork, changes were made in the following areas:

- Add Python 3.7 and Django 3.2 compatibility
- Everything needed from [django-sneak](https://github.com/rphlo/django-sneak.git) is merged directly with code
- Errors are shown in the same way as the results logs
- Form is shown as table with positional (required) arguments in bold
- Add support for date and json argument types as well as for choices parameter
- Commands are discovered from the list of names declared in the same `admin.py` file

> Asynchronous is still not supported for now

## Installation

- Install only: add `git+git://github.com/Hxperience1/django-admincommand@master#egg=django-admincommand` to your `requirements.txt` file and run `pip install -r requirements.txt` as usual
- Install and develop: clone the project, `cd` to the directory and run `pip install -e .`

> Uninstall simply with `pip uninstall django_admincommand`

Add the application where you defined management commands in the list of installed applications:

```python
INSTALLED_APPS = [
	'admincommand',
]
```

Finally, apply the app's initial migration

```shell
python manage.py migrate
```

## Settings

You need to activate the Django admin in the settings and ``urls.py``
depending on your needs the configuration may vary, refer
to the Django documentation related to the
[`admin application`](https://docs.djangoproject.com/en/dev/ref/contrib/admin/).


## Make magic happen


Create a Django Management Command:

```python
# ./music/management/commands/lyrics.py

class Command(BaseCommand):
    help = "Compute lyrics based an bitorological fluctuations"

    def handle(self, *args, **options):
        # algorithm that generated lyrics based on a title and a dictionary
```

Then you will have to add your command to the list:

```python
# ./music/admin.py

ADMIN_COMMAND_LIST = [
    'lyrics',
]
```

If all is well, the new admin command will be available under the
«Admin Command» area of the administration of the default admin site.

If you use custom admin site, don't forget to register
``admincommand.models.AdminCommand`` to the admin site object.


## Forms

Forms for the options are build by running an inspection of the command arguments (defaults to `string` for positional arguments and to `boolean` / checkbox for optional ones).
If the form does not seems correct for your management command, please check the `type` option in your management command.


## Logs

Logs emitted using the Django (and Python) logging module will be printed on the results page of the admin. They will still go into the normal logging process. If exception occurs it will also be printed on the results page.

Please, make sure you log your messages with a logger and not a `print` function, otherwise the results page will be empty. For more info on how to use a logger see [Django documentation](https://docs.djangoproject.com/en/3.2/topics/logging/).


## Compatibility

This module was tested and is designed for Django 3.2, may work with other versions

## Permissions

You MUST add to every user or groups that should have access to the list of commands
«Can change admincommand» permission. Every admin command gets it's own permission
«Can Run AnAdminCommand», so you can add it to proper users or group. Users will
only see and be able to execute admin commands for which they have the permission.


## Asynchronous tasks


Not supported at the moment

