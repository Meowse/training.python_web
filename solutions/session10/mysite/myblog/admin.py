from django.contrib import admin
from myblog.models import Post
from myblog.models import Category

admin.site.register(Post)
admin.site.register(Category)

class CategoryInline(admin.TabularInline):
    model = Category.posts.through

class CategoryAdmin(admin.ModelAdmin):
    inlines = [
        CategoryInline,
    ]
    exclude = ('posts',)

class PostAdmin(admin.ModelAdmin):
    inlines = [
        CategoryInline,
    ]
