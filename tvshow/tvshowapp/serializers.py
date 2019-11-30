from tvshowapp.models import Candidate, Performance, User, PerformanceScore, Team
from rest_framework import serializers

class PerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performance
        fields = ('name', 'date', 'average_score')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username')

class CandidateListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ('pk', 'team', 'username', 'first_name', 'last_name')
    username = serializers.CharField(source='user.username')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    team = serializers.CharField(source='team.team_name')


class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ('pk', 'team', 'team_average', 'personal_average', 'username', 'first_name', 'last_name', 'performances')
    username = serializers.CharField(source='user.username')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    performances = PerformanceSerializer(many=True, read_only=True)
    team = serializers.CharField(source='team.team_name')
    team_average = serializers.SerializerMethodField()
    personal_average = serializers.SerializerMethodField()

    def get_team_average(self, obj):
        return PerformanceScore.average_score_by_team(obj.team)

    def get_personal_average(self, obj):
        return PerformanceScore.average_score_by_candidate(obj)

class TeamCandidatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ('pk', 'team', 'username', 'first_name', 'last_name', 'performances')
    username = serializers.CharField(source='user.username')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    performances = PerformanceSerializer(many=True, read_only=True)

class TeamListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('pk', 'team_name', 'mentor_name', 'team_average', 'candidates')
    mentor_name = serializers.CharField(source='mentor.username')
    team_average = serializers.SerializerMethodField()
    candidates = TeamCandidatesSerializer(many=True, read_only=True)

    def get_team_average(self, obj):
        return PerformanceScore.average_score_by_team(obj)

class TeamDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('pk', 'team_name', 'mentor_name', 'team_average', 'candidates')
    mentor_name = serializers.CharField(source='mentor.username')
    team_average = serializers.SerializerMethodField()
    candidates = TeamCandidatesSerializer(many=True, read_only=True)

    def get_team_average(self, obj):
        return PerformanceScore.average_score_by_team(obj)