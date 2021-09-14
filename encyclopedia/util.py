import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import random


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def list_entries_lower():
    names = []
    for name in list_entries():
        names.append(name.lower())
    return names


def list_sub_entries(title):
    _, filenames = default_storage.listdir("entries")
    entries = list(sorted(re.sub(r"\.md$", "", filename)
                          for filename in filenames if filename.endswith(".md")))
    sub_entries = []
    for entry in entries:
        if title.lower() in entry.lower():
            sub_entries.append(entry)
    return sub_entries


def get_random_entry(*exclusions):
    entries_without_none = list_entries()
    for exclusion in exclusions:
        if exclusion in entries_without_none:
            entries_without_none.remove(exclusion)
    return random.choice(entries_without_none)


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    content = re.sub(r'\s\n+', '\n', content)
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None


def get_entry_title(title):
    for entry in list_entries():
        if title.lower() == entry.lower():
            return entry
    return None
