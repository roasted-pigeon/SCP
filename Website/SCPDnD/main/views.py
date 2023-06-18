import os

from django.conf import settings
from django.shortcuts import render, redirect
from django.utils.datetime_safe import datetime
import hashlib
import base64


from .forms import UserLoginForm, UserSignupForm, GameCreateForm
from .models import User, Audio, Image, Document, Game


def mainPage(request):
    if 'user' in request.session:
        current_user = request.session['user']
        data = {'current_user': current_user,
                'username': User.objects.get(email=current_user).first_name+" "+User.objects.get(email=current_user).last_name}
        return render(request, 'main/mainPage.html', data)
    else:
        return redirect('login')
    return render(request, 'main/login.html')

def login(request):
    error = ''
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            instance = form.save(commit= False)
            try:
                personToCheck = User.objects.get(email=instance.email)
                salt = base64.urlsafe_b64encode((personToCheck.first_name + personToCheck.last_name + personToCheck.registration_date.strftime("%Y-%m-%d %H:%M:%S")).encode(encoding='UTF-8'))
                t_sha = hashlib.sha512()
                t_sha.update((instance.password_hash + str(salt)).encode(encoding='UTF-8'))
                hashed_password = base64.urlsafe_b64encode(t_sha.digest())
                input_password = hashed_password.decode(encoding='UTF-8')
                if personToCheck.password_hash==input_password:
                    request.session['user'] = personToCheck.email
                    return redirect('main')
                else:
                    error = 'Incorrect data.'
            except:
                error = 'Incorrect data.'
        else:
            error = 'The input data is messed up. Check the format of input.'
    form = UserLoginForm()
    data = {
        'form': form,
        'error': error
    }
    return render(request, 'main/login.html', data)

def signup(request):
    error = ''
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            instance = form.save(commit= False)
            if instance.password_hash==request.POST['password_repeat']:
                password = str(instance.password_hash)
                dateOfRegistration = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                salt = base64.urlsafe_b64encode((instance.first_name+instance.last_name+dateOfRegistration).encode(encoding='UTF-8'))
                t_sha = hashlib.sha512()
                t_sha.update((password + str(salt)).encode(encoding='UTF-8'))
                hashed_password = base64.urlsafe_b64encode(t_sha.digest())
                instance.password_hash= hashed_password.decode(encoding='UTF-8')
                instance.registration_date = dateOfRegistration
                instance.save()
                return redirect('login')
            else:
                error = 'Passwords do not match. Try again.'
        else:
            error = 'The input data is messed up. Check the format of input.'
    form = UserSignupForm()
    data = {
        'form': form,
        'error': error
    }
    return render(request, 'main/signup.html', data)

def logout(request):
    try:
        del request.session['user']
    except:
        return redirect('login')
    return redirect('login')

def showAudio(request):
    if 'user' in request.session:
        current_user = request.session['user']
        audios = Audio.objects.all()
        data = {'current_user': current_user,
                'username': User.objects.get(email=current_user).first_name+" "+User.objects.get(email=current_user).last_name,
                'audios': audios}
        return render(request, 'main/audioLibrary.html', data)
    else:
        return redirect('login')

def uploadAudio(request):
    if 'user' in request.session:
        current_user = request.session['user']
        data = {'current_user': current_user,
                'username': User.objects.get(email=current_user).first_name+" "+User.objects.get(email=current_user).last_name}
        if request.method == 'POST' and request.FILES['audio']:
            audio = request.FILES['audio']
            uploader = User.objects.get(email=current_user)
            upload_date = datetime.now()
            name = audio.name
            file_path = os.path.join(settings.MEDIA_ROOT, 'audio', name)
            with open(file_path, 'wb') as f:
                for chunk in audio.chunks():
                    f.write(chunk)
            audio_record = Audio.objects.create(
                uploader=uploader,
                upload_date=upload_date,
                name=name,
                file_link=file_path
            )
            audio_record.save()
            return redirect('audioLibrary')
        else:
            return render(request, 'main/audioUpload.html', data)
    else:
        return redirect('login')

def showImages(request):
    if 'user' in request.session:
        current_user = request.session['user']
        images = Image.objects.all()
        data = {'current_user': current_user,
                'username': User.objects.get(email=current_user).first_name+" "+User.objects.get(email=current_user).last_name,
                'images':images}
        return render(request, 'main/imageLibrary.html', data)
    else:
        return redirect('login')

