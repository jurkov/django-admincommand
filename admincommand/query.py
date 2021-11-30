from admincommand.models import AdminCommand


class CommandQuerySet(object):
    """
    Custom QuerySet to list runnable commands
    """

    class query:
        select_related = True
        where = False
        order_by = []

    def __init__(self, user, value=None):
        self.user = user
        if value is None:
            self.value = self.filter().value
        else:
            self.value = value

    def __len__(self):
        return len(self.value)

    def __getitem__(self, s):
        if isinstance(s, slice):
            return self.value.__getitem__(s)
        else:
            return self.value[s]

    def _clone(self):
        return type(self)(self.user, self.value)

    def count(self):
        return len(self)

    def filter(self, *args, **kwargs):
        all_commands = []
        for command in AdminCommand.all():
            # only list commands that the user can run
            # to avoid useless 503 messages
            full_permission_codename = "admincommand.%s" % command.permission_codename()
            if self.user.has_perm(full_permission_codename):
                all_commands.append(command)
        return type(self)(self.user, all_commands)

    def order_by(self, *args, **kwargs):
        return self

    def iterator(self):
        for v in self.value:
            yield v
