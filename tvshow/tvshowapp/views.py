from django.shortcuts import render
from django.http import Http404
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from .models import Candidate, Performance, PerformanceScore, Team
from .serializers import CandidateSerializer, CandidateListSerializer, TeamListSerializer, TeamDetailSerializer


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=status.HTTP_404_NOT_FOUND)
    if user.is_candidate:
        # candidates are not allowed to login for now
        return Response({'error': 'Invalid Credentials'},
                status=status.HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key,
                     'user_id': user.pk,
                     'user_type': user.user_type
                     },
                    status=status.HTTP_200_OK)

class CandidateList(APIView):
    """
    List all candidates.
    """
    def get(self, request, format=None):
        if not request.user.is_authenticated or not request.user.is_mentor:
            return Response(status=403)
        candidates = Candidate.objects.filter(team__mentor=request.user)
        serializer = CandidateSerializer(candidates, many=True)
        return Response(serializer.data)

class CandidateDetail(APIView):
    def get_object(self, pk):
        try:
            return Candidate.objects.get(pk=pk)
        except Candidate.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        if not request.user.is_authenticated or not request.user.is_mentor:
            return Response(status=403)
        candidate = self.get_object(pk)
        serializer = CandidateSerializer(candidate)
        return Response(serializer.data)

class TeamList(APIView):
    """
    List all teams.
    """
    def get(self, request, format=None):
        if not request.user.is_authenticated or not request.user.is_admin:
            return Response(status=403)
        teams = Team.objects.all()
        serializer = TeamDetailSerializer(teams, many=True)
        return Response(serializer.data)

class TeamDetail(APIView):
    """
    Team details.
    """
    def get_object(self, pk):
        try:
            return Team.objects.get(pk=pk)
        except Team.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        if not request.user.is_authenticated or not request.user.is_mentor:
            return Response(status=403)
        team = self.get_object(pk)
        serializer = TeamDetailSerializer(team)
        return Response(serializer.data)
