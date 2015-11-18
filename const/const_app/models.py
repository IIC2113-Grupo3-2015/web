from django.db import models
from django.contrib.auth.models import User


# Entidades de la aplicación. Recordemos que las relaciones
# se realizan mediante funciones en Django.

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    follows = models.ManyToManyField('self', through='PairData', symmetrical=False)
    picture = models.ImageField(upload_to='profile_images', blank = True)
    role = models.CharField(max_length = 50)
    about = models.TextField()

    def __str__(self):
        return self.user.username

class PairData(models.Model):
    common_user = models.ForeignKey(UserProfile,
            related_name='common_user')
    candidate_user = models.ForeignKey(UserProfile,
            related_name='candidate_user')

class Like(models.Model):
    pass

class Post(models.Model):
    post_title = models.TextField()
    post_text = models.TextField()
    post_author = models.ForeignKey(User)
    pub_date = models.DateTimeField('date published')
    def as_json(self):
        return dict(
            id=self.id,
            post_title=self.post_title,
            post_text=self.post_text,
            post_author_id=self.post_author.id,
            post_author_username=self.post_author.username,
            pub_date=self.pub_date.isoformat()
            )

class Comment(models.Model):
    post = models.ForeignKey(Post)
    user = models.ForeignKey(User)
    content = models.TextField()
    def as_json(self):
        return dict(
            id=self.id,
            post_id=self.post.id,
            user_id=self.user.id,
            content=self.content
            )
