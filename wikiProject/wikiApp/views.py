from django.shortcuts import render, redirect, get_object_or_404
from .models import WikiModel, ItemModel, UserModel
from .forms import Wikiform, ItemForm, UserForm
from django.contrib.auth.models import User
from django.views.static import serve
from django.db.models import Q

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

    tempUser = UserModel.objects.get(username=request.user)
    context = {'Postform': form}

    if request.method == 'POST':
        print(request.method)

        if form.is_valid():
            print("WORKED")
            print(form)
            # form.save()
            theImage = ''
            if request.FILES:
                theImage = request.FILES["imageUpload"]

            WikiModel.objects.create(title=request.POST["title"], textField=request.POST["textField"],
                                     dateCreated=request.POST["dateCreated"], imageUpload= theImage,
                                     foreignkeyToUserModel=tempUser)

            #         title = models.CharField(max_length=100)
            # textField = models.TextField(max_length=1000)
            # dateCreated = models.DateField(default=timezone.now)
            # imageUpload = models.ImageField(upload_to="media", null = True, blank=True)
            # foreignkeyToUserModel

            return redirect('index')

        else:
            print(form.errors)
            context = {
                'errors': form.errors,
                'Postform': form
            }

    return render(request, 'wikiApp/addPost.html', context)


def addItem(request, item_id):
    form = ItemForm(request.POST or None)
    tempUser = get_object_or_404(WikiModel, pk=item_id)
    context = {'Itemform': form}
    if request.method == 'POST':
        print(request.method)

        if form.is_valid():
            theImage = ''
            if request.FILES:
                theImage = request.FILES["imageUpload"]
            ItemModel.objects.create(itemField=request.POST["itemField"],
                                 imageUpload=theImage,foreignkeyToWiki=tempUser, )

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


def listPost(request):
    query = request.GET.get("q", None)
    qs = WikiModel.objects.all()
    if query is not None:
        qs = qs.filter(Q(title__icontains= query))

    context = {

        'post_list': qs

    }

    return render(request, 'wikiApp/listPost.html', context)


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


# grabs the Users post by ID and displays user entries
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