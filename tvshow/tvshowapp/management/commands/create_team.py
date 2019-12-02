
from django.core.management.base import BaseCommand
from tvshowapp.models import User, CANCIDATE_TYPE, Candidate, Team

class Command(BaseCommand):
    help = 'Create  teams'

    def add_arguments(self, parser):
        parser.add_argument('teamname', type=str, help='team name')
        parser.add_argument('mentor', type=str, help='Mentor Username')
        parser.add_argument('-c', '--candidate', type=str, help='Candidate Username')

    def handle(self, *args, **kwargs):
        teamname = kwargs['teamname']
        mentor = kwargs['mentor']
        candidate = kwargs['candidate']
        try:
            mentor = User.objects.get(username=mentor)
            if not mentor.is_mentor:
                self.stdout.write('Not a valid mentor')
                return
        except User.DoesNotExist:
            self.stdout.write('Not a valid mentor')
            return
        if candidate:
            try:
                user = User.objects.get(username=candidate)
                if not user.is_candidate:
                    self.stdout.write('Not a valid candidate')
                    return
                candidate = user.candidate
            except User.DoesNotExist:
                self.stdout.write('Not a valid candidate')
                return
        team = Team.objects.create(
            mentor=mentor,
            team_name=teamname
        ) 
        if candidate:
            candidate.team = team
            candidate.save()
