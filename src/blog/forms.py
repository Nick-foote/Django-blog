from django import forms

from .models import BlogPost

class BlogPostForm(forms.Form):
	title = forms.CharField()
	slug = forms.SlugField()
	content = forms.CharField(widget=forms.Textarea)

class BlogPostModelForm(forms.ModelForm):
	class Meta:
		model = BlogPost
		fields = ['title', 'slug', 'image', 'content', 'publish_date']

	def clean_title(self, *args, **kwargs):
		instance = self.instance
		print(instance)
		title = self.cleaned_data.get('title')

		qs = BlogPost.objects.filter(title__iexact=title)
		if instance is not None:
			qs = qs.exclude(pk=instance.pk)
		# id=instance.id. takes qs that matches title and then removes the instance itself
		# 
		if qs.exists():
			raise forms.ValidationError("This title already exists")
		return title

