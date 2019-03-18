# a list of imports, they include All my model and forms



from django.shortcuts import render, redirect, get_object_or_404
from .models import WikiModel, ItemModel, UserModel
from .forms import Wikiform, ItemForm, UserForm
from django.contrib.auth.models import User

from django.db.models import Q

# grabs all/list of objects in database and renders on home screen
def index(request):
    if request.user.is_authenticated:
        print(request.user)

        wikiUser = UserModel.objects.get(username=request.user)
        print(wikiUser)
        # filters through the users entries
        allEntries = WikiModel.objects.filter(foreignkeyToUserModel=wikiUser)
    else:

        allEntries = ''
    print(allEntries)
    context = {"allEntries": allEntries}

    return render(request, 'wikiApp/index.html', context)


# imports a form and allos user to create/save a profile in the database
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
# gets a form that allows user to input data into the required fields.

def addPost(request):
    form = Wikiform(request.POST or None)

    tempUser = UserModel.objects.get(username=request.user)
    context = {'Postform': form}

    if request.method == 'POST':
        print(request.method)

        if form.is_valid():
            print("WORKED")
            print(form)
            # form.save()

            # if theres a valid file to upload it creates and saves it the database
            theImage = ''
            if request.FILES:
                theImage = request.FILES["imageUpload"]

            WikiModel.objects.create(title=request.POST["title"], textField=request.POST["textField"],
                                     dateCreated=request.POST["dateCreated"], imageUpload= theImage,
                                     foreignkeyToUserModel=tempUser)



            return redirect('index')

        else:
            print(form.errors)
            context = {
                'errors': form.errors,
                'Postform': form
            }

    return render(request, 'wikiApp/addPost.html', context)
# through the viewpost the add item function allows related objects to be attatched to it via foreignkey variable created in the model

def addItem(request, item_id):
    form = ItemForm(request.POST or None)
    tempUser = get_object_or_404(WikiModel, pk=item_id)
    context = {'Itemform': form}
    if request.method == 'POST':
        print(request.method)

        if form.is_valid():

            ItemModel.objects.create(itemField=request.POST["itemField"],foreignkeyToWiki=tempUser, )

            return redirect('index')

        else:
            print(form.errors)
            context = {
            'errors': form.errors,
            'Itemform': form}



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
    # Grab an exact entry of the GameModel using the primary key
    editExistingPost = get_object_or_404(WikiModel, pk=post_id)

    # Post method
    if request.method == "POST":
        # This will fill in the form with the user's information and use the exact GameModel with primary key
        form = Wikiform(request.POST, instance=editExistingPost)
        if form.is_valid():
            form.save()
        else:
            print("Form is not valid")
        return redirect("index")
    form = Wikiform(instance=editExistingPost)
    context = {
        "Postform": form,
        "post_id": post_id
    }
    return render(request, "wikiApp/editPost.html", context)




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
# grabs all the objects on the data base allows the user to search key words according to title

def listPost(request):
    query = request.GET.get("q", None)
    qs = WikiModel.objects.all()
    if query is not None:
        qs = qs.filter(Q(title__icontains= query))

    context = {

        'post_list': qs

    }

    return render(request, 'wikiApp/listPost.html', context)
# this allows one object to be selected and rendered on the scrreen using the foreignkey created in the model

def viewPost(request, post_id):
    wikiModel = get_object_or_404(WikiModel, pk=post_id)
    print(wikiModel)
    relatedItems = ItemModel.objects.filter(foreignkeyToWiki= wikiModel)
    print(post_id)
    context = {'post_list': wikiModel,
               "relatedItems": relatedItems,
               }
    print(relatedItems)

    return render(request, 'wikiApp/viewPost.html', context)



def postDetails(request,):



    return render(request, 'wikiApp/postDetails.html')


def searchBar(request):
    wikiModelResults = WikiModel.objects.all()
    search_term = ""
    if 'search' in request.GET:
        search_term = request.GET['search']
        wikiModelResults = WikiModel.filter(title__icontains=search_term)

        context={'myList': wikiModelResults, 'search_term': search_term}

    return render(request, 'wikiApp/searchResults.html', context)