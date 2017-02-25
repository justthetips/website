from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    @staticmethod
    def get_list_of_tags():
        return Tag.objects.all()

class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    @staticmethod
    def get_list_of_categories():
        return Category.objects.all()

class Post(models.Model):
    author = models.ForeignKey(User)
    title = models.CharField(max_length=100)
    content = models.TextField()
    category = models.ForeignKey(Category)
    pub_date = models.DateField()
    draft = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    @staticmethod
    def get_latest_posts(number = None):
        posts = Post.objects.order_by('-pub_date')
        return posts if number is None else posts[:number]

    @staticmethod
    def get_latest_posts_with_category(category_name, number = None):
        try:
            category = Category.objects.get(name=category_name)
        except Category.DoesNotExist:
            return None
        posts = Post.get_latest_posts().filter(category=category)
        return posts if number is None else posts[:number]

    @staticmethod
    def get_latest_posts_with_tag(tag_name, number = None):
        try:
            tag = Tag.objects.get(name=tag_name)
        except Tag.DoesNotExist:
            return None
        post_tag = PostTag.objects.filter(tag=tag)
        return [elem.post for elem in post_tag]
        
class PostTag(models.Model):
    class Meta:
        unique_together = ('post', 'tag')
    post = models.ForeignKey(Post)
    tag = models.ForeignKey(Tag)

    def __str__(self):
        return "%d (Post: %s; Tag: %s)" % (self.id, self.post, self.tag)
