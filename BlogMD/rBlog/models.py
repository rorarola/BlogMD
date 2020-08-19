from django.db import models
from django.utils import timezone 
from django.urls import reverse

class Category(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")
    title = models.CharField(max_length=255, verbose_name="Title")

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['title']

    def __str__(self):
        return self.title

class Post(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")
    is_published = models.BooleanField(default=False, verbose_name="Is published?")
    published_at = models.DateTimeField(null=True, blank=True, editable=False, verbose_name="Published at")
    # Foreign Key used because post can only have one category, but category can have multiple posts
    category = models.ForeignKey(Category, related_name='post', on_delete=models.SET_NULL, null=True)
    '''
    on_delete引數的說明
    CASCADE：此值設定，是級聯刪除
    PROTECT：此值設定，是會報完整性錯誤
    SET_NULL：此值設定，會把外來鍵設定為null，前提是允許為null
    SET_DEFAULT：此值設定，會把設定為外來鍵的預設值
    SET()：此值設定，會呼叫外面的值，可以是一個函式。 一般情況下使用CASCADE就可以了。
    '''
    author = models.CharField(max_length=200, verbose_name="Author")
    title = models.CharField(max_length=200, verbose_name="Title")
    text = models.TextField(verbose_name="Text")

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        ordering = ['-created_at']

    def publish(self):
        self.is_published = True
        self.published_at = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        # self.id is being used to store the book uniquely in the database, as defined in the Book Model.
        return reverse('post-detail', kwargs={"id": self.id}) 
