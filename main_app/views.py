from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from .models import Cat, CatToy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

#### USER ####


def login_view(request):
    if request.method == 'POST':
        # try to log the user in
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            u = form.cleaned_data['username']
            p = form.cleaned_data['password']
            user = authenticate(username=u, password=p)
            if user is not None:
                if user.is_active:
                    login(request, user) # log the user in by creating a session
                    return HttpResponseRedirect('/user/'+u)
                else:
                    print('The account has been disabled.')
        else: # it was a GET request so send the empty login form
            print('The username and/or password is incorrect.')
    else:
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/cats')

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect('/user/'+str(user))
        else:
            return HttpResponse('<h1>Try Again</h1>')
    else:
        form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})

@login_required
def profile(request, username):
    user = User.objects.get(username=username)
    cats = Cat.objects.filter(user=user)
    return render(request, 'profile.html', {'username': username, 'cats': cats})

#### CATS ####
# Django will make a create cat form for us!
@method_decorator(login_required, name='dispatch')
class CatCreate(CreateView):
    model = Cat
    fields = '__all__'
    success_url = '/cats/'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        print('!!!!!! SELF.OBJECT', self.object)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect('/cats')


class CatUpdate(UpdateView):
    model = Cat
    fields = ['name', 'breed', 'description', 'age']

    def form_valid(self, form):  # this will allow us to catch the pk to redirect to show page
        # don't post to the db until we say so
        self.object = form.save(commit=False)
        self.object.save()
        return HttpResponseRedirect('/cats/'+str(self.object.pk))


class CatDelete(DeleteView):
    model = Cat
    success_url = '/cats'


def cats_index(request):
    # Get all cats from the db
    cats = Cat.objects.all()
    return render(request, 'cats/index.html', {'cats': cats})


def cats_show(request, cat_id):
    cat = Cat.objects.get(id=cat_id)
    toys = CatToy.objects.all()
    return render(request, 'cats/show.html', {'cat': cat, 'toys': toys})


#### CATTOYS ####

def cattoys_index(request):
    cattoys = CatToy.objects.all()
    return render(request, 'cattoys/index.html', {'cattoys': cattoys})

def cattoys_show(request, cattoy_id):
    cattoy = CatToy.objects.get(id=cattoy_id)
    return render(request, 'cattoys/show.html', {'cattoy': cattoy})

class CatToyCreate(CreateView):
    model = CatToy
    fields = '__all__'
    success_url = '/cattoys'

class CatToyUpdate(UpdateView):
    model = CatToy
    fields = ['name', 'color']
    success_url = '/cattoys'

class CatToyDelete(DeleteView):
    model = CatToy
    success_url = '/cattoys'

def assoc_toy(request, cat_id, toy_id):
    Cat.objects.get(id=cat_id).cattoys.add(toy_id)
    return HttpResponseRedirect('/cats/'+str(cat_id))

def unassoc_toy(request, cat_id, toy_id):
    Cat.objects.get(id=cat_id).cattoys.remove(toy_id)
    return HttpResponseRedirect('/cats/'+str(cat_id))

#### DEFAULT ####

def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


# def cats_index(request):
#     return render(request, 'cats/index.html', {'cats': cats})

# class Cat:
#     def __init__(self, name, breed, description, age):
#         self.name = name
#         self.breed = breed
#         self.description = description
#         self.age = age


# cats = [
#     Cat('Lolo', 'tabby', 'foul little demon', 3),
#     Cat('Sachi', 'tortoise shell', 'diluted tortoise shell', 0),
#     Cat('Raven', 'black tripod', '3 legged cat', 4)
# ]
