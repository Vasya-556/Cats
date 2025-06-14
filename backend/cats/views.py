from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import SpyCat, Mission, Target
from .serializers import SpyCatSerializer, MissionSerializer, TargetSerializer

class SpyCatViewSet(viewsets.ModelViewSet):
    queryset = SpyCat.objects.all()
    serializer_class = SpyCatSerializer

    def partial_update(self, request, *args, **kwargs):
        if 'salary' not in request.data:
            return Response({'error': 'Only salary can be updated'}, status=status.HTTP_400_BAD_REQUEST)
        return super().partial_update(request, *args, **kwargs)

class MissionViewSet(viewsets.ModelViewSet):
    queryset = Mission.objects.all()
    serializer_class = MissionSerializer

    def destroy(self, request, *args, **kwargs):
        mission = self.get_object()
        if mission.cat is not None:
            return Response({'error': 'Cannot delete mission assigned to a cat'}, status=status.HTTP_400_BAD_REQUEST)
        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=['post'])
    def assign_cat(self, request, pk=None):
        mission = self.get_object()
        cat_id = request.data.get('cat')
        if not cat_id:
            return Response({'error': 'Cat id required'}, status=status.HTTP_400_BAD_REQUEST)
        from django.shortcuts import get_object_or_404
        cat = get_object_or_404(SpyCat, id=cat_id)
        mission.cat = cat
        mission.save()
        return Response(self.get_serializer(mission).data)

    @action(detail=True, methods=['post'])
    def mark_complete(self, request, pk=None):
        mission = self.get_object()
        mission.completed = True
        mission.save()
        for target in mission.targets.all():
            target.completed = True
            target.save()
        return Response(self.get_serializer(mission).data)

class TargetViewSet(viewsets.ModelViewSet):
    queryset = Target.objects.all()
    serializer_class = TargetSerializer