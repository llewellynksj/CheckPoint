from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.text import slugify
from .models import Post
from .forms import CommentForm, PostForm, UpdatePostForm


def index(request):
    """Request the view for blog.html"""
    return render(request, 'blogPoint/blog.html')


class PostList(generic.ListView):
    """Post list on blog.html"""
    model = Post
    queryset = Post.objects.filter(status=1).order_by("-created_on")
    template_name = "blogPoint/blog.html"
    paginate_by = 6


class PostDetail(View):
    """Settings for displaying individual BlogPosts"""
    def get(self, request, slug, *args, **kwargs):
        """Get information on Blogpost from backend"""
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by("-created_on")
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            "blogPoint/post_detail.html",
            {
                "post": post,
                "comments": comments,
                "commented": False,
                "liked": liked,
                "comment_form": CommentForm()
            },
        )

    def post(self, request, slug, *args, **kwargs):
        """Send information back to backend"""
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by("-created_on")
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment_form.instance.user = request.user
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
        else:
            comment_form = CommentForm()

        return render(
            request,
            "blogPoint/post_detail.html",
            {
                "post": post,
                "comments": comments,
                "commented": True,
                "comment_form": comment_form,
                "liked": liked
            },
        )


class PostLike(View):
    """Remove or add like and redirect to post_detail.html"""
    def post(self, request, slug, *args, **kwargs):
        """With this function user can like or remove its like"""
        post = get_object_or_404(Post, slug=slug)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        return HttpResponseRedirect(reverse('post_detail', args=[slug]))


class AddPostView(LoginRequiredMixin, generic.CreateView):
    """Allow users to post"""
    model = Post
    form_class = PostForm
    template_name = 'add_post.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.slug = slugify(form.cleaned_data['title'])
        return super(AddPostView, self).form_valid(form)


class UpdatePostView(UserPassesTestMixin, generic.UpdateView):
    """Allow user to update their posts"""
    model = Post
    template_name = 'update_post.html'
    form_class = UpdatePostForm

    def test_func(self):
        logged_in_user = self.request.user
        current_ticket = self.get_object()

        if current_ticket.author == logged_in_user:
            return True
        else:
            return False


class DeletePostView(UserPassesTestMixin, generic.DeleteView):
    """Allow user to delete post"""
    model = Post
    template_name = 'delete_post.html'
    success_url = reverse_lazy('blogs')

    def test_func(self):
        logged_in_user = self.request.user
        current_ticket = self.get_object()

        if current_ticket.author == logged_in_user:
            return True
        else:
            return False
