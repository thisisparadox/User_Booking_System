from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import BlogComment, BlogReview

@receiver(post_save, sender=BlogComment)
def notify_admin_on_new_comment(sender, instance, created, **kwargs):
    if created and not instance.approved:
        subject = f'New Comment Awaiting Approval: {instance.post.title}'
        message = render_to_string('blog/emails/new_comment_notification.txt', {
            'comment': instance,
            'admin_url': f'{settings.SITE_URL}/admin/blog/blogcomment/{instance.id}/change/',
        })
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [settings.ADMIN_EMAIL],
            fail_silently=True,
        )

@receiver(post_save, sender=BlogReview)
def notify_admin_on_new_review(sender, instance, created, **kwargs):
    if created and not instance.approved:
        subject = f'New Review Awaiting Approval: {instance.post.title}'
        message = render_to_string('blog/emails/new_review_notification.txt', {
            'review': instance,
            'admin_url': f'{settings.SITE_URL}/admin/blog/blogreview/{instance.id}/change/',
        })
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [settings.ADMIN_EMAIL],
            fail_silently=True,
        )

@receiver(post_save, sender=BlogComment)
def notify_user_on_comment_approval(sender, instance, **kwargs):
    if instance.approved and not instance.user_notified:
        subject = f'Your comment has been approved'
        message = render_to_string('blog/emails/comment_approved_notification.txt', {
            'comment': instance,
            'post_url': f'{settings.SITE_URL}{instance.post.get_absolute_url()}',
        })
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [instance.user.email],
            fail_silently=True,
        )
        instance.user_notified = True
        instance.save(update_fields=['user_notified'])

@receiver(post_save, sender=BlogReview)
def notify_user_on_review_approval(sender, instance, **kwargs):
    if instance.approved and not instance.user_notified:
        subject = f'Your review has been approved'
        message = render_to_string('blog/emails/review_approved_notification.txt', {
            'review': instance,
            'post_url': f'{settings.SITE_URL}{instance.post.get_absolute_url()}',
        })
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [instance.user.email],
            fail_silently=True,
        )
        instance.user_notified = True
        instance.save(update_fields=['user_notified'])