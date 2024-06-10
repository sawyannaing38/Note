import re
import os

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def list_categories():
    """
    Returns a list of all folder inside entries
    """
    foldernames, _ = default_storage.listdir("entries")
    return list(foldername for foldername in foldernames)

def list_notes(category):
    """
    Returns a list of all notes for a specific category
    """
    _, filenames = default_storage.listdir(f"entries/{category}")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_note(category, title, content):
    """
    Save a note inside entires / category path
    If the file alreay exists it will delete the original file
    """
    filename = f"entries/{category.title()}/{title.title()}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_note(category,title):
    """
    Get the content of the title
    if file doesn't exist it return None
    """
    try:
        f = default_storage.open(f"entries/{category}/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None