def uploadImage(request):
    if 'user' in request.session:
        current_user = request.session['user']
        data = {'current_user': current_user,
                'username': User.objects.get(email=current_user).first_name+" "+User.objects.get(email=current_user).last_name}
        if request.method == 'POST' and request.FILES['image']:
            image = request.FILES['image']
            uploader = User.objects.get(email=current_user)
            upload_date = datetime.now()
            name = image.name
            file_path = os.path.join(settings.MEDIA_ROOT, 'images', name)
            with open(file_path, 'wb') as f:
                for chunk in image.chunks():
                    f.write(chunk)
            image_record = Image.objects.create(
                uploader=uploader,
                upload_date=upload_date,
                name=name,
                file_link=file_path
            )
            image_record.save()
            return redirect('imageLibrary')
        else:
            return render(request, 'main/imageUpload.html', data)
    else:
        return redirect('login')

def account(request):
    if 'user' in request.session:
        current_user = request.session['user']
        print(current_user)
        data = {'current_user': current_user,
                'username': User.objects.get(email=current_user).first_name + " " + User.objects.get(
                    email=current_user).last_name,
                'userObject': User.objects.get(email=current_user)}
        return render(request, 'main/account.html', data)
    else:
        return redirect('login')

def showDocuments(request):
    if 'user' in request.session:
        current_user = request.session['user']
        documents = Document.objects.all()
        data = {'current_user': current_user,
                'username': User.objects.get(email=current_user).first_name+" "+User.objects.get(email=current_user).last_name,
                'documents':documents}
        return render(request, 'main/documentLibrary.html', data)
    else:
        return redirect('login')

def uploadDocument(request):
    if 'user' in request.session:
        current_user = request.session['user']
        data = {'current_user': current_user,
                'username': User.objects.get(email=current_user).first_name+" "+User.objects.get(email=current_user).last_name}
        if request.method == 'POST' and request.FILES['document']:
            document = request.FILES['document']
            uploader = User.objects.get(email=current_user)
            upload_date = datetime.now()
            name = document.name
            file_path = os.path.join(settings.MEDIA_ROOT, 'documents', name)
            with open(file_path, 'wb') as f:
                for chunk in document.chunks():
                    f.write(chunk)
            document_record = Document.objects.create(
                uploader=uploader,
                upload_date=upload_date,
                name=name,
                file_link=file_path
            )
            document_record.save()
            return redirect('documentLibrary')
        else:
            return render(request, 'main/documentUpload.html', data)
    else:
        return redirect('login')

def showGames(request):
    if 'user' in request.session:
        games = []
        current_user = request.session['user']
        try:
            games = Game.objects.filter(creator_id=User.objects.get(email=current_user).user_id)
        except:
            pass
        data = {'current_user': current_user,
                'username': User.objects.get(email=current_user).first_name + " " + User.objects.get(email=current_user).last_name,
                'games': games}
        return render(request, 'main/gameLibrary.html', data)
    else:
        return redirect('login')

def createGame(request):
    error=''
    if 'user' in request.session:
        current_user = request.session['user']
        if request.method == 'POST':
            form = GameCreateForm(request.POST)
            if form.is_valid():
                instance = form.save(commit=False)
                try:
                    game_record = Game.objects.create(
                        title=instance.title,
                        description = instance.description,
                        creation_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        next_session_date = instance.next_session_date.strftime("%Y-%m-%d %H:%M:%S"),
                        creator = User.objects.get(email=current_user),
                    )
                    game_record.save()
                    return redirect('gameLibrary')
                except:
                    error = 'Incorrect data.'
            else:
                error = 'The input data is messed up. Check the format of input.'
        form = GameCreateForm()
        data = {
            'current_user': current_user,
            'username': User.objects.get(email=current_user).first_name + " " + User.objects.get(email=current_user).last_name,
            'form': form,
            'error': error
        }
        return render(request, 'main/gameCreate.html', data)
    else:
        return redirect('login')

def generateTable(width, height):
    table_html = "<table class='gameField'>"
    for i in range(height):
        table_html += "<tr>"
        for j in range(width):
            table_html += "<td class='gameCell'></td>"
        table_html += "</tr>"
    table_html += "</table>"
    return table_html


def tableGenerator(request):
    if request.method == 'POST':
        width = int(request.POST.get('width'))
        height = int(request.POST.get('height'))
        table_html = generateTable(width, height)
        return render(request, 'main/gameScreen.html', {'table_html': table_html})
    return render(request, 'main/createGameScreen.html')