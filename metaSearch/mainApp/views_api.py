from django.contrib.auth.models import User, Group
from django.core.exceptions import FieldError
from rest_framework import viewsets
from mainApp.serializers import ProjectSerializer, CategorySerializer, KindSerializer, PageLanguageSerializer, ProgrammingLanguageSerializer
from mainApp.models import Project, Category, ProgrammingLanguage, Kind, PageLanguage
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from haystack.query import SearchQuerySet
from mainApp.haystackUtil import HayStackUtilities
from haystack.inputs import AutoQuery
from mainApp.customExceptions import FieldWrong




@api_view(['GET'])
def project_list(request):
    """
    List all Projects, or create a new snippet.
    """
    if request.method == 'GET':
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def project_detail(request, pk):
    """
    Retrieve, update or delete a project instance.
    """
    try:
        project = Project.objects.get(pk=pk)
    except Project.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        print("IN THING")
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

@api_view(['GET'])
def project_search_fulltext(request, text):
    print(text)
    wrappedpro = SearchQuerySet().filter(content=AutoQuery(text))
    resultList = HayStackUtilities.unwrapResult(wrappedpro)
    print(resultList)
    if len(wrappedpro) == 0:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = ProjectSerializer(resultList, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def search_project(request):
    params = deconstruct_params(request)
    try:
        currentResults = apply_filters(Project.objects.all(), params)
    except FieldWrong as e:
        return Response("Field invalid!: " + str(e.field) + "=" + str(e.value), status=status.HTTP_400_BAD_REQUEST )

    if(len(currentResults) == 0) :
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = ProjectSerializer(currentResults, many=True)
    return Response(serializer.data)



@api_view(['GET'])
def search_category(request):
    params = deconstruct_params(request)
    try:
        currentResults = apply_filters(Category.objects.all(), params)
    except FieldWrong as e:
        return Response("Field invalid!: " + str(e.field) + "=" + str(e.value), status=status.HTTP_400_BAD_REQUEST )
    if(len(currentResults) == 0) :
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = CategorySerializer(currentResults, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def search_kind(request):
    params = deconstruct_params(request)
    try:
        currentResults = apply_filters(Kind.objects.all(), params)
    except FieldWrong as e:
        return Response("Field invalid!: " + str(e.field) + "=" + str(e.value), status=status.HTTP_400_BAD_REQUEST )
    if(len(currentResults) == 0) :
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = KindSerializer(currentResults, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def search_language(request):
    params = deconstruct_params(request)
    try:
        currentResults = apply_filters(PageLanguage.objects.all(), params)
    except FieldWrong as e:
        return Response("Field invalid!: " + str(e.field) + "=" + str(e.value), status=status.HTTP_400_BAD_REQUEST )
    if(len(currentResults) == 0) :
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = PageLanguageSerializer(currentResults, many=True)
    return Response(serializer.data)

def apply_filters(all_objects, params):
    for (key,action, values) in params:
        search_field = key + '__' + action if action != '' else key
        for value in values:
            try:
                all_objects = all_objects.filter(**{search_field: value})
            except FieldError:
                raise FieldWrong(search_field, value)
    return all_objects

def deconstruct_params(params):
    params_list = []
    params_raw = params.GET.lists()
    for (key, value) in params_raw:
        field_action_list = key.split('*')
        if len(field_action_list) > 2 :
            raise Exception('underscoretm','Too Many Underscores')
        params_list.append((field_action_list[0], field_action_list[1] if len(field_action_list) > 1 else '', value))
    return params_list

#
# class ProjectViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """
#     queryset = Project.objects.all().order_by('-created_at')
#     serializer_class = ProjectSerializer
#
# class CategoryViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer
#
# class KindViewSet(viewsets.ModelViewSet):
#     queryset = Kind.objects.all()
#     serializer_class = KindSerializer
#
# class PageLanguageViewSet(viewsets.ModelViewSet):
#     queryset = PageLanguage.objects.all()
#     serializer_class = PageLanguageSerializer
#
# class ProgrammingLanguageViewSet(viewsets.ModelViewSet):
#     queryset = ProgrammingLanguage.objects.all()
#     serializer_class = ProgrammingLanguageSerializer
#
