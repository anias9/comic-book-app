from django.shortcuts import render, redirect
from .forms import ComicForm, ElementsForm
from django.http import Http404
from .models import Comic, User, Elementy, Profil
from django.forms import modelformset_factory
from django.views.generic import CreateView,  UpdateView
from PIL import Image, ImageDraw, ImageFont, ImageFile
import uuid


from django.contrib.sites.models import Site

"""
TODO

Wyszukiwanie komiksów, 
like i dislike,
ulubione

"""

def home(request):
    last_comics = Comic.objects.filter(publiczny=1)[:1]
    return render(request, 'home.html', {'last_comics':last_comics})

def postacie(request):
    return render(request, 'postacie.html')


def sample(request):
    return render(request, 'sample.html')

def moje_komentarze(request):
    comic = Comic.objects.all()
    return render(request, 'moje_komentarze.html')


def detail(request, comic_id):
    try:
        comic = Comic.objects.get(pk = comic_id)
    except Comic.DoesNotExist:
        raise Http404("Podany komiks nie istnieje")
    return render(request, 'detail.html', {'comic': comic})


def uzytkownicy(request):
    users = User.objects.filter(is_superuser=0)
    comics = Comic.objects.all()
    context = {
        'users': users,
        'comics': comics,
    }
    return render(request, 'uzytkownicy.html', context)


def profil(request, owner_id):
    try:
        user_id = owner_id
        owner = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        raise Http404("Podany użytkownik nie istnieje")
    comics = Comic.objects.filter(owner_id=user_id)
    context = {
        'owner': owner,
        'comics': comics,
    }
    return render(request, 'profil.html', context)


def delete_comic(request, comic_id):
    if request.user.is_authenticated:
        comic = Comic.objects.get(pk=comic_id)
        elementy_id = comic.element.id
        elementy = Elementy.objects.get(pk = elementy_id)
        comic.delete()
        elementy.delete()
    return render(request, 'delete_comic.html')


def delete_elementy(request, elementy_id):
        elementy = Elementy.objects.get(pk=elementy_id)
        elementy.delete()
        return redirect('rysuj')


# dodanie elementów komiksów do Elementy
def rysuj(request):
    form = ElementsForm(request.POST, request.FILES)

    if request.method == 'POST':
        form.instance.background = request.POST.get('background', None)
        form.instance.character1 = request.POST.get('character1', None)
        form.instance.character2 = request.POST.get('character2', None)
        form.instance.chat1 = request.POST.get('chat1', None)
        form.instance.chat2 = request.POST.get('chat2', None)
        form.instance.text1 = request.POST.get('text1', None)
        form.instance.text2 = request.POST.get('text2', None)

        if form.is_valid():
            form.save()

            return redirect('stworzone', elementy_id=form.instance.id)
        else:
            form = ElementsForm()

    return render(request, 'rysuj.html', {
        'form': form})


#stworzenie komiksów z wybranych Elementów
def stworzone(request, elementy_id):
    elementy = Elementy.objects.get(pk = elementy_id)

    im1 = Image.open(elementy.background)
    img1 = im1.resize((600,600))
    im2 = Image.open(elementy.character1)
    img2 = im2.resize((250,250))
    im3 = Image.open(elementy.character2)
    img3 = im3.resize((250,250))
    im4 = Image.open(elementy.chat1)
    img4 = im4.resize((280,280))
    im5 = Image.open(elementy.chat2)
    img5 = im5.resize((280,280))

    img1.paste(img2, (0, 350), img2)
    img1.paste(img3, (330, 350), img3)
    img1.paste(img4, (30, 50), img4)
    img1.paste(img5, (290, 50), img5)

    t = ''
    t2 = ''

    if len(elementy.text1) <= 70:
        for i, c in enumerate(elementy.text1):
            if i == 18 or i == 36 or i == 54 or i == 70:
                if c == ' ' or c == ',' or c == '.':
                    t += '\n'
                else:
                    t += '-\n'
                t += c
            else:
                t += c
    else:
        t = "Wprowadzony\ntekst jest za dlugi.\nProszę spróbować\nponownie"

    if len(elementy.text2) <= 70:
        for i, c in enumerate(elementy.text2):
            if i == 18 or i == 36 or i == 54 or i == 70:
                if c == ' ' or c == ',' or c == '.':
                    t2 += '\n'
                else:
                    t2 += '-\n'
                t2 += c
            else:
                t2 += c
    else:
        t2 = "Wprowadzony\ntekst jest za dlugi.\nProszę spróbować\nponownie"

    draw = ImageDraw.Draw(img1)
    font = ImageFont.truetype('/home/ichiraku/Downloads/abhaya-libre/AbhayaLibre-Regular.ttf', 25)
    draw.text((60, 100), t, (0, 0, 0), font=font)
    draw.text((320, 100), t2, (0, 0, 0), font=font)

    filename = str(uuid.uuid4()) + '.png'
    img1.save('media/' + filename)
    img1 = filename
    elementy.background = img1

    form = ComicForm(request.POST, request.FILES)

    if request.method == 'POST':

        form.instance.owner = request.user
        form.instance.comics = elementy.background
        form.instance.element = elementy


        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            form = ComicForm()

    context = {
        'form': form,
        'elementy': elementy,
    }
    return render(request, 'stworzone.html', context)



def stworz(request, elementy_id):
    elementy = Elementy.objects.get(pk = elementy_id)
    form = ComicForm(request.POST, request.FILES)

    if request.method == 'POST':

        form.instance.owner = request.user

        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            form = ComicForm()

    context = {
        'form': form,
        'elementy': elementy,
    }
    return render(request, 'stworz.html', context)



def najnowsze(request):
    last_comics = Comic.objects.filter(publiczny=1)[:5]
    return render(request, 'najnowsze.html', {'last_comics':last_comics},)


def kolekcja(request):
    all_comics = Comic.objects.filter(publiczny=1)
    return render(request, 'kolekcja.html',  {'all_comics' : all_comics,})



class ComicCreate(CreateView):
    model = Comic
    fields = ['comics', 'title', 'publiczny']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(ComicCreate, self).form_valid(form)





