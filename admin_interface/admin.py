from django.contrib import admin
from .models import Service, ServiceImage
from .models import (BlogCategory, BlogPost, BlogImage,
                    BlogReview, BlogComment, ReviewImage)

class ServiceImageInline(admin.TabularInline):
    model = ServiceImage
    extra = 1

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'adult_price', 'is_featured', 'order')
    list_filter = ('category', 'is_featured')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ServiceImageInline]
    ordering = ('order',)


class BlogImageInline(admin.TabularInline):
    model = BlogImage
    extra = 1


class BlogReviewInline(admin.TabularInline):
    model = BlogReview
    readonly_fields = ('post', 'user', 'title', 'content', 'rating', 'stay_date', 'booking_id', 'created_date')
    extra = 0

    def has_add_permission(self, request, obj=None):
        return False


class BlogCommentInline(admin.TabularInline):
    model = BlogComment
    readonly_fields = ('post', 'user', 'content', 'created_date')
    extra = 0

    def has_add_permission(self, request, obj=None):
        return False


class ReviewImageInline(admin.TabularInline):
    model = ReviewImage
    extra = 1


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publish_date', 'status', 'is_featured')
    list_filter = ('status', 'created_date', 'publish_date', 'author', 'is_featured')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish_date'
    ordering = ('status', '-publish_date')
    inlines = [BlogImageInline, BlogReviewInline, BlogCommentInline]


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(BlogReview)
class BlogReviewAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'rating', 'created_date', 'approved')
    list_filter = ('approved', 'created_date', 'rating')
    search_fields = ('content', 'title')
    actions = ['approve_reviews']
    inlines = [ReviewImageInline]

    def approve_reviews(self, request, queryset):
        queryset.update(approved=True)

    approve_reviews.short_description = "Approve selected reviews"
    actions = ['approve_reviews', 'send_approval_notification']

    def send_approval_notification(self, request, queryset):
        for review in queryset.filter(approved=False):
            from blog.signals import notify_admin_on_new_review
            notify_admin_on_new_review(sender=BlogReview, instance=review, created=True)
        self.message_user(request, f"Approval notifications sent for {queryset.count()} reviews.")

    send_approval_notification.short_description = "Send approval notification for selected reviews"


@admin.register(BlogComment)
class BlogCommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'created_date', 'approved')
    list_filter = ('approved', 'created_date')
    search_fields = ('content',)
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(approved=True)

    approve_comments.short_description = "Approve selected comments"
    actions = ['approve_comments', 'send_approval_notification']

    def send_approval_notification(self, request, queryset):
        for comment in queryset.filter(approved=False):
            # Reuse our signal logic
            from blog.signals import notify_admin_on_new_review
            notify_admin_on_new_comment(sender=BlogComment, instance=comment, created=True)
        self.message_user(request, f"Approval notifications sent for {queryset.count()} comments.")

    send_approval_notification.short_description = "Send approval notification for selected comments"