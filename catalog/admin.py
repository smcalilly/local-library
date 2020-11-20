from django.contrib import admin
from .models import Author, Genre, Book, BookInstance, Language

# Register your models here.
# admin.site.register(Book)
# admin.site.register(BookInstance)
# admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Language)

class BookInline(admin.TabularInline):
	model = Book
	extra = 0


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
	list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
	fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
	inlines = [BookInline]


# make it so an admin can create a book instance while creating a book
class BookInstanceInline(admin.TabularInline):
	model = BookInstance
	extra = 0


# register the admin classes for book
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
	list_display =('title', 'author', 'display_genre')
	inlines = [BookInstanceInline]


# register the admin classes for BookInstance
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
	list_display = ('book', 'status', 'borrower', 'due_back', 'id')
	list_filter = ('status', 'due_back')

	fieldsets = (
		(None, {
			'fields': ('book', 'imprint', 'id')
		}), 
		('Availability', {
			'fields': ('status', 'due_back', 'borrower')
		}),
	)