from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.template import loader
from .models import LoadedImage, Biometric
from .forms import AddImageForm
from django.utils import timezone
from .preprocess import image_processing
from django.core.files import File
import uuid


def index(request):
    latest = Biometric.objects.order_by('-created_at')[:5]
    template = loader.get_template('image/latest.html')
    objects = []
    for x in latest:
        objects.append(
            {
                'name': x.name,
                'created_at': x.created_at,
                'orig': x.image_url,
                'preprocessed': x.preprocessed_url,
                'gauss': x.gauss_url,
                'grabcut': x.grabcut_url,
                'grabcut_gauss': x.grabcut_gauss_url,
                'params': {
                    'lower': x.lower_thresh,
                    'upper': x.upper_thresh,
                    'denoise': x.denoise_lvl,
                    'clahe': x.clahe_lvl,
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
            linked_id = str(uuid.uuid4())
            image = clean_data['image']
            lower_thresh = clean_data['lower_thresh']
            upper_thresh = clean_data['upper_thresh']
            denoise_lvl = clean_data['denoise_lvl']
            clahe_lvl = clean_data['clahe_lvl']
            gauss_block_size = clean_data['gauss_block_size']
            gauss_constant = clean_data['gauss_constant']
            new_image = LoadedImage(
                id=linked_id,
                created_at=timezone.now(),
                image=image,
            )
            new_image.save()
            img_name = new_image.image.name.split('/')[1]
            img_url = new_image.image.url
            input_img = '.' + new_image.image.url
            preprocessed_url = '/media/preprocessed/' + img_name
            preprocessed_output_path = './media/preprocessed/' + img_name
            gauss_url = '/media/gauss/' + img_name
            gauss_output_path = './media/gauss/' + img_name
            grabcut_url = '/media/grabcut/' + img_name
            grabcut_output_path = './media/grabcut/' + img_name
            grabcut_gauss_url = '/media/grabcut_gauss/' + img_name
            grabcut_gauss_output_path = './media/grabcut_gauss/' + img_name
            image_processing.preprocess(
                input_path=input_img,
                preprocessed_path=preprocessed_output_path,
                gauss_path=gauss_output_path,
                grabcut_path=grabcut_output_path,
                grabcut_gauss_output_path=grabcut_gauss_output_path,
                lower_thresh=lower_thresh,
                upper_thresh=upper_thresh,
                denoise_lvl=denoise_lvl,
                clahe_lvl=clahe_lvl,
                gauss_block_size=gauss_block_size,
                gauss_constant=gauss_constant
            )
            new_biometric = Biometric(
                id=linked_id,
                name=clean_data['name'],
                created_at=timezone.now(),
                image_name=img_name,
                image_url=img_url,
                preprocessed_url=preprocessed_url,
                gauss_url=gauss_url,
                grabcut_url=grabcut_url,
                grabcut_gauss_url=grabcut_gauss_url,
                lower_thresh=lower_thresh,
                upper_thresh=upper_thresh,
                denoise_lvl=denoise_lvl,
                clahe_lvl=clahe_lvl,
                gauss_block_size=gauss_block_size,
                gauss_constant=gauss_constant
            )
            new_biometric.save()
            return HttpResponseRedirect('/')
    else:
        form = AddImageForm()
    template = loader.get_template('image/add.html')
    context = {
        'form': form
    }
    return HttpResponse(template.render(context, request))
