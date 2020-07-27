from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect


from .forms import BlogPostModelForm
from .models import BlogPost


# def blog_post_detail_page(request, slug):
# 	obj = get_object_or_404(BlogPost, slug=slug)
# 	template_name = 'blog_post_detail.html'
# 	context = {"object": obj}
# 	return render(request, template_name, context)


def blog_post_list_view(request):
	# list out objects
	# could be search
	qs = BlogPost.objects.published()
	if request.user.is_authenticated:
		my_qs = BlogPost.objects.filter(user=request.user)
		qs = (qs | my_qs).distinct()
	template_name = 'blog/list.html'
	context = {'object_list': qs}
	return render(request, template_name, context)




# @login_required
@staff_member_required
def blog_post_create_view(request):
	# create objects
	#  use a form
	# request.user -> returns somthing
	form = BlogPostModelForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		obj = form.save(commit=False)
		# obj.title = form.cleaned_data.get("title") +"123"
		obj.user = request.user
		obj.save()
		form = BlogPostModelForm()
	template_name = 'form.html'
	context = {"form": form}
	return render(request, template_name, context)


@staff_member_required
def blog_post_detail_view(request, slug):
	# 1 object or detail view
	obj = get_object_or_404(BlogPost, slug=slug)
	template_name = 'blog/detail.html'
	context = {'object': obj}
	return render(request, template_name, context)


@staff_member_required
def blog_post_update_view(request, slug):
	obj = get_object_or_404(BlogPost, slug=slug)
	form = BlogPostModelForm(request.POST or None, instance=obj)
	if form.is_valid():
		form.save()
	template_name = 'form.html'
	context = {'form': form, "title": f"Update: {obj.title}"}
	return render(request, template_name, context)
# f"string {substitution}"

@staff_member_required
def blog_post_delete_view(request, slug):
	obj = get_object_or_404(BlogPost, slug=slug)
	template_name = 'blog/delete.html'
	if request.method == "POST":
		obj.delete()
		return redirect("/blog")
	context = {'object_list': obj}
	return render(request, template_name, context)
























