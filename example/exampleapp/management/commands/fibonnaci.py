from django.core.management.base import BaseCommand


def fibonnaci(x):
    if x == 0:
        return 0
    if x == 1:
        return 1
    return fibonnaci(x-1) + fibonnaci(x-2)


class Command(BaseCommand):
    help = "Compute fibonnaci number"


    def add_arguments(self, parser):
        parser.add_argument('argument')


    def handle(self, *args, **options):
        arg = options['argument']
        r = fibonnaci(int(arg))
        self.stdout.write('fibonnaci(%s) = %s' % (arg, r))
