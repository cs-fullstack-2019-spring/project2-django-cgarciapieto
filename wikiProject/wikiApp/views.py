from django.shortcuts import render, redirect, get_object_or_404
from .models import WikiModel, ItemModel
from .forms import Wikiform, ItemForm, UserForm
from django.contrib.auth.models import User


# grabs all/list of objects in database and renders on home screen
def index(request):
    allEntries = WikiModel.objects.all
    context = {"allEntries": allEntries}

    return render(request, 'wikiApp/index.html', context)


# grabs the Users post by ID and displays user entries
def postDetails(request, post_id):



    return render(request, 'wikiApp/addPost.html',context)





# imports newUser ModelForm and POST to the database if all fields are valid.
def newUser(request):
    if request.method == ('POST' or None):

        print(request.method)
        form = UserForm(request.POST or None)
        context = {
            'errors': form.errors,
            'form': form
        }
        if form.is_valid():
            print("IT WORKED")
            form.save()
            User.objects.create_user(request.POST["username"],
                                     "",
                                     request.POST["password1"])
            return redirect('index')
        else:
            context = {
                'errors': form.errors,
                'form': form
            }
    return render(request, 'wikiApp/newUser.html', context)


def addPost(request):

    form = Wikiform(request.POST or None)
    context = {'Postform': form}

    if request.method == 'POST':
        print(request.method)

        if form.is_valid():
            print("WORKED")
            # form.save()
            WikiModel.objects.create(title = request.POST["title"],
                                textField = request.POST["textField"],
                                dateCreated =request.POST['dateCreated'],
                                imageUpload =request.POST['imageUpload'])
            return redirect('index')

        else:
            context = {
                'errors': form.errors,
                'Postform': form
            }

    return render(request, 'wikiApp/addPost.html', context)


def addItem(request):
    form = ItemForm()
    context = {
        'Itemform': form
    }
    return render(request, 'wikiApp/addItem.html', context)


def deletePost(request, item_id):
    return render(request, 'wikiApp/deletePost.html')


def deleteItem(request, item_id):
    return render(request, 'wikiApp/deleteItem.html')


def editPost(request, post_id):
    return render(request, 'wikiApp/editPost.html')


def editItem(request, item_id):
    return render(request, 'wikiApp/editItem.html')


def listPost(request):
    return render(request, 'wikiApp/listPost.html')


def viewPost(request):
    return render(request, 'wikiApp/listPost.html')
