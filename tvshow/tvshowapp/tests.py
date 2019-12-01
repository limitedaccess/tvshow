from django.test import TestCase

from rest_framework.test import APIRequestFactory, force_authenticate

from .models import User, Candidate, Performance, PerformanceScore, Team
from .serializers import CandidateSerializer, TeamDetailSerializer
from .views import CandidateList, TeamList


class ModelTests(TestCase):

    def setUp(self):
        self.admin = User.objects.create(
            username='admin1', email='admin@test.com', user_type=1, password='test1')
        self.mentor1 = User.objects.create(
            username='mentor1', email='mentor1@test.com', user_type=2, password='test1')
        self.team1 = Team.objects.create(
            mentor=self.mentor1
        )
        self.candidateUser = User.objects.create(
            username='candidate1', email='candidate1@test.com', user_type=3, password='test1')
        self.candidate1 = Candidate.objects.create(
            user=self.candidateUser,
            team=self.team1
        )

    def test_user_type(self):
        admin = User.objects.get(username='admin1')
        self.assertTrue(admin.is_admin)
        mentor1 = User.objects.get(username='mentor1')
        self.assertFalse(mentor1.is_admin)
        self.assertTrue(mentor1.is_mentor)
        self.assertTrue(self.candidateUser.is_candidate)

    def test_performance_score(self):
        performance = Performance.objects.create(
            candidate=self.candidate1,
            name='Song by candidate1'
        )
        PerformanceScore.objects.create(
            performance=performance,
            mentor=self.mentor1,
            score=100
        )
        self.assertEquals(performance.average_score, 100)
        mentor2 = User.objects.create_user(username='mentor2', email='mentor2@test.com', user_type=2)
        PerformanceScore.objects.create(
                performance=performance,
                mentor=mentor2,
                score=0
            )
        self.assertEquals(performance.average_score, 50)

        performance2 = Performance.objects.create(
            candidate=self.candidate1,
            name='Song 2 by candidate1'
        )
        PerformanceScore.objects.create(
            performance=performance,
            mentor=self.mentor1,
            score=80
        )
        score = PerformanceScore.average_score_by_candidate(self.candidate1)
        self.assertEquals(score, 60)
        score = PerformanceScore.average_score_by_team(self.team1)
        self.assertEquals(score, 60)

    def test_candidate_serializer(self):
        serializer = CandidateSerializer(self.candidate1)
        self.assertEqual(set(serializer.data.keys()), set(
            ['pk', 'team', 'team_average', 'personal_average', 'username', 'first_name', 'last_name', 'performances']))

    def test_team_serializer(self):
        serializer = TeamDetailSerializer(self.team1)
        self.assertEqual(set(serializer.data.keys()), set(
            ['pk', 'team_name', 'mentor_name', 'team_average', 'candidates']))

    def test_candidates_view(self):
        # only mentor can get a list of candidates
        factory = APIRequestFactory()
        request = factory.get('/api/candidates/')
        view = CandidateList.as_view()
        force_authenticate(request, user=self.mentor1)
        response = view(request)
        self.assertEquals(response.status_code, 200)

        force_authenticate(request, user=self.admin)
        response = view(request)
        self.assertEquals(response.status_code, 403)

    def test_teams_view(self):
        # only admin can get a list of teams
        factory = APIRequestFactory()
        request = factory.get('/api/teams/')
        view = TeamList.as_view()
        force_authenticate(request, user=self.mentor1)
        response = view(request)
        self.assertEquals(response.status_code, 403)

        force_authenticate(request, user=self.admin)
        response = view(request)
        self.assertEquals(response.status_code, 200)
