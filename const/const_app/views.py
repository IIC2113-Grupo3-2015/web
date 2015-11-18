from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, JsonResponse
from django.template.context_processors import csrf
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Post, Comment, UserProfile
from django.utils import timezone
import pygal
from pygal.style import Style
import json
from random import randint
import psycopg2
import requests
from django.views.decorators.csrf import csrf_exempt

def generic_delete(request, Model, param):
    if request.method == 'POST':
        model_id = request.POST.get(param)
        model = Model.objects.get(id = model_id)
        if request.user == model.user:
            model.delete()
    return HttpResponse(
                json.dumps({'ok': 1}),
                content_type="application/json"
                )
def index(request):
    # Este método es llamado cada vez que se necesita ir a la página de
    # bienvenida. No necesita login.
    return render(request, 'const/index.html', {})
    # Después de la llamada, la página es cambiada por la de bienvenida.

def main_page(request):
    # Este método envía a la página principal de todo usuario, donde se muestran
    # las últimas novedades. Necesita login.
    pass
    # El método renderea la página junto a un diccionario, en el que
    # se envían los valores requeridos por la página desde la base de datos.

@login_required
def user_profile(request, user_id):
    # Este método es llamado cuando se quiere acceder al perfil de un usuario.
    # Necesita de un usuario con login que coincida con la url.
    # Además el id del usuario debe estar explícito en la url
    user = request.user
    required_user = User.objects.get(id = user_id)
    candidates = User.objects.all()
    candidates_posts = []
    for candidate in candidates:
        if candidate.username != 'admin' and candidate.userprofile.role == 'candidate':
            for post in candidate.post_set.all():
                candidates_posts.append(post)
    context = {'user': user, 'posts': candidates_posts}
    if user.id != int(user_id) or user.userprofile.role == 'candidate':
        return HttpResponse("Error")
    return render(request, 'const/profile.html', context)
    # El método te lleva al perfil del usuario

@login_required
def candidate_profile_page(request, user_id):
    # Este método se llama cuando se quiere ir a la página de un candidato
    # usando una cuenta de candidato. Se debe estar logeado con el usuario
    # respectivo.
    user = request.user
    required_user = User.objects.get(id = user_id)
    if required_user.userprofile.role != 'candidate':
        return HttpResponse("Error")

    print(request.user.id)
    print(required_user.id)
    is_self_user = required_user.id == request.user.id
    posts = required_user.post_set.all()

    g = graph(required_user.username)

    #cur.close()
    #conn.close()

    context = {'required_user': required_user, 'is_self_user': is_self_user,
                'posts': posts, 'graph': g}
    return render(request, 'const/candidate.html', context)
    # El método te lleva al perfil del usuario candidato

@login_required
def view_post(request, post_id):
    post = Post.objects.get(id = post_id)
    username = post.post_author.username
    comments = post.comment_set.all()
    has_comments = len(comments) > 0
    print("HC", has_comments)
    context = {'post': post, 'username': username, 'comments': comments,
            'has_comments': has_comments}
    return render(request, 'const/post.html', context)

@login_required
def create_post(request):
    # El usuario candidato ejecuta esta función cuando añade un nuevo post
    # en su entrada. El usuario que realiza el request queda registrado
    # como autor del post. Los datos son pasados mediante POST HTTP.
    if request.method == 'POST':
        content = request.POST.get('content')
        title = request.POST.get('title').replace("\n", " ")

        if request.user.userprofile.role == 'candidate':
            myPost = Post(post_title = title,
                        post_text = content,
                        post_author = request.user,
                        pub_date = timezone.now())
            myPost.save()
        userImage = request.user.userprofile.picture.url
        return HttpResponse(
                        json.dumps({}),
                        content_type="application/json"
                            )
    # El post es guardado en la base de datos

@login_required
def create_post_page(request):
    # El usuario candidato ejecuta esta función cuando añade un nuevo post
    # en su entrada. El usuario que realiza el request queda registrado
    # como autor del post. Los datos son pasados mediante POST HTTP.
    if request.user.userprofile.role != 'candidate':
        return HttpResponse("Error")
    context = {'user': request.user}
    return render(request, 'const/createpost.html', context)
    # El post es guardado en la base de datos

def delete_comment(request):
    # El usuario candidato ejecuta esta función cuando elimina un comentario
    # en un post. El usuario que hace el request debe ser el dueño del post.
    # Los datos son pasados mediante POST HTTP.
    return generic_delete(request, Comment, 'comment_id')
    # Se elimina el post de la DB.

@login_required
def create_comment(request):
    # El usuario ejecuta esta función al comentar en un post de un candidato.
    # Se genera un comentario asociado al post visible para todos los usuarios.
    # Se requiere login. Los valores se pasan mediante POST HTTP.
    if request.method == 'POST':
        post = Post.objects.get(id = request.POST.get('pid'))
        content = request.POST.get('content').replace("\n", "<br>")
        myComment = Comment(post = post,
                    content = content,
                    user = request.user)
        myComment.save()
        cid = myComment.id
        userImage = request.user.userprofile.picture.url
    return HttpResponse(
                    json.dumps({'cont': content, 'userImage': userImage, 'cid': cid}),
                    content_type="application/json"
                        )
    # El post queda guardado en la db.

