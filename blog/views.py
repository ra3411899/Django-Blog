from django.shortcuts import render, get_object_or_404
from .models import Post
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# The code imports necessary modules for the Django MVC framework and defines a PostListView class, 
# using the ListView generic view from Django to view a list of posts. 
# It sets the model to be used as the Post model and the template name to 'blog/home.html'. 
# The context object name is set to 'posts' and ordering is set by the date_posted in descending.
# The number of entries displayed per page is 5.


class PostListView(ListView):
    model = Post
    template_name = "blog/home.html" # <app>/<model>_<viewtype>.html
    context_object_name = 'posts' # Access Variable Name - Defined
    ordering = ['-date_posted']
    paginate_by = 5


class UserPostListView(ListView):
    model = Post
    template_name = "blog/user_posts.html" # <app>/<model>_<viewtype>.html
    context_object_name = 'posts' # Access Variable Name - Defined
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')
    


class PostDetailView(DetailView):
    model = Post

# LoginRequiredMixin - Is Used when we try to create any blog - then we need to login first
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    # template_name = ""
    fields = ['title', 'content']

    # Need To define the form_valid() cause when we submit it will show a not intigrity error - does not knwo about the logged in user
    def form_valid(self, form):
        form.instance.author = self.request.user # It gets Created but not redirect was define - 
        return super().form_valid(form)

        # Need to Configured - No URL to redirect to.  Either provide a url or define a get_absolute_url method on the Model.
    # def get_absolute_url(self):
    #     return reverse('post-detail', kwargs={'pk': self.pk})


# UserPassesTestMixin - before this any user can update any post, So, now with UserPassesTestMixin, it will if the same user is trying to do that or not
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

# test_func, which checks if the current user is the author of the post.
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    # self.request.user - this will check for the current logged In User with Post Author


class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin ,DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    


def home(request):
    context = {
        'posts' : Post.objects.all()
    }
    return render(request, 'blog/home.html', context)

def about(request):
    return render(request, 'blog/about.html', {})
