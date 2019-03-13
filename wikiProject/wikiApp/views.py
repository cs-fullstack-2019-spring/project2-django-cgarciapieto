from django.shortcuts import render, redirect, get_object_or_404
from .models import WikiModel, ItemModel, UserModel
from .forms import Wikiform, ItemForm, UserForm
from django.contrib.auth.models import User


# grabs all/list of objects in database and renders on home screen
def index(request):
    if request.user.is_authenticated:
        print(request.user)

        wikiUser = UserModel.objects.get(username=request.user)
        print(wikiUser)

        allEntries = WikiModel.objects.filter(foreignkeyToUserModel=wikiUser)
    else:

        allEntries = ''
    print(allEntries)
    context = {"allEntries": allEntries}

    return render(request, 'wikiApp/index.html', context)


# imports newUser ModelForm and POST to the database if all fields are valid.
def newUser(request):
    form = UserForm(request.POST or None)
    context = {'Userform': form}

    if request.method == 'POST':
        print(request.method)

        if form.is_valid():
            print("WORKED")

            User.objects.create_user(request.POST["username"], "", request.POST["password1"])
            form.save()
            return redirect('index')

        else:
            context = {
                'errors': form.errors,
                'Userform': form
            }

    return render(request, 'wikiApp/newUser.html', context)



def addPost(request):
    form = Wikiform(request.POST or None)
    context = {'Postform': form}

    if request.method == 'POST':
        print(request.method)

        if form.is_valid():
            print("WORKED")

            WikiModel.objects.create(title=request.POST["title"],
                                     textField=request.POST["textField"],
                                     dateCreated=request.POST['dateCreated'],
                                     imageUpload=request.POST['imageUpload'])
            form.save()
            return redirect('index')

        else:
            context = {
                'errors': form.errors,
                'Postform': form
            }

    return render(request, 'wikiApp/addPost.html', context)


def addItem(request):
    form = ItemForm()
    if form.is_valid():
        ItemModel.objects.create(itemField=request.POST["itemField"],
                                 imageUpload2=request.POST["imageUpload2"])
        form.save()
    context = {
        'Itemform': form
    }
    return render(request, 'wikiApp/addItem.html', context)


def deletePost(request, post_id):
    deleteWikiPost = get_object_or_404(WikiModel, pk=post_id)
    deleteWikiPost.delete()
    return redirect('index')


def deleteItem(request, item_id):
    deleteThisItem = get_object_or_404(ItemModel, pk=item_id)
    deleteThisItem.delete()
    return redirect('index')
    # return render(request, 'wikiApp/deleteItem.html')


def editPost(request, post_id):
    editExistingPost = get_object_or_404(WikiModel, pk=post_id)
    if request.method == "POST":
        form = Wikiform(request.POST, instance=editExistingPost)
        if form.is_valid():
            form.save()
        else:
            print("form is not valid")

        return redirect('index')

    return render(request, 'wikiApp/editPost.html')


def editItem(request, item_id):
    editThisitem = get_object_or_404(ItemModel, pk=item_id)
    if request.method == "POST":

        form = ItemForm(request.POST, instance=editThisitem)
        if form.is_valid():
            form.save()
        else:
            print("form is not valid")

        return redirect('index')

    return render(request, 'wikiApp/editItem.html')


def listPost(request):

    # # This will put all the user's information from the HTML page into this new form variable
    # form = Wikiform(request.POST)
    # # This puts the logged in user entry into the variable collector
    # userPost = UserModel.objects.get(username=request.user)
    #
    #
    # if form.is_valid():
    #
    #     WikiModel.objects.create(title=request.POST["title"],
    #                              textField=request.POST["textField"],
    #                              dateCreated=request.POST['dateCreated'],
    #                              imageUpload=request.POST['imageUpload'])
    #     form.save()
    #     return redirect('index')
    # else:
    #     context = {"form":form, "errors":form.errors}

        return render(request, 'wikiApp/listPost.html',)



def viewPost(request, post_id):
    post_list = get_object_or_404(WikiModel, pk=post_id)


    context = {'post_list': post_list}

    return render(request, 'wikiApp/viewPost.html', context)


# grabs the Users post by ID and displays user entries
def postDetails(request, post_id):
    return render(request, 'wikiApp/postDetails.html')
