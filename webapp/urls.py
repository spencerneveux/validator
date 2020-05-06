from django.conf.urls import url
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views
from .views import (
    IndexView,
    HomeView,
    UserCreate,
    RSSFeedList
)

from .views import (
    AccountUpdate,
    ProfileUpdate
)

from .views import (
    AuthorList,
    AuthorDetailView,
    AuthorCreate,
    AuthorDelete,
    AuthorUpdate,
)
from .views import (
    ArticleList,
    ArticleDetailView,
    ArticleScoreView,
    ArticleCreate,
    ArticleUpdate,
    ArticleDelete,
)
from .views import (
    PublisherArticleList,
    PublisherDetailView,
    PublisherList,
    PublisherCreate,
    PublisherUpdate,
    PublisherDelete,
)

from .views import (
    KnowledgeList,
    KnowledgeDetailView,
)

from .views import (
    BookmarkListView
)

from .views import (
    CommentCreateView,
    CommentDeleteView
)

urlpatterns = [

    # ===================
    # Base Views
    # ===================
    path("", IndexView.as_view(), name="index"),
    path("home/", HomeView.as_view(), name="home"),

    # ===================
    # Login
    # ===================
    path('accounts/', include('django.contrib.auth.urls')),

    # ===================
    # Registration
    # ===================
    path("signup", UserCreate.as_view(), name="user-add"),

    # ===================
    # Account
    # ===================
    path("account/<int:pk>", AccountUpdate.as_view(), name="account"),

    # ===================
    # Profile
    # ===================
    path("profile/<int:pk>/", ProfileUpdate.as_view(), name="profile-update"),


    # ===================
    # RSS
    # ===================
    path("rss/", RSSFeedList.as_view(), name="rss-list"),

    # ===================
    # Comment
    # ===================
    path("comment/<int:article_id>", CommentCreateView.as_view(), name="comment-add"),
    path('comment/<int:pk>/delete', CommentDeleteView.as_view(), name="comment-delete"),

    # ===================
    # Authors
    # ===================
    path("authors/", AuthorList.as_view(), name="author-list"),
    path("author/<int:pk>", AuthorDetailView.as_view(), name="author-detail"),
    path("author/add/", AuthorCreate.as_view(), name="author-add"),
    path("author/<int:pk>/", AuthorUpdate.as_view(), name="author-update"),
    path(
        "author/<int:pk>/delete", AuthorDelete.as_view(), name="author-delete"
    ),
    
    # ===================
    # Articles
    # ===================
    path("articles/", ArticleList.as_view(), name="article-list"),
    path("article/<int:pk>", ArticleDetailView.as_view(), name="article-detail"),
    path("article/score/<int:pk>", ArticleScoreView.as_view(), name="article-score"),
    path("article/add/", ArticleCreate.as_view(), name="article-add"),
    path("article/<int:pk>", ArticleUpdate.as_view(), name="article-update"),
    path(
        "article/<int:pk>/delete",
        ArticleDelete.as_view(),
        name="article-delete",
    ),
    path("articles/<publisher>/", PublisherArticleList.as_view()),
    
    # ===================
    # Publishers
    # ===================
    path("publishers/", PublisherList.as_view(), name="publisher-list"),
    path(
        "publisher/<int:pk>",
        PublisherDetailView.as_view(),
        name="publisher-detail",
    ),
    path("publisher/add", PublisherCreate.as_view(), name="publisher-add"),
    path(
        "publisher/<int:pk>",
        PublisherUpdate.as_view(),
        name="publisher-update",
    ),
    path(
        "publisher/<int:pk>/delete",
        PublisherDelete.as_view(),
        name="publisher-delete",
    ),
    
    # ===================
    # Knowledge
    # ===================
    path("knowledge/", KnowledgeList.as_view(), name="knowledge-list"),
    path("knowledge/<int:pk>", KnowledgeDetailView.as_view(), name="knowledge-detail"),

    # ===================
    # Bookmark
    # ===================
    path("bookmark/", BookmarkListView.as_view(), name="bookmark-list"),

    #====================
    # Social
    #====================
    path("social/", include('social_django.urls'), name="social"),

    # ===================
    # Utility
    # ===================
    url(r'^ajax/favorite/$', views.favorite, name='favorite'),
    url(r'^ajax/add_rss/$', views.add_rss_feed, name='add-rss'),
    url(r'^ajax/remove_rss/$', views.remove_rss_feed, name='remove-rss'),
    url(r'^ajax/bookmark/$', views.bookmark, name='bookmark'),
    url(r'^ajax/remove_bookmark/$', views.remove_bookmark, name='remove-bookmark'),
    url(r'^ajax/like/$', views.like, name='like'),
    url(r'^ajax/get_popular_rss_articles/$', views.get_popular_rss_articles, name='get-popular-rss-articles'),
    url(r'^ajax/get_popular_rss_articles/$', views.get_popular_rss_articles, name='get-popular-rss-articles'),
    url(r'^ajax/get_latest_rss_articles/$', views.get_latest_rss_articles, name='get-latest-rss-articles'),
    url(r'^ajax/search_rss/$', views.search_rss, name='search-rss'),
    url(r'^ajax/news/$', views.news, name='news'),
    url(r'^ajax/sports/$', views.sports, name='sports'),
    url(r'^ajax/tech/$', views.tech, name='tech'),
    url(r'^ajax/business/$', views.business, name='business'),
    url(r'^ajax/politics/$', views.politics, name='politics'),
    url(r'^ajax/gaming/$', views.gaming, name='gaming'),
    url(r'^ajax/set_article_details/$', views.article_details, name='set-article-details'),
    url(r'^ajax/dark_mode/$', views.dark_mode, name='dark-mode'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


