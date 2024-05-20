from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, UpdateView, DeleteView, CreateView
from django.contrib.auth.models import User
from hitcount.utils import get_hitcount_model
from hitcount.models import HitCount
from .models import News, Category, Social, Comment
from .forms import ContactForm, CommentForm
import hitcount
from django.db.models import Q
from hitcount.views import HitCountDetailView, HitCountMixin
# Create your views here.


def news_list(request):
    news_list = News.published.all()
    context = {
        "news_list": news_list
    }
    return render(request, "news/news_list.html", context=context)


def social_sytes(request):
    social_sytes = Social.objects.all()
    context = {
        'social_sytes': social_sytes
    }
    return render(request, "news/base.html", context)


def news_detail(request, news):
    news = get_object_or_404(News, slug=news, status=News.Status.Published)
    context = {}
    # hitcount logik
    hit_count = get_hitcount_model().objects.get_for_object(news)
    hits = hit_count.hits
    hitcontext = context['hitcount'] = {'pk': hit_count.pk}
    hit_count_response = HitCountMixin.hit_count(request, hit_count)
    if hit_count_response.hit_counted:
        hits = hits + 1
        hitcontext['hit_counted'] = hit_count_response.hit_counted
        hitcontext['hit_message'] = hit_count_response.hit_message
        hitcontext['total_hits'] = hits

    categories = Category.objects.all()
    comments = news.comments.filter(active=True)
    comments = Comment.objects.filter(news=news, active=True)
    comments_count = comments.count()
    comment_form = CommentForm()
    new_comment = None
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # We make new model obyect but don't create to DB
            new_comment = comment_form.save(commit=False)
            new_comment.news = news
            # izoh egasini sorov yuborayotkan userga bogladik
            new_comment.user = request.user
            # malumotlar bazasiga saqlaymiz
            new_comment.save()
    else:
        comment_form = CommentForm()
    context = {
        "news": news,
        'categories': categories,
        'comments': comments,
        'new_comment': new_comment,
        'comments_count': comments_count,
        'comment_form': comment_form,
    }
    return render(request, "news/news_detail.html", context)


def homePageView(request):
    categories = Category.objects.all()
    news_list = News.published.all().order_by("-publish_time")[:5]
    local_one = News.published.filter(category__name="Maxalliy").order_by("-publish_time")[0]
    local_news = News.published.all().filter(category__name="Maxalliy").order_by("-publish_time")[1:5]

    context = {
        'news_list': news_list,
        'categories': categories,
        'local_one': local_one,
        'local_news': local_news
    }
    return render(request, 'news/home.html', context)

class HomePageView(ListView):
    model = News
    template_name = "news/home.html"
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['news_list'] = News.published.all().order_by("-publish_time")[:5]
        context['maxalliy_xabarlar'] = News.published.all().filter(category__name="Maxalliy").order_by("-publish_time")[:5]
        context['xorijiy_xabarlar'] = News.published.all().filter(category__name="Xorij").order_by("-publish_time")[:5]
        context['texnologiya_xabarlar'] = News.published.all().filter(category__name="Texnologiya").order_by("-publish_time")[:5]
        context['sport_xabarlar'] = News.published.all().filter(category__name="Sport").order_by("-publish_time")[:5]

        return context


class ErrorPageView(TemplateView):
    model = News
    template_name = "news/404.html"
    context_object_name = 'error'

    def get(self, request):
        categories = Category.objects.all()
        news_list = News.published.all().order_by("-publish_time")[:5]
        context = {
            'news_list': news_list,
            'categories': categories,
        }
        return render(request, "news/404.html", context)



# def contactsPageView(request):
#     form = ContactForm(request.POST)
#     if request.method == "POST" and form.is_valid():
#         form.save()
#         return HttpResponse('Biz bilan boglanganingiz uchun tashakkur!')
#     context = {
#         'form': form
#     }
#     return render(request, 'news/contact.html', context)

class contactsPageView(TemplateView):
    model = News
    template_name = "news/contact.html"
    context_object_name = 'news'

    def get(self, request, *args, **kwargs):
        form = ContactForm()
        categories = Category.objects.all()
        news_list = News.published.all().order_by("-publish_time")[:5]
        context = {
            'form': form,
            'news_list': news_list,
            'categories': categories
        }
        return render(request, "news/contact.html", context)

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if request.method == "POST" and form.is_valid():
            form.save()
            return HttpResponse('<h2>Biz bilan boglanganingiz uchun tashakkur!</h2>')

        context = {
            'form': form
        }

        return render(request, 'news/contact.html', context)


class LocalNewsView(ListView):
    model = News
    template_name = "news/maxalliy.html"
    context_object_name = 'maxalliy_yangliklar'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name='Maxalliy')
        return news


class ForeignNewsView(ListView):
    model = News
    template_name = "news/xorij.html"
    context_object_name = 'xorij_yangliklar'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name='Xorij')
        return news


class TechnologyNewsView(ListView):
    model = News
    template_name = "news/technologiy.html"
    context_object_name = 'texnologik_yangliklar'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name='Texnologiya')
        return news


class SportNewsView(ListView):
    model = News
    template_name = "news/sport.html"
    context_object_name = 'sport_yangliklar'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name='Sport')
        return news


class NewsUpdateView(UpdateView):
    model = News
    fields = ('title', 'body', 'image', 'category', 'status')
    template_name = "crud/news_edit.html"



class NewsDeleteView(DeleteView):
    model = News
    template_name = "crud/news_delete.html"
    success_url = reverse_lazy('home_view')


class NewsCreateView(CreateView):
    model = News
    fields = ('title', 'slug', 'body', 'image', 'category', 'status')
    template_name = "crud/news_create.html"


def admin_page_view(request):
    admin_users = User.objects.filte(is_superuser=True)
    context={
        'admin_users': admin_users
    }
    return render(request, "pages/admin_page.html", context)


class SearchResultView(ListView, News):
    model = News
    template_name = "news/search_result.html"
    context_object_name = "barcha_yangliklar"

    # def get_queryset(self):
    #     query = self.request.GET.get('q')
    #     return News.objects.filter(
    #         Q(title__icontains=query) | Q(body__icontains=query)
    #     )
    #     # return News.objects.none()


