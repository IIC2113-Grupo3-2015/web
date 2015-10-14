from django.shortcuts import render

def index(request):
    # Este método es llamado cada vez que se necesita ir a la página de
    # bienvenida. No necesita login.
    context = {}
    return render(request, 'const/index.html', context)
    # Después de la llamada, la página es cambiada por la de bienvenida.

def main_page(request):
    # Este método envía a la página principal de todo usuario, donde se muestran
    # las últimas novedades. Necesita login.
    pass
    # El método renderea la página junto a un diccionario, en el que
    # se envían los valores requeridos por la página desde la base de datos.

def profile_page(request, user_id):
    # Este método es llamado cuando se quiere acceder al perfil de un usuario.
    # Necesita de un usuario con login que coincida con la url.
    # Además el id del usuario debe estar explícito en la url
    pass
    # El método te lleva al perfil del usuario

def candidate_profile_page(request, user_id):
    # Este método se llama cuando se quiere ir a la página de un candidato
    # usando una cuenta de candidato. Se debe estar logeado con el usuario
    # respectivo.
    pass
    # # El método te lleva al perfil del usuario candidato

def create_post_entry(request):
    # El usuario candidato ejecuta esta función cuando añade un nuevo post
    # en su entrada. El usuario que realiza el request queda registrado
    # como autor del post. Los datos son pasados mediante POST HTTP.
    pass
    # El post es guardado en la base de datos

def delete_post_entry(request):
    # El usuario candidato ejecuta esta función cuando elimina un post
    # en su perfil. El usuario que hace el request debe ser el dueño del post.
    # Los datos son pasados mediante POST HTTP.
    pass
    # Se elimina el post de la DB.

def comment_post(request):
    # El usuario ejecuta esta función al comentar en un post de un candidato.
    # Se genera un comentario asociado al post visible para todos los usuarios.
    # Se requiere login. Los valores se pasan mediante POST HTTP.
    pass
    # El post queda guardado en la db.

def delete_post(request):
    # El usuario ejecuta esta función al eliminar un comentario de un post.
    # Se requiere login. Los valores se pasan mediante POST HTTP.
    pass
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

def login(request):
    # Se ejecuta cuando un usuario quiere logearse
    pass
    # El usuario queda logeado.

def logout(request):
    # Se ejecuta cuando el usuario quiere cerrar sesión.
    # El usuario debe estar logeado.
    pass
    # El usuario cierra su sesión.

def register(request):
    # Se ejecuta cuando se registra un nuevo usuario en el sistema.
    pass
    # El usuario se guarda en la db

def is_candidate(function_from_view):
    # Decorador que permite ver si un usuario está logeado y
    # además es candidato.
    pass
    # Si no es candidato, no retorna nada. Si es candidato se retorna
    # la función entregada como parámetro
