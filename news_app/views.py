from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView

from .models import News, Category
from .forms import ContactForm

# Create your views here.


def news_list(request):
    news_list = News.published.all()
    context = {
        "news_list": news_list
    }
    return render(request, "news/news_list.html", context=context)


def news_detail(request, news):
    news = get_object_or_404(News, slug=news, status= News.Status.Published)
    context = {
        "news": news
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
    template_name = "news/mahalliy.html"
    context_object_name = 'mahalliy_yangliklar'

    def get_queryset(self):
        categories = Category.objects.all()
        news = self.model.published.all().filter(category__name='Mahalliy')
        return news, categories

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


