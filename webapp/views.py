import os
import requests
from django.utils import timezone
from django.urls import reverse_lazy, reverse
from django.core import serializers
from django.shortcuts import redirect
from google.cloud.language_v1 import enums
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView
from django.http import JsonResponse
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.core.mail import send_mail

from .forms import ContactForm



from django.views.generic.edit import (
    CreateView,
    DeleteView,
    UpdateView,
    FormView
)
from .models import (
    Author,
    Article,
    Publisher,
    Score,
    Entity,
    Category,
    MetaData,
    Knowledge,
    User,
    Profile,
    RSSFeed,
    Like,
    Comment,
    CommentForm,
    Favorite,
    Bookmark,
    RSS,
    UserForm,
    ProfileForm,
)


# =========================
# Base Views
# =========================
class IndexView(FormView):
    template_name = "webapp/index.html"
    form_class = ContactForm
    success_url = '.'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        from_email = form.cleaned_data['from_email']
        subject = form.cleaned_data['subject']
        message = form.cleaned_data['message']
        send_mail(subject, message, from_email,
                  ['projectvalidator2019@gmail.com', ])

        return super(IndexView, self).form_valid(form)



class HomeView(ListView):
    model = Article
    template_name = "webapp/home.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rssfeed_list'] = RSSFeed.objects.all()
        return context

# =========================
# User
# =========================
class UserCreate(CreateView):
    form_class = UserForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("login")


