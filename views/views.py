from django.shortcuts import render, reverse, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.views import generic
from django.db.models import Q
from django.utils.datastructures import MultiValueDictKeyError

from .models import Image, Keyword

class IndexView(generic.ListView):
    template_name = 'views/index.html'
    context_object_name = 'latest_images'

    def get_queryset(self):
        """Return the last five published questions."""
        return Image.objects.order_by('-pub_date')[:25]


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
        
        image.save()

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
    limit = int(getValueOr(request.GET, 'limit', '10'))

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
    images = images[page*limit:(page+1)*limit]

    context = {
        "filtered_images": images,
        "keywords": keywords,
        "page": page,
        "limit": limit,
        "suggested_keywords": suggestions
    }

    return render(request, 'views/search.html', context)

def getValueOr(dictionary, key, default):
    try:
        return dictionary[key]
    except MultiValueDictKeyError as e:
        return default