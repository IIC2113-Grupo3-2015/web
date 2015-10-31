from django.test import TestCase
from .models import Post, PairData, Like, UserProfile, Comment
from django.contrib.auth.models import User

from django.utils import timezone

# Create your tests here.

class PostTest(TestCase):
    #Este test prueba la creación de un Post y que se guarde bien en su usuario.

    def setUp(self):
        pass

    def test_are_created(self):
        u1 = User.objects.create(username='user1')
        u1.save()
        post = Post(
                post_title = "title",
                post_text = "text",
                post_author = u1,
                pub_date = timezone.now()
        )
        post.save()
        self.assertEqual((len(Post.objects.all()) >= 0), True)
        self.assertEqual((len(u1.post_set.all()) >= 0), True)

    def tearDown(self):
        pass

class PairDataTest(TestCase):

    def setUp(self):
        pass

    def test_are_created(self):
        u1 = User.objects.create(username='user1')
        u2 = User.objects.create(username='user2')
        u1.save()
        u2.save()
        up1 = UserProfile(role = 'common', user = u1)
        up2 = UserProfile(role = 'candidate', user = u2)
        up1.save()
        up2.save()

        pd = PairData(common_user = up1, candidate_user = up2)
        pd.save()


        self.assertEqual((len(u1.userprofile.common_user.all()) == 1), True)
        # El usuario común tiene acceso a un pair data como "usuario común".
        self.assertEqual((len(u2.userprofile.common_user.all()) == 0), True)
        # El usuario candidato no accede a pair data como "común".

        self.assertEqual((len(u1.userprofile.candidate_user.all()) == 0), True)
        # El usuario común no tiene acceso a un pair data como "candidato".
        self.assertEqual((len(u2.userprofile.candidate_user.all()) == 1), True)
        # El usuario candidato accede a pair data como "candidato".


    def tearDown(self):
        pass

class CommentTest(TestCase):

    def setUp(self):
        pass

    def test_are_created(self):
        u1 = User.objects.create(username='user1')
        u1.save()
        post = Post(
                post_title = "title",
                post_text = "text",
                post_author = u1,
                pub_date = timezone.now()
        )

        post.save()
        comment = Comment(
                post = post,
                user = u1,
                content = "asd"
        )
        comment.save()
        self.assertEqual((len(Comment.objects.all()) > 0), True)
        self.assertEqual((len(post.comment_set.all()) > 0), True)



    def tearDown(self):
        pass
