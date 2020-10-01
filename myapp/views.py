from django.shortcuts import render, redirect, reverse
from .models import Post, Comment
from django.views.generic.edit import CreateView
from .forms import CommentForm
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

def index(request):
    posts = Post.objects.all()
    context ={'posts':posts}
    return render(request, 'index.html', context)

class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'description', 'image']
    #created_at, updated_at, user(who is logged in), likes are updated automatically
    template_name = 'create.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

@login_required
def detail(request, pk):
    p = Post.objects.get(pk=pk)
    comments = Comment.objects.filter(post_id = pk) #to get all the posts related to the particular post
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.cleaned_data['comment']
            c = Comment(post_id = pk, comment = comment, user = request.user)
            c.save()
            return HttpResponseRedirect(reverse('detail', kwargs = {'pk':pk}))#after commenting the post it should redirect to the same page
    else:
        form = CommentForm()
    return render(request, 'detail.html', {'form':form,'p':p, 'comments':comments})


def like(request):
    if request.is_ajax():
        post_id = request.GET.get('post')#data from frontend
        post = Post.objects.get(id = post_id)
        post.likes += 1
        post.save()
        data = {'likes':post.likes}
    return JsonResponse(data)