def delete_post(request):
    # El usuario candidato ejecuta esta función cuando elimina un post
    # en su perfil. El usuario que hace el request debe ser el dueño del post.
    # Los datos son pasados mediante POST HTTP.
    return generic_delete(request, Post, 'post_id')
    # El post queda eliminado de la db.

def give_stars_comment(request):
    # Un usuario ejecuta esta función para calificar
    # un comentario con estrellas del uno al cinco. Se pasa por POST.
    pass
    # Las estrellas son guardadas en la DB.

def give_stars_post(request):
    # Un usuario ejecuta esta función para calificar
    # un post con estrellas del uno al cinco. Se pasa por POST.
    pass
    # Las estrellas son guardadas en la DB.

def show_candidate(request, candidate_id):
    # Se ejecuta para llevar a la página en que se muestra el dashboard
    # del candidato, donde se muestra el contenido asociado a él.
    pass
    # Luego de ejecutarse se muestra la página.

def config_page(request, user_id):
    # Se ejecuta para ingresar a la página de configuraciones.
    pass
    # Es posible ingresar a la página de configuraciones si se está logeado.

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                uid = user.id
                if user.userprofile.role == 'candidate':
                    return  HttpResponse(
                            json.dumps({'redirect': "/candidate/user/" +
                            str(uid)}), content_type="application/json")
                else:
                    return  HttpResponse(
                            json.dumps({'redirect': "/profile/user/" +
                            str(uid)}), content_type="application/json")
                return  HttpResponse(
                        json.dumps({'redirect': "/profile/user/" + str(uid)}),
                        content_type="application/json"
                                    )
            else:
                return HttpResponse("Your const account is disabled.")
        else:
            return HttpResponse(
                    json.dumps({}),
                    content_type="application/json"
                                )

    else:
        return render(request, 'const/login.html', {})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

def register(request):
    # Se ejecuta cuando se registra un nuevo usuario en el sistema.
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            cpassword = request.POST.get('cpassword')
            about = request.POST.get('about')
            picture = request.FILES.get('picture')
            if password == cpassword:
                user = User(username = username)
                user.set_password(password)
                user.save()
                up = UserProfile(user = user, picture = picture, role="common",
                                about = about)
                up.save()
                return HttpResponse(
                            json.dumps({'redirect': "/login/"}),
                            content_type="application/json"
                                        )
            else:
                return HttpResponse(
                            json.dumps({}),
                            content_type="application/json"
                                        )
        except:
            return HttpResponse(
                        json.dumps({'redirect': "/login/"}),
                        content_type="application/json"
                                    )

    else:
        return render(request, 'const/register.html', {})
    # El usuario se guarda en la db

def graph(username):
    pos_host = 'localhost'
    pos_port = 5432
    pos_db = 'scrapper'
    pos_user = 'scrapper'
    pos_pass = 'scrapper'

    #conn = psycopg2.connect(database=pos_db, user=pos_user, password=pos_pass, host=pos_host, port=pos_port)
    #cur = conn.cursor()

    try:
        #cur.execute("SELECT * FROM proms WHERE idcandidato = '" + str(username).lower() + "';")
        #rows = cur.fetchall()

        labels = ["a", "b", "c"]
        values = [1, 2, 3]

        #for row in rows:
            #labels.append(row[1])
            #values.append(row[2])
    except:
        print("Error")

    s = Style(colors=('#5DA5DA', '#000000'))
    radar_chart = pygal.Radar(style = s)
    radar_chart.title = 'Emociones'
    radar_chart.x_labels = labels
    radar_chart.add('Candidato', values)
    g = radar_chart.render(fill = True)
    return g


# API Section

def JsonResponseNotFound(data):
    return HttpResponseNotFound(
        json.dumps(data),
        content_type="application/json"
        )

def user_to_json(user):
    return dict(
        id=user.id,
        username=user.username
        )

def api_post_get(request, post_id):
    # Se obtiene el post y todos los comentarios de este.
    try:
        post = Post.objects.get(id = post_id)

        if request.method == 'GET':
            username = post.post_author.username
            comments = post.comment_set.all()
            has_comments = len(comments) > 0

            data = {
                'post': post.as_json(),
                'comments': [c.as_json() for c in comments]
                }

            return JsonResponse(data)

    except:
        pass

    return JsonResponseNotFound({ 'error': True })

@csrf_exempt
def api_post_delete(request, post_id):
    # TODO authentication
    # El usuario candidato ejecuta esta función cuando elimina un post
    # en su perfil. El usuario que hace el request debe ser el dueño del post.
    # Los datos son pasados mediante DELETE HTTP.
    try:
        post = Post.objects.get(id = post_id)

        if request.method == 'DELETE':
            if request.user == post.post_author:
                post.delete()
                return JsonResponse({ 'ok': True })

    except:
        pass

    return JsonResponse({ 'error': True })


def api_candidate_show(request, user_id):
    # Este método se llama cuando se quiere ir a la página de un candidato
    # usando una cuenta de candidato. Se debe estar logeado con el usuario
    # respectivo.
    try:
        required_user = User.objects.get(id = user_id)

        if required_user.userprofile.role != 'candidate':
            return JsonResponse({ 'error': True })
        
        posts = required_user.post_set.all()
        g = graph(required_user.username)

        data = {
            'required_user': user_to_json(required_user),
            'posts': [p.as_json() for p in posts],
            'graph': str(g)}
        return JsonResponse(data)

    except:
        pass

    return JsonResponse({ 'error': True })
