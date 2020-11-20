import datetime

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse

from catalog.models import Book, Author, BookInstance, Genre
from catalog.forms import RenewBookForm

@login_required
def index(request):
	"""View function for home page of site."""

	# generate counts of some of the main objects
	num_books = Book.objects.all().count()
	num_instances = BookInstance.objects.all().count()

	# available books (status = 'a')
	num_instances_available = BookInstance.objects.filter(status__exact='a').count()

	# the `all()` is implied by default
	num_authors = Author.objects.count()

	# number of visits to this view, as counted in the session variable
	num_visits = request.session.get('num_visits', 1)
	request.session['num_visits'] = num_visits + 1

	# get a count of genres
	num_genres = Genre.objects.count()

	# get a count of book titles that contain the word "the"
	num_books_with_the_in_the_title = Book.objects.filter(title__icontains="the").count()

	context = {
		'num_books': num_books,
		'num_instances': num_instances,
		'num_instances_available': num_instances_available,
		'num_authors': num_authors,
		'num_genres': num_genres,
		'num_books_with_the_in_the_title': num_books_with_the_in_the_title,
		'num_visits': num_visits
	}

	# render the HTML template index.html with the data in the context variable
	return render(request, 'index.html', context=context)


class BookListView(LoginRequiredMixin, generic.ListView):
	model = Book
	paginate_by = 10


class BookDetailView(LoginRequiredMixin, generic.DetailView):
	model = Book


class AuthorListView(LoginRequiredMixin, generic.ListView):
	model = Author


class AuthorDetailView(LoginRequiredMixin, generic.DetailView):
	model = Author


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
	"""Generic class-based view listing books on loan to current user."""
	model = BookInstance
	template_name = 'catalog/bookinstance_list_borrowed_user.html'
	paginate_by = 10

	def get_queryset(self):
		return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


class AllBorrowedBooksListView(PermissionRequiredMixin, generic.ListView):
	model = BookInstance
	template_name = 'catalog/bookinstance_list_all_borrowed.html'
	paginate_by = 10
	permission_required = 'catalog.can_mark_returned'


@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
	"""View function for renewing a specific BookInstance by librarian."""
	book_instance = get_object_or_404(BookInstance, pk=pk)

	# if this is a POST request, then process the form data
	if request.method == 'POST':
		# create a form instance and populate it with data from the request (binding)
		form = RenewBookForm(request.POST)

		# check if form is valid
		if form.is_valid():
			# get it from the form and save it
			book_instance.due_back = form.cleaned_data['renewal_date']
			book_instance.save()

            # upon success, redirect
			return HttpResponseRedirect(reverse('borrowed'))
	else:
    	# send a blank form because it should be the intial GET request(unbound form)
		proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
		form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    # a form will be returned with the initial GET request or returned as a form with an error
	context = {
		'form': form,
		'book_instance': book_instance
	}

	return render(request, 'catalog/book_renew_librarian.html', context)

	