# =========================
# Account
# =========================
class AccountUpdate(UpdateView):
    model = User
    fields = ('email',)
    success_url = reverse_lazy("account")
    template_name = "webapp/account_form.html"

    def get_success_url(self):
        return reverse('account', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_form'] = ProfileForm()
        return context

# =========================
# Profile
# =========================
class ProfileUpdate(UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = "webapp/profile_form.html"

    def get_success_url(self):
        return reverse('account', kwargs={'pk': self.object.user.id})

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

# =========================
# RSS Feeds
# =========================
class RSSFeedList(ListView):
    model = RSSFeed

# =========================
# Comments
# =========================
class CommentCreateView(CreateView):
    form_class = CommentForm
    template_name = "webapp/comment_form.html"

    def form_valid(self, form):
        article = Article.objects.get(pk=self.kwargs['article_id'])
        form.instance.user = self.request.user
        form.instance.article = article
        return super(CommentCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['article'] = Article.objects.get(pk=self.kwargs['article_id'])
        return context

class CommentDeleteView(DeleteView):
    model = Comment
    success_url = reverse_lazy('home')


# =========================
# Articles
# =========================
class ArticleList(ListView):
    model = Article

class ArticleDetailView(DetailView):
    model = Article

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm
        return context

class ArticleScoreView(DetailView):
    model = Article
    template_name = "webapp/article_score.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["score_list"] = Score.objects.order_by("score")
        context["entity_list"] = Entity.objects.order_by("name")
        context["author_article_list"] = Article.objects.filter(author=self.object.author)
        context["article_list"] = Article.objects.filter(category__name=self.object.category.name)[:3]
        context["category"] = self.object.get_categories()
        return context


class ArticleCreate(CreateView):
    model = Article
    fields = "__all__"


class ArticleUpdate(UpdateView):
    model = Article
    fields = "__all__"


class ArticleDelete(DeleteView):
    model = Article
    success_url = reverse_lazy("article-list")


# =========================
# Authors
# =========================
class AuthorList(ListView):
    model = Author


class AuthorDetailView(DetailView):
    model = Author

    def get_object(self):
        obj = super().get_object()
        obj.last_accessed = timezone.now()
        obj.save()
        return obj


class AuthorCreate(CreateView):
    model = Author
    fields = "__all__"


class AuthorUpdate(UpdateView):
    model = Author
    fields = "__all__"


class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy("author-list")


# =========================
# Publishers
# =========================
class PublisherArticleList(ListView):
    template_name = "webapp/articles_by_publisher.html"

    def get_queryset(self):
        self.publisher = get_object_or_404(Publisher, name=self.kwargs["publisher"])
        return Article.objects.filter(publisher=self.publisher)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["publisher"] = self.publisher
        return context


class PublisherDetailView(DetailView):
    model = Publisher


class PublisherList(ListView):
    model = Publisher
    context_object_name = "publisher_list"


class PublisherCreate(CreateView):
    model = Publisher
    fields = "__all__"


class PublisherUpdate(UpdateView):
    model = Publisher
    fields = "__all__"


class PublisherDelete(DeleteView):
    model = Publisher
    success_url = reverse_lazy("publisher-list")


# =========================
# Knowledge 
# =========================
class KnowledgeList(ListView):
    model = Knowledge


class KnowledgeDetailView(DetailView):
    model = Knowledge


# =========================
# Bookmarks
# =========================
class BookmarkListView(ListView):
    model = Bookmark

# =========================
# Utility 
# =========================
@receiver(user_logged_in)
def got_online(sender, user, request, **kwargs):
    user.profile.is_online = True
    user.profile.save()

@receiver(user_logged_out)
def got_offline(sender, user, request, **kwargs):  
    user.profile.is_online = False
    user.profile.save()


def like(request):
    article_id = request.GET.get('article-id')
    operation = request.GET.get('operation')

    like, created = Like.objects.get_or_create(user=request.user, article_id=article_id)
    if operation == "like":
        if like.is_liked:
            data = {
                'Test': 'Liked'
            }
        else:
            like.is_liked = True
            like.save()
            data = {
                'Test': 'Like'
            }
    elif operation == "dislike":
        if like.is_liked == False:
            data = {
                'Test': 'Disliked'
            }
        else:
            like.is_liked = False
            like.save()
            data = {
                'Test': 'Dislike'
            }

    return JsonResponse(data)


def favorite(request):
    article_id = request.GET.get('article-id')
    new_dislike, added = Favorite.objects.get_or_create(user=request.user, article_id=article_id)

    if added:
        data = {
            'Test': True
        }
    else:
        data = {
            'Test': False
        }

    return JsonResponse(data)


def bookmark(request):
    article_id = request.GET.get('article-id')
    bookmark, bookmarked = Bookmark.objects.get_or_create(user=request.user, article_id=article_id)
    if not bookmark.is_bookmarked:
        bookmark.is_bookmarked = True
        bookmark.save()
        data = {
            'Test': True
        }
    else:
        data = {
            'Test': False
        }

    return JsonResponse(data)

def remove_bookmark(request):
    article_id = request.GET.get('article-id')
    bookmark = Bookmark.objects.get(user=request.user, article_id=article_id)
    print(bookmark.is_bookmarked)
    if bookmark.is_bookmarked:
        bookmark.is_bookmarked = False
        bookmark.save()
        data = {
            'Test': True
        }
    else:
        data = {
            'Test': False
        }

    return JsonResponse(data)

def add_rss_feed(request):
    rss_id = request.GET.get('rss-id')

    rss, added = RSS.objects.get_or_create(user=request.user, rss_id=rss_id)
    print(rss.feed_added)

    # Add feed if not added
    if not rss.feed_added:
        rss.feed_added = True
        rss.feed_removed = False
        rss.save()
        data = {
            'Test': True
        }
    else:
        data = {
            'Test': False
        }

    return JsonResponse(data)


def remove_rss_feed(request):
    rss_id = request.GET.get('rss-id')

    rss, removed = RSS.objects.get_or_create(user=request.user, rss_id=rss_id)

    # Remove feed if it has been added
    if not rss.feed_removed:
        rss.feed_added = False
        rss.feed_removed = True
        rss.save()
        data = {
            'Test': True
        }
    else:
        data = {
            'Test': False
        }

    return JsonResponse(data)


def get_popular_rss_articles(request):
    rss_id = request.GET.get('rss-id')
    rss_feed = RSSFeed.objects.get(pk=rss_id)

    if rss_feed:
        article_list = rss_feed.get_popular_article_list()
        article_data_list = []
        article_stats = {}
        for article in article_list:
            article_data = {
                'id': article.id,
                'rss_feed_id': article.rss_feed_id,
                'title': article.title,
                'publisher': article.publisher,
                'author': article.author,
                'content': article.content,
                'date': article.date
            }
            article_stats[article.id] = ('likes', article.get_likes(), 'comments', article.get_total_comments())
            article_data_list.append(article_data)
        data = {
            'Test': True,
            'article_list': article_data_list,
            'article_stats': article_stats,
        }
    else:
        data = {
            'Test': False
        }

    return JsonResponse(data)


def get_latest_rss_articles(request):
    rss_id = request.GET.get('rss-id')
    rss_feed = RSSFeed.objects.get(pk=rss_id)

    if rss_feed:
        article_list = rss_feed.get_latest_article_list()
        article_data_list = []
        article_stats = {}
        for article in article_list:
            article_data = {
                'id': article.id,
                'rss_feed_id': article.rss_feed_id,
                'title': article.title,
                'publisher': article.publisher,
                'author': article.author,
                'content': article.content,
                'date': article.date
            }
            article_stats[article.id] = ('likes', article.get_likes(), 'comments', article.get_total_comments())
            article_data_list.append(article_data)
        data = {
            'Test': True,
            'article_list': article_data_list,
            'article_stats': article_stats,
        }
    else:
        data = {
            'Test': False
        }

    return JsonResponse(data)

def search_rss(request):
    query = request.GET.get('search')
    results = RSSFeed.objects.filter(name__contains=query)

    # TODO: Search for feed description
    print(results)

    if results:
        data = {
            'Test': True,
            'results': list(results.values()),
        }
    else:
        data = {
            'Test': False,
        }
    return JsonResponse(data)

def news(request):
    results = RSSFeed.objects.filter(category="News")

    if results:
        data = {
            'Test': True,
            'results': list(results.values()),
        }
    else:
        data = {
            'Test': False,
        }

    return JsonResponse(data)

def tech(request):
    results = RSSFeed.objects.filter(category="Tech")

    if results:
        data = {
            'Test': True,
            'results': list(results.values()),
        }
    else:
        data = {
            'Test': False,
        }

    return JsonResponse(data)

def sports(request):
    results = RSSFeed.objects.filter(category="Sports")

    if results:
        data = {
            'Test': True,
            'results': list(results.values()),
        }
    else:
        data = {
            'Test': False,
        }

    return JsonResponse(data)

def business(request):
    results = RSSFeed.objects.filter(category="Business")

    if results:
        data = {
            'Test': True,
            'results': list(results.values()),
        }
    else:
        data = {
            'Test': False,
        }

    return JsonResponse(data)

def gaming(request):
    results = RSSFeed.objects.filter(category="Gaming")

    if results:
        data = {
            'Test': True,
            'results': list(results.values()),
        }
    else:
        data = {
            'Test': False,
        }

    return JsonResponse(data)

def politics(request):
    results = RSSFeed.objects.filter(category="Politics")

    if results:
        data = {
            'Test': True,
            'results': list(results.values()),
        }
    else:
        data = {
            'Test': False,
        }

    return JsonResponse(data)

def article_details(request):
    profile = Profile.objects.get(user=request.user)

    if profile.article_details:
        profile.article_details = False
        profile.save()
        data = {
            'Test': False
        }
    else:
        profile.article_details = True
        profile.save()
        data = {
            'Test': True
        }

    return JsonResponse(data)

def dark_mode(request):
    profile = Profile.objects.get(user=request.user)

    if profile.dark_mode:
        profile.dark_mode = False
        profile.save()
        data = {
            'Test': False
        }
    else:
        profile.dark_mode = True
        profile.save()
        data = {
            'Test': True
        }

    return JsonResponse(data)



def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('account/')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return redirect(request, 'account_form.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })