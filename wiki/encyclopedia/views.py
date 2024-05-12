from django.shortcuts import render
import markdown2
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
import random
from .util import get_entry, save_entry, list_entries

class NewEntryForm(forms.Form):
    newTitle = forms.CharField(label="Entry Title")
    newContent = forms.CharField(label="Entry Content", widget=forms.Textarea)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": list_entries()
    })

def entry(request, entryTitle):

    entryContent = get_entry(entryTitle)
    
    if entryContent:
        entryContent = markdown2.markdown(entryContent)
        return render(request, "encyclopedia/entry.html", {
            "entryTitle": entryTitle,
            "entryContent": entryContent,
        })

    else:
        return render(request, "encyclopedia/not_found.html", {
            "entryTitle": entryTitle,
        })

def search(request):
    if request.method == 'GET':
        search_query = request.GET.get('q')

        all_entries = list_entries()

        if search_query in all_entries:
            entryContent = markdown2.markdown(get_entry(search_query))
            return render(request, "encyclopedia/entry.html", {
                "entryTitle": search_query,
                "entryContent": entryContent,
            })

        else:
        
            search_results = [
                entry for entry in all_entries
                if search_query.lower() in entry.lower()
            ]

            if not search_results:
                return render(request, "encyclopedia/not_found.html", {
                "entryTitle": search_query,
            })

            return render(request, "encyclopedia/search_results.html", {
                "entries": search_results
            })

def new(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new.html", {
            "form": NewEntryForm()
        })
    
    else:
        form = NewEntryForm(request.POST)
        if form.is_valid():
            newTitle = form.cleaned_data["newTitle"]
            newContent = form.cleaned_data["newContent"]
            if newTitle in list_entries():
                return render(request, "encyclopedia/new.html", {
                    "nameUnavaiable": True,
                    "form": NewEntryForm()
                })
            else:
                save_entry(newTitle, newContent)
                return HttpResponseRedirect(f'/{newTitle}')
        else:
            return render(request, "encyclopedia/new.html",{
                    "invalid": True,
                    "form": NewEntryForm()
                })
        
def edit(request, entryTitle):
    if request.method == "GET":
        entryContent = get_entry(entryTitle)
        return render(request, "encyclopedia/edit.html", {
                "entryTitle": entryTitle,
                "entryContent": entryContent,
            })
    else:
        entryContent = request.POST.get('entryContent')
        save_entry(entryTitle, entryContent)
        return HttpResponseRedirect(f'/{entryTitle}')


def randomEntry(request):
    all_entries = list_entries()
    if all_entries:
        random_entry = random.choice(all_entries)
        return HttpResponseRedirect(f'/{random_entry}')
    else:
        return HttpResponseRedirect('')