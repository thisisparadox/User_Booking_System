from django import forms
from .models import BlogReview, BlogComment, ReviewImage
from django.core.files.images import get_image_dimensions


class BlogReviewForm(forms.ModelForm):
    class Meta:
        model = BlogReview
        fields = ['title', 'content', 'rating', 'stay_date', 'booking_id']
        widgets = {
            'stay_date': forms.DateInput(attrs={'type': 'date'}),
            'content': forms.Textarea(attrs={'rows': 5}),
        }


class BlogCommentForm(forms.ModelForm):
    class Meta:
        model = BlogComment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your comment here...'}),
        }


class ReviewImageForm(forms.ModelForm):
    class Meta:
        model = ReviewImage
        fields = ['image']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'accept': 'image/*'})
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if not image.content_type.startswith('image/'):
                raise forms.ValidationError("The uploaded file must be an image.")
            
            # Check image dimensions
            width, height = get_image_dimensions(image)
            if width > 4096 or height > 4096:
                raise forms.ValidationError("Image dimensions should not exceed 4096x4096 pixels.")
            
            # Check file size (max 5MB)
            if image.size > 5 * 1024 * 1024:
                raise forms.ValidationError("Image file size should not exceed 5MB.")
            
        return image