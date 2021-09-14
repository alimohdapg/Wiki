from django.shortcuts import render
from . import util
import markdown2
from django.urls import reverse
from django.http import HttpResponseRedirect
from django import forms
import re


class SearchForm(forms.Form):
    page_name = forms.CharField(label="Search Encyclopedia", widget=forms.TextInput(
        attrs={'style': 'width: 90%;', 'id': 'search_form'}))


class NewPageForm(forms.Form):
    page_title = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Page Title', 'class': 'form-control', 'style': 'width: 40%;'}))
    markdown_area = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': 'Markdown Content', 'class': 'form-control', 'style': 'width: 90%;'}))


class EditPageForm(forms.Form):
    markdown_area = forms.CharField(label="", widget=forms.Textarea(
        attrs={'placeholder': 'Markdown Content', 'class': 'form-control', 'style': 'width: 90%;'}))


def index(request):
    if request.method == "POST":
        # Take in the data the user submitted and save it as form
        form = SearchForm(request.POST)
        # Check if form data is valid (server-side)
        if form.is_valid():
            # Isolate the task from the 'cleaned' version of form data
            page_name = form.cleaned_data["page_name"]
            # Redirect user to list of tasks
            # return HttpResponseRedirect(reverse("tasks:index"))
            if util.get_entry_title(page_name) != None:
                details = {
                    "name": util.get_entry_title(page_name),
                    "body": markdown2.markdown(util.get_entry(page_name)),
                    "form": SearchForm(),
                    "random_page": util.get_random_entry("None")
                }
                return HttpResponseRedirect(page_name, (details))
            else:
                details = {
                    "sub_entries": util.list_sub_entries(page_name),
                    "form": SearchForm(),
                    "random_page": util.get_random_entry("None")
                }
                return render(request, "encyclopedia/search.html", details)
        else:
            # If the form is invalid, re-render the page with existing information.
            return render(request, "encyclopedia/index.html", {
                "entries": util.list_entries(),
                "form": form,
                "random_page": util.get_random_entry("None")
            })
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": SearchForm(),
        "random_page": util.get_random_entry("None")
    })


def new_page(request):
    if request.method == "POST":
        # Take in the data the user submitted and save it as form
        form = NewPageForm(request.POST)
        # Check if form data is valid (server-side)
        if form.is_valid():
            # Isolate the task from the 'cleaned' version of form data
            page_title = form.cleaned_data["page_title"]
            markdown_area = form.cleaned_data["markdown_area"]
            # Redirect user to list of tasks
            # return HttpResponseRedirect(reverse("tasks:index"))
            if page_title.lower() in util.list_entries_lower():
                return render(request, "encyclopedia/new_page.html", {
                    "title_and_markdown_form": form,
                    "error": "Page Exists Already",
                    "form": SearchForm(),
                    "random_page": util.get_random_entry("None")
                })
            else:
                util.save_entry(page_title, markdown_area)
                details = {
                    "name": util.get_entry_title(page_title),
                    "body": markdown2.markdown(util.get_entry(page_title)),
                    "form": SearchForm(),
                    "random_page": util.get_random_entry("None")
                }
                return HttpResponseRedirect(page_title, (details))
        else:
            # If the form is invalid, re-render the page with existing information.
            return render(request, "encyclopedia/new_page.html", {
                "title_and_markdown_form": form,
                "error": "Invalid Input",
                "form": SearchForm(),
                "random_page": util.get_random_entry("None")
            })
    return render(request, "encyclopedia/new_page.html", {
        "title_and_markdown_form": NewPageForm(),
        "error": "",
        "form": SearchForm(),
        "random_page": util.get_random_entry("None")
    })


def edit(request, name):
    if request.method == "POST":
        # Take in the data the user submitted and save it as form
        form = EditPageForm(request.POST)
        # Check if form data is valid (server-side)
        if form.is_valid():
            # Isolate the task from the 'cleaned' version of form data
            page_title = name
            markdown_area = form.cleaned_data["markdown_area"]
            # Redirect user to list of tasks
            # return HttpResponseRedirect(reverse("tasks:index"))
            if page_title.lower() in util.list_entries_lower():
                util.save_entry(page_title, markdown_area)
                details={
                    "name": util.get_entry_title(page_title),
                    "body": markdown2.markdown(util.get_entry(page_title)),
                    "form": SearchForm(),
                    "random_page": util.get_random_entry("None", name)
                }
                return HttpResponseRedirect(f"/wiki/{name}", (details))
            else:
                return render(request, "encyclopedia/edit.html", {
                    "name": name,
                    "markdown_form": form,
                    "error": "Page Not Found",
                    "form": SearchForm(),
                    "random_page": util.get_random_entry("None", name)
                })
        else:
            # If the form is invalid, re-render the page with existing information.
            return render(request, "encyclopedia/edit.html", {
                "name": name,
                "markdown_form": form,
                "error": "Invalid Input",
                "form": SearchForm(),
                "random_page": util.get_random_entry("None", name)
            })
    return render(request, "encyclopedia/edit.html", {
        "name": name,
        "markdown_form": EditPageForm(initial={'markdown_area': util.get_entry(name)}),
        "error": "",
        "form": SearchForm(),
        "random_page": util.get_random_entry("None", name)
    })


def title(request, name):
    if util.get_entry_title(name) == None:
        details = {
            "name": "None",
            "body": markdown2.markdown(util.get_entry(None)),
            "form": SearchForm(),
            "random_page": util.get_random_entry("None", name)
        }
    else:
        details = {
            "name": util.get_entry_title(name),
            "body": markdown2.markdown(util.get_entry(name)),
            "form": SearchForm(),
            "random_page": util.get_random_entry("None", name)
        }
    return render(request, "encyclopedia/entry.html", details)
