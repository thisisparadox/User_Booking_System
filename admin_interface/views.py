from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Service, ReviewImage
from django.views.generic import ListView, DetailView
from .models import BlogPost, BlogCategory, BlogReview, BlogComment
from .forms import BlogReviewForm, BlogCommentForm, ReviewImageForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db import models
from django.core.cache import cache
from django.http import HttpResponseForbidden
from django.views.decorators.http import require_POST
import json

def index(request):
    return render(request, 'index.html')


def services(request):
    services = Service.objects.all().order_by('order')

    # Group services by category for the navigation
    categories = dict(Service.SERVICE_CATEGORIES)
    services_by_category = {cat[0]: [] for cat in Service.SERVICE_CATEGORIES}

    for service in services:
        services_by_category[service.category].append(service)

    context = {
        'services': services,
        'services_by_category': services_by_category,
        'categories': categories,
    }
    return render(request, 'services.html', context)

def blog(request):
    return render(request, 'blog.html')


def contact(request):
    if request.method == 'POST':
        # Process contact form
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Here you would typically save to database or send email
        messages.success(request, 'Your message has been sent successfully!')
        return redirect('contact')

    return render(request, 'contact.html')


def book(request):
    if request.method == 'POST':

        room_type = request.POST.get('room_type')
        check_in = request.POST.get('check_in')
        check_out = request.POST.get('check_out')
        adults = request.POST.get('adults')
        children = request.POST.get('children')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        special_requests = request.POST.get('special_requests')

        # Here you would typically save booking to database
        messages.success(request, 'Your booking has been confirmed!')
        return redirect('book')

    return render(request, 'book.html')


class BlogListView(ListView):
    model = BlogPost
    template_name = 'blog.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset().filter(status='published')

        # Filter by category if specified
        category_slug = self.request.GET.get('category')
        if category_slug:
            category = get_object_or_404(BlogCategory, slug=category_slug)
            queryset = queryset.filter(category=category)

        # Search functionality
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                models.Q(title__icontains=search_query) |
                models.Q(content__icontains=search_query) |
                models.Q(excerpt__icontains=search_query)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = BlogCategory.objects.all()
        context['featured_post'] = BlogPost.objects.filter(
            is_featured=True,
            status='published'
        ).first()
        return context


class BlogDetailView(DetailView):
    model = BlogPost
    template_name = 'blog_post_detail.html'
    context_object_name = 'post'

    def get_queryset(self):
        return super().get_queryset().filter(status='published')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = BlogCommentForm()
        context['review_form'] = BlogReviewForm()
        context['image_form'] = ReviewImageForm()
        context['approved_comments'] = self.object.comments.filter(approved=True)
        context['approved_reviews'] = self.object.reviews.filter(approved=True)
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)

        # Handle partial requests for AJAX
        if request.GET.get('partial') == 'comments':
            return render(request, 'blog/_comments_partial.html', {
                'approved_comments': self.object.comments.filter(approved=True)
            })

        return self.render_to_response(context)


# @login_required
def add_comment(request, post_id):
    # Rate limiting - 5 comments per hour
    cache_key = f'comment_rate_limit_{request.user.id}'
    comment_count = cache.get(cache_key, 0)

    if comment_count >= 5:
        return HttpResponseForbidden("You've exceeded the maximum number of comments allowed per hour.")

    post = get_object_or_404(BlogPost, id=post_id)

    if request.method == 'POST':
        form = BlogCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user

            # Auto-approve if user is in Trusted Commenters group
            if request.user.groups.filter(name='Trusted Commenters').exists() or \
                    request.user.has_perm('blog.can_post_comment_without_approval'):
                comment.approved = True
                messages.success(request, 'Your comment has been posted.')
            else:
                messages.success(request, 'Your comment has been submitted and is awaiting approval.')

            comment.save()

            # Update rate limit counter only after successful submission
            cache.set(cache_key, comment_count + 1, timeout=3600)  # 1 hour

            return redirect('blog:post_detail',
                            year=post.publish_date.year,
                            month=post.publish_date.month,
                            day=post.publish_date.day,
                            slug=post.slug)

    # If not POST or form invalid, redirect back to post
    return redirect('blog:post_detail',
                    year=post.publish_date.year,
                    month=post.publish_date.month,
                    day=post.publish_date.day,
                    slug=post.slug)


# @login_required
def add_review(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    if request.method == 'POST':
        review_form = BlogReviewForm(request.POST)
        image_form = ReviewImageForm(request.POST, request.FILES)

        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.post = post
            review.user = request.user
            review.save()

            # Handle multiple image uploads
            images = request.FILES.getlist('images')
            for i, image in enumerate(images[:5]):  # Limit to 5 images
                ReviewImage.objects.create(review=review, image=image)

            messages.success(request, 'Your review has been submitted and is awaiting approval.')
            return redirect('blog:post_detail', year=post.publish_date.year,
                            month=post.publish_date.month,
                            day=post.publish_date.day,
                            slug=post.slug)

    return redirect('blog:post_detail', year=post.publish_date.year,
                    month=post.publish_date.month,
                    day=post.publish_date.day,
                    slug=post.slug)


@require_POST
# @login_required
def like_post(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    action = request.POST.get('action')

    if action == 'like':
        post.likes.add(request.user)
    else:
        post.likes.remove(request.user)

    return JsonResponse({
        'status': 'ok',
        'total_likes': post.likes.count()
    })