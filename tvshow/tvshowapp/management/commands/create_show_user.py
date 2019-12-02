
from django.core.management.base import BaseCommand
from tvshowapp.models import User, CANCIDATE_TYPE, Candidate

class Command(BaseCommand):
    help = 'Create  users'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='User Name')
        parser.add_argument('-t', '--usertype', type=int, help='User Type')
        parser.add_argument('-p', '--password', type=str, help='Password')

    def handle(self, *args, **kwargs):
        username = kwargs['username']
        usertype = kwargs['usertype']
        password = kwargs['password']
        user = User.objects.create_user(username=username, user_type=usertype, email='', password='123')
        if usertype == CANCIDATE_TYPE:
            Candidate.objects.create(user=user)
