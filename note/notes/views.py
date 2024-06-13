from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
import os
from . import util
import markdown

# Create your views here.

# For main page
def index(request):
    
    categories = util.list_categories()

    return render(request, "notes/index.html", {
        "categories" : categories
    })

# For adding note
def add(request):

    if request.method == "GET":
        return render(request, "notes/add.html", {
            "title" : "",
            "category" : "",
            "content" : ""
        })
    
    # For post method
    category = request.POST.get("category")
    title = request.POST.get("title")
    content = request.POST.get("content").replace("\n\n", "\n").replace("\r\n", "\n")

    if os.path.exists(f"{settings.BASE_DIR}/entries/{category}"):
        # Getting all the files for tht category
        notes = util.list_notes(category)

        if title.title() in notes:
            return render(request, "notes/add.html", {
                "title" : title,
                "category" : category,
                "content" : content,
                "message" : "Note with that name already esists",
                "exists" : True
            })
    # Save that content
    util.save_note(category, title, content)

    return HttpResponseRedirect(reverse("note", args=[category, title]))

# For getting files for specific category
def entry(request, category):

    notes = util.list_notes(category)

    if notes:
        title = notes[0]
       
        # Get the content for the first note
        content = util.get_note(category, notes[0])
        return render(request, "notes/entry.html", {
            "notes" : notes,
            "category" : category,
            "title" : title,
            "content" : markdown.markdown(content)
        })
    
    else:
        return render(request, "notes/apology.html", {
            "message" :f"There is not note for {category}."
        })

# For Getting content of the specific file
def note(request, category, title):

    content = util.get_note(category, title).replace("\n\n", "\n").replace("\r\n", "\n")
    notes = util.list_notes(category)

    return render(request, "notes/entry.html", {
        "notes" : notes,
        "category" : category,
        "content" : markdown.markdown(content),
        "title" : title
    })

# For editing page
def edit(request, category, title):
    if request.method == "POST":

        # Get the content
        content = request.POST.get("content").replace("\n\n", "\n").replace("\r\n", "\n")

        # Save the changes
        util.save_note(category,title,content)

        return HttpResponseRedirect(reverse("note", args=[category, title]))

    content = util.get_note(category, title)

    return render(request, "notes/edit.html", {
        "category" : category,
        "title" : title,
        "content" : content
    })

        

# For removing
def remove(request, category, title):
    os.remove(f"{settings.BASE_DIR}/entries/{category}/{title}.md")

    # Getting all file inside that category
    folders = util.list_notes(category)

    if not folders:
        return HttpResponseRedirect(reverse("index"))
    
    else:
        return HttpResponseRedirect(reverse("entry", args=[category]))