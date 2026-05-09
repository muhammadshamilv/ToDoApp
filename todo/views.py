from django.shortcuts import render
from .models import Task

# REST FRAMEWORK IMPORTS
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import TaskSerializer


# FRONTEND VIEW
def home(request):
    if request.method == "POST":
        title = request.POST.get('title')
        
        if title:
            Task.objects.create(title=title)
        
    tasks = Task.objects.all()
    return render(request, 'home.html', {'tasks': tasks})


# API VIEW
@api_view(['GET', 'POST'])
def task_list(request):
    
    # Get all Task
    if request.method == 'GET':
        tasks = Task.objects.all()
        
        serializer = TaskSerializer(tasks, many=True)
        
        return Response(serializer.data)
    
    # Create Task
    elif request.method == 'POST':
        
        serializer = TaskSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            
            return Response(serializer.data)
        
        return Response(serializer.errors)
    

@api_view(['GET', 'PUT', 'DELETE'])
def task_detail(request, pk):
    try:
        task = Task.objects.get(id=pk)
    except Task.DoesNotExist:
        return Response({"error": "Task Not Found"})
    
    #Get Single Taks
    if request.method == 'GET':
        serializer = TaskSerializer(task)
        return Response(serializer.data)
    
    # Update Task
    elif request.method == 'PUT':
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data) 
        return Response(serializer.errors)
    
    #Delete Task
    elif request.method == 'DELETE':
        task.delete()
        return Response({"message": "Task Deleted"})
    