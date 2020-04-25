from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.template import loader
from .models import Image, ProcessedImage
from .forms import AddImageForm
from django.utils import timezone
from .preprocess import image_processing
from django.core.files import File


def index(request):
    latest = Image.objects.order_by('-created_at')[:5]
    template = loader.get_template('image/latest.html')
    objects = []
    for x in latest:
        objects.append(
            {
                'name': x.name,
                'created_at': x.created_at,
                'orig': x.image.url,
                'processed': x.image.url.replace('image', 'processed')
            }
        )
    context = {
        'objects': objects,
    }
    return HttpResponse(template.render(context, request))


def add_image(request: HttpRequest):
    if request.method == 'POST':
        form = AddImageForm(request.POST, request.FILES)
        if form.is_valid():
            clean_data = form.cleaned_data
            image = clean_data['image']
            new_image = Image(
                name=clean_data['name'],
                created_at=timezone.now(),
                image=image)
            new_image.save()
            img_name = new_image.image.name.split('/')[1]
            processed_image_path = './media/processed/' + img_name
            image_processing.preprocess(
                path='.' + new_image.image.url,
                output_path=processed_image_path,
                lower_thresh=145,
                upper_thresh=255)
            new_processed_image = ProcessedImage(
                name=clean_data['name'] + 'processed',
                url='/media/processed/' + img_name
            )
            new_processed_image.save()
            return HttpResponseRedirect('/')
    else:
        form = AddImageForm()
    template = loader.get_template('image/add.html')
    context = {
        'form': form
    }
    return HttpResponse(template.render(context, request))
