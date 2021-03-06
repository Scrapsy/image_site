from django.shortcuts import render, reverse, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.views import generic
from django.db.models import Q
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.decorators import login_required

from .models import Image, Keyword


class IndexView(generic.ListView):
    template_name = 'views/index.html'
    context_object_name = 'latest_images'

    def get_queryset(self):
        page = self.request.GET.get('page', 0)
        limit = self.request.GET.get('limit', 25)
        page = int(page)
        limit = int(limit)
        start = page * limit
        end = (page + 1) * limit
        if start < 0:
            start = 0
            end = limit
        return Image.objects.order_by('-pub_date')[start:end]

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        page = self.request.GET.get('page', 0)
        page = int(page)
        ctx['last_page'] = page - 1
        ctx['page'] = page
        ctx['next_page'] = page + 1
        ctx['limit'] = self.request.GET.get('limit', 25)
        return ctx


@login_required
def submit(request):
    if request.method == "POST":
        try:
            image_image = request.FILES["image_image"]
            image_title = request.POST["image_title"]
            image_description = request.POST["image_description"]
            image_keywords = request.POST["image_keywords"]
            pub_date = timezone.now()
        except KeyError as ke:
            print("Key error({0})".format(ke))
            print(request.POST)
            return render(request, 'views/submit.html', {
                'error_message': "Information missing.",
            })
        image = Image(
            title=image_title,
            description=image_description,
            keywords=image_keywords,
            pub_date=pub_date)

        splits = image_image.name.split(".")
        filetype = splits[len(splits)-1:]
        image_image.name = "{0}.{1}".format(str(image.id), filetype)
        image.image = image_image
        image.save()

        for key in image_keywords.split(","):
            new_key, created = Keyword.objects.get_or_create(keyword=key.strip().lower())
            new_key.uses += 1
            new_key.save()

        return HttpResponseRedirect(reverse('views:show', args=(image.id,)))
    else:
        suggestions = []
        for word in Keyword.objects.all():
            suggestions.append(word.keyword)
        suggestions.sort()
        context = {
            "suggested_keywords": suggestions
        }
        return render(request, 'views/submit.html', context)


@login_required
def update(request, pk):
    if request.method == "POST":
        try:
            image_id = pk
            image_title = request.POST["image_title"]
            image_description = request.POST["image_description"]
            image_keywords = request.POST["image_keywords"]
            pub_date = timezone.now()
        except KeyError as ke:
            print("Key error({0})".format(ke))
            print(request.POST)
            return render(request, 'views/submit.html', {
                'error_message': "Information missing.",
            })
        image = Image.objects.get(id=image_id)
        image.title=image_title
        image.description=image_description
        image.keywords=image_keywords
        image.pub_date=pub_date

        image.save()

        for key in image_keywords.split(","):
            new_key, created = Keyword.objects.get_or_create(keyword=key.strip().lower())
            new_key.uses += 1
            new_key.save()

        return HttpResponseRedirect(reverse('views:show', args=(image.id,)))
    else:
        image = Image.objects.get(id=pk)
        suggestions = []
        for word in Keyword.objects.all():
            suggestions.append(word.keyword)
        suggestions.sort()
        context = {
            "suggested_keywords": suggestions,
            "image": image
        }
        return render(request, 'views/edit.html', context)


class ShowView(generic.DetailView):
    model = Image
    template_name = 'views/show.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        keywords = context['image'].keywords
        context['keywords'] = keywords.split(",")
        return context


def search(request):
    keywords = getValueOr(request.GET, 'keywords', '')
    page = int(getValueOr(request.GET, 'page', '0'))
    limit = int(getValueOr(request.GET, 'limit', '25'))
    page = int(page)
    limit = int(limit)

    suggestions = []
    for word in Keyword.objects.all():
        suggestions.append(word.keyword)
    suggestions.sort()

    if len(keywords) == 0:
        context = {
            "keywords": keywords,
            "page": page,
            "limit": limit,
            "suggested_keywords": suggestions
        }
        return render(request, 'views/search.html', context)
    keys = keywords.split(",")

    # This seems like poor poor database handling to me...
    # But I'm too lazy to fix it right now... so eh?
    images = Image.objects.all()
    for key in keys:
        images = images.filter(Q(keywords__contains=key.strip().lower()))
    start = page*limit
    end = (page+1)*limit
    if start < 0:
        start = 0
        end = limit
    images = images[start:end]

    context = {
        "filtered_images": images,
        "keywords": keywords,
        "page": page,
        "last_page": page-1,
        "next_page": page+1,
        "limit": limit,
        "suggested_keywords": suggestions
    }

    return render(request, 'views/search.html', context)

def keywords(request):
    keywords = Keyword.objects.all().order_by('keyword')
    max_uses = 0
    for keyword in keywords:
        if max_uses < keyword.uses:
            max_uses = keyword.uses

    for keyword in keywords:
        keyword.fontsize = 30 + ((keyword.uses - max_uses) / max_uses) * 16
        if 30 < keyword.fontsize:
            keyword.fontsize = 30

    context = {
        "keywords": keywords
    }
    return render(request, 'views/keywords.html', context)


def getValueOr(dictionary, key, default):
    try:
        return dictionary[key]
    except MultiValueDictKeyError:
        return default