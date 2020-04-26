from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.template import loader
from .models import Image
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
                'processed': x.processed_url,
                'params': {
                    'lower': x.lower_thresh,
                    'upper': x.upper_thresh,
                }
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
            processed_url = '/media/processed/' + image.name
            processed_output_path = './media/processed/' + image.name
            lower_thresh = clean_data['lower_thresh']
            upper_thresh = clean_data['upper_thresh']
            new_image = Image(
                name=clean_data['name'],
                created_at=timezone.now(),
                image=image,
                processed_url=processed_url,
                lower_thresh=lower_thresh,
                upper_thresh=upper_thresh)
            new_image.save()
            input_img = '.' + new_image.image.url
            image_processing.preprocess(
                path=input_img,
                output_path=processed_output_path,
                lower_thresh=lower_thresh,
                upper_thresh=upper_thresh)
            return HttpResponseRedirect('/')
    else:
        form = AddImageForm()
    template = loader.get_template('image/add.html')
    context = {
        'form': form
    }
    return HttpResponse(template.render(context, request))
