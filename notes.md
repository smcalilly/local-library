# part 3: using models
django web apps access and manage data through python objects referred to as models. models define thes tructure of stored data, including the field *types* and possibly alos their maximum size, default values, selection list options, help text for documentation, label text for forms, etc.

The definition of the model is independent of the underlying database -- you can choose one of several as part of your project settings. Once you've chosen what database you want to use, you don't need to talk to it directly at all -- you just write your model structure and other code, and Django handles all the dirty work of communication with the DB.

## designing the LocalLibrary models
[See this section](https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Models#Designing_the_LocalLibrary_models)

## model primer
### model definition
models are defined in an app's models.py file. 

subclass of `django.db.models.Model`

- fields  
a model can have an arbitrary number of fields, of any type -- each one represents column of data that we want to store in one of our db tables. Each DB records (row) will consist of one of each field values.

For example: 
```
my_field_name = models.CharField(max_length=20, help_text='Enter field documentation')
```


#### common field arguments
- `help_text`: provides a text label for HTML forms (like in the admin site)
- `verbose_name`: a human-readable name for the field used in field labels. if not specified, django will infer the default verbose name from the field name
- `default`: the default value for the field. this can be a value or a callable object, in which case the object will be called every time a new record is created
- `null`: if `True`, dj will store blank values as NULL in the DB for fields where this is appropriate. The default is `False`
- `blank`: if `True`, the field is allowed to be blank in your forms.
- `choices`: a group of choices for this field.
- `primary_key`: If `True`, sets the current field as the primary key for the model

#### common field types
- `CharField` is used to define short-to-mid sized fixed-length strings. You must specify the `max_length` of the data to be stored.
- `TextField` is used for large arbitary-length strings. You may specify `max_lengh` for the field, but this is used only when the field is displayed in forms (it's not enforced at the DB level)
- `IntgerField` is a field for storing integer (whole number) values, and for validating entered values as integers in forms.
- `DateField` and `DateTimeField` are used for storing/respresenting dates and date/time information.
- `EmailField` is used to store and validate email addresses.
- `FileField` and `ImageField` are used to upload files and images respectively 
- `AutoField` is a special type of `IntegerField` that automatically increments.
- `ForeignKey` is used to specify a one-to-many relationship to another DB model
- `ManyToManyField` is used to specify a many-to-many relationship'

This only a sample, there are many otheres. You can see a [full list here](https://docs.djangoproject.com/en/2.1/ref/models/fields/#field-types).


### Metadata
You can declare model-level metadata for your model by delcaring `class Meta` as show:
```
class Meta:
	ordering = ['-my_field_name']
```

There are other things you can do with the metadata, like set the default ordering or give the model a new verbose name. See the [full list here](https://docs.djangoproject.com/en/2.1/ref/models/options/)


## working with the models
this is how you work with django's orm!

### creating and modifying records
you can create a record by instantiating a model and then calling `save()`.
```
# create a new record using the model's constructor
record = MyModelName(my_field_name="instance_1")

# save the object into the database
record.save()
```
note: if you haven't declared any field as a `primary_key`, the new record will be given one automatically, with the field name `id`. You could query this field after saving the record, and it would have a value of 1.

You can access the fields in this new record using the dot syntax. You can change the values. You have to call `save()` to store modified values to the database.

```
# access model field values using python attributes
print(record.id) # should return 1 for the first record
print(record.my_field_name) should print 'instance_1'

# change record by modifying the fields, then calling save()
record.my_field_name = 'new_instance_name'
record.save()
```


### searching for records
you can search for records that match certain criteria using the model's `objects` attributes (provided by the base class)

we can get records for a model as a `QuerySet`, using `objects.all()`. The `QuerySet` is an iterable object, meaning that it contains a number of objects that we can iterate/loop through.
```
all_books = Book.objects.all()
```

django's `filter()` method allows us to filter the returned `QuerySet` to match a specified text or numeric field against a particular criteria. for example, to filter for books that contain "wild" in the title and then count them, we could do the following:
```python
wild_books = Books.objects.filter(title__contains='wild')
number_wild_books = wild_books.count()
```
the fields to match and the type of match are defined in the filter paramter name, using the fomrat: `field_name__match_type`.

in some cases, you'll need to filter on a field that defines a one-to-many relationship to another model (i.e. a `ForeignKey`). In this case you can "index" to fields within the related model with additional double underscores. For example, to filter for books with a specific genre pattern, you will have to index to the `name` through the `genre` field as shown:
```
# will match on: fiction, sciene fiction, non-fiction, etc
books_containing_genre = Book.objects.filter(genre__name__icontains='fictions')
```
there is a lot you can do with this. for more info, [go here](https://docs.djangoproject.com/en/2.1/topics/db/queries/).

# mdn django part 4 - admin site
[this is the place to go for a good guide on customizing the admin site](https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Admin_site)
- first you need to register it at `catalog/admin.py`

- then create a superuser
```
python3 manage.py createsuperuser
```

#  django - guide on views
## path in url functions
We also created a placeholder file for the URLConf module, named /catalog/urls.py. Add the following lines to that file: 

urlpatterns = [
    path('', views.index, name='index'),
]

The path() function defines the following:

    A URL pattern, which is an empty string: ''. We'll discuss URL patterns in detail when working on the other views.
    A view function that will be called if the URL pattern is detected: views.index,  which is the function named index() in the views.py file. 

The path() function also specifies a name parameter, which is a unique identifier for this particular URL mapping. You can use the name to "reverse" the mapper, i.e.  to dynamically create a URL that  points to the resource that the mapper is designed to handle. For example, we can use the name parameter to link to our home page from any other page by adding the following link in a template:

<a href="{% url 'index' %}">Home</a>.

## function based view
a view is a function that 
- processes an http request
- fetches the required data from a database
- renders an html page using an html template
- returns the generated html in an http response 

pass the context

into the handle bars
{{ variable_name }}

you can extend/override the base views

great!


## generic views
generic class-based list and detail views.

create a new view by inheriting from a generic class view, like:
```
class BookListView(generic.ListView):
	model = Book
```
You assign the`model` variable to whatever model you're trying to interact with. 

then you reference an instance of that view in the urls.py `urlpaths` list. 

then you create a template that corresponds to the view's name. the generic view takes care of all the variables that are within the view, but you can override the generic view's `context` and do other OOP sort of things with it

# sessions
super useful built in session management -- easy to use in a django view. can modify and delete stuff in the session, within the view. it's a python dictionary. need to specifically update the item in session db if you want to persist a change to the session object.

## user authentication and permissions
https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Authentication
django has a built in authentication and authorization system, built on top of the session framework.

it includes
1. models for Users and Groups (simply a generic way of applying specific permissions to more than one user)
2. permissions/flags that designate whether a user/group may perform a task
3. forms/views for logging in users
4. view tools for restricting content (authorization)

- authenticate with the `LoginRequiredMixin`
- authorize with the `PermissionRequiredMixin`
	[working with user permissions](https://medium.com/djangotube/django-roles-groups-and-permissions-introduction-a54d1070544)

# django forms
https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Forms

### form class
"The `Form` class is the heart of Django's form handling system. It specifies the fields in their form, fields' layout, display widgets, labels, initial values, valid values, and possibly error messages."

"The class also provides methods for rendering itself in templates using predefined formats (tables, lists, etc) or for getting the value of any element (enabling fine-grained manual rendering)"

declaration syntax for a `Form` is very simliar to declaring a `Model`.

arguments common to a form:
- required
- label
- label_suffix
- initial
- widget
- help_text
- error_messages
- validators
- localize
- disabled

### validation
https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Forms#Validation
"the easiest way to validate a single field is to override the method `clean_<fieldname>()` for the field you want to check.""


### views
then you gotta tie it up with the view

functional view can use the `@login_required` and `@permission_required` decorators

bound and unbound form
bind the POST request to the form and validate it. if it validates, save the data
if there is an error then return a form instance with the error:

```
@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_by_librarian(request, pk):
	"""View function for renewing a specific BookInstance by librarian."""
	book_instance = get_object_or_404(BookInstance, pk=pk)
	if request.method == 'POST':
	    form = RenewBookForm(request.POST)

	    if form.is_valid():
	        book_instance.due_back = form.cleaned_data['renewal_date']
	        book_instance.save()

	        # redirect
	        return HttpResponseRedirect(reverse('all-borrowed') )

	context = {
	    'form': form,
	    'book_instance': book_instance,
	}

	return render(request, 'catalog/book_renew_librarian.html', context)
```

## ModelForm class
```
from django.forms import ModelForm

from catalog.models import BookInstance

class RenewBookModelForm(ModelForm):
    def clean_due_back(self):
       data = self.cleaned_data['due_back']
       
       # Check if a date is not in the past.
       if data < datetime.date.today():
           raise ValidationError(_('Invalid date - renewal in past'))

       # Check if a date is in the allowed range (+4 weeks from today).
       if data > datetime.date.today() + datetime.timedelta(weeks=4):
           raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

       # Remember to always return the cleaned data.
       return data

    class Meta:
        model = BookInstance
        fields = ['due_back']
        labels = {'due_back': _('Renewal date')}
        help_texts = {'due_back': _('Enter a date between now and 4 weeks (default 3).')} 
```

