from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render

class NewTaskForm(forms.Form):
    task = forms.CharField(label="New Task")
    priority = forms.IntegerField(label="Priority", min_value=1, max_value=5)

# Create your views here.
def index(request):
    if "tasks" not in request.session:
        request.session["tasks"] = []
    return render(request, "tasks/index.html", {
        "tasks": request.session["tasks"]
    })

def addTask(request):
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            newTask = {"task": form.cleaned_data["task"], "priority": form.cleaned_data["priority"]}
            request.session["tasks"] += newTask
            request.session.save()
            return HttpResponseRedirect(reverse("tasks:index"))
        else:
            return render(request, "tasks/addTask.html", {
                "form": form
            })

    return render(request, "tasks/addTask.html", {
        "form": NewTaskForm()
    })






# backup
# from django import forms
# from django.shortcuts import render

# tasks = ["Work", "Gym", "Code"]

# class NewTaskForm(forms.Form):
#     task = forms.CharField(label="New Task")
#     priority = forms.IntegerField(label="Priority", min_value=1, max_value=10)

# # Create your views here.
# def index(request):
#     return render(request, "tasks/index.html", {
#         "tasks": tasks
#     })

# def addTask(request):
#     if request.method == "POST":
#         form = NewTaskForm(request.POST)
#         if form.is_valid():
#             tasks.append(form.cleaned_data["task"])
#         else:
#             return render(request, "tasks/addTask.html", {
#                 "form": form
#             })

#     return render(request, "tasks/addTask.html", {
#         "form": NewTaskForm()
#     })

