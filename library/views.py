from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Q
from datetime import timedelta, date
from .models import Book, BookIssue, Subscription, CreativeWork, Comment, Like, Activity, Review,Genre
from .forms import SignUpForm, LoginForm, CreativeWorkForm, CommentForm
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView

def home(request):
    return render(request, 'library/home.html')

@login_required
def available_books(request):
    query = request.GET.get('q', '')
    genre_id = request.GET.get('genre', '')
    year = request.GET.get('year', '')
    
    books = Book.objects.all()
    
    if query:
        books = books.filter(Q(title__icontains=query) | Q(author__icontains=query))
    
    if genre_id:
        books = books.filter(genre__id=genre_id)
    
    if year:
        books = books.filter(published_date__year=year)

    genres = Genre.objects.all()
    
    context = {
        'books': books,
        'genres': genres,
    }
    
    return render(request, 'library/available_books.html', context)

@login_required
def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'library/book_detail.html', {'book': book})

@login_required
def add_review(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == "POST":
        review_text = request.POST.get('review_text')
        rating = request.POST.get('rating')
        Review.objects.create(
            book=book,
            user=request.user,
            review_text=review_text,
            rating=rating
        )
    return redirect('book_detail', book_id=book_id)

@login_required
def borrow_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == "POST" and book.available:
        # Update book status
        book.available = False
        book.save()

        # Create a borrowing record with the correct field names
        issued_on = timezone.now()
        due_date = issued_on + timedelta(days=14)  # +14 days from issue date
        BookIssue.objects.create(
            book=book,
            user=request.user,
            issued_on=issued_on,
            due_date=due_date
        )

        # Redirect to the success page with relevant data
        return redirect('successful_borrow', book_id=book.id)
    else:
        # Optionally handle the case where the book is not available
        return redirect('book_detail', book_id=book.id)
    
@login_required
def successful_borrow(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    book_issue = get_object_or_404(BookIssue, book=book, user=request.user)
    return render(request, 'library/successful_borrow.html', {
        'book': book,
        'borrow_date': book_issue.borrow_date,
        'due_date': book_issue.due_date
    })

@login_required
def profile(request):
    try:
        subscription = Subscription.objects.get(user=request.user)
    except Subscription.DoesNotExist:
        subscription = None

    last_books_issued = BookIssue.objects.filter(user=request.user).order_by('-issued_on')[:5]

    recent_activity = Activity.objects.filter(user=request.user).order_by('-timestamp')[:10]

    context = {
        'subscription': subscription,
        'last_books_issued': last_books_issued,
        'recent_activity': recent_activity,
    }
    return render(request, 'library/profile.html', context)

@login_required
def subscription_details(request):
    try:
        subscription = Subscription.objects.get(user=request.user)
        days_left = (subscription.end_date - timezone.now()).days
    except Subscription.DoesNotExist:
        subscription = None
        days_left = 0

    context = {
        'subscription': subscription,
        'days_left': days_left
    }
    return render(request, 'library/subscription_details.html', context)

@login_required
def renew_subscription(request):
    try:
        subscription = Subscription.objects.get(user=request.user)
        subscription.end_date += timedelta(days=30)
        subscription.save()
    except Subscription.DoesNotExist:
        Subscription.objects.create(
            user=request.user,
            start_date=date.today(),
            end_date=date.today() + timedelta(days=30)
        )
    return redirect('subscription_details')

@login_required
def new_subscription(request):
    if request.method == 'POST':
        Subscription.objects.create(
            user=request.user,
            start_date=date.today(),
            end_date=date.today() + timedelta(days=30)
        )
        return redirect('subscription_details')
    return render(request, 'library/new_subscription.html')

@login_required
def creative_works(request):
    works = CreativeWork.objects.all()
    return render(request, 'library/creative_works.html', {'works': works})

@login_required
def creative_work_detail(request, pk):
    work = get_object_or_404(CreativeWork, pk=pk)
    comments = work.comments.all()
    user_liked = work.likes.filter(user=request.user).exists()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.work = work
            comment.author = request.user
            comment.save()
            return redirect('creative_work_detail', pk=pk)
    else:
        comment_form = CommentForm()

    return render(request, 'library/creative_work_detail.html', {
        'work': work,
        'comments': comments,
        'comment_form': comment_form,
        'user_liked': user_liked,
    })

@login_required
def add_creative_work(request):
    if request.method == 'POST':
        form = CreativeWorkForm(request.POST, request.FILES)
        if form.is_valid():
            creative_work = form.save(commit=False)
            creative_work.creator = request.user
            creative_work.save()
            return redirect('creative_works')
    else:
        form = CreativeWorkForm()
    return render(request, 'library/add_creative_work.html', {'form': form})

@login_required
def like_creative_work(request, pk):
    work = get_object_or_404(CreativeWork, pk=pk)
    like, created = Like.objects.get_or_create(work=work, user=request.user)
    if not created:
        like.delete()
    return redirect('creative_work_detail', pk=pk)

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'library/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'library/login.html', {'form': form})

def logout(request):
    auth_logout(request)
    return redirect('home')

class CustomPasswordResetView(PasswordResetView):
    template_name = 'library/password_reset.html'
    email_template_name = 'library/password_reset_email.html'
    success_url = '/login/'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'library/password_reset_confirm.html'
    success_url = '/login/'
