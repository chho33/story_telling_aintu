from django.shortcuts import render,redirect
from django.utils import timezone
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt

from project.settings import MEDIA_ROOT,STATICFILES_DIRS 
from PIL import Image
import glob
import os
import speech_recognition as sr
from .models import AudioFile 
from .utils import *

# Create your views here.
def index(request):
    return render(request,'index.html',{})

def append(request):
    return render(request,'append_pic.html',{})

def edit(request):
    return render(request,'ImageEdit.html',{})

def save_audio():
    pass

@csrf_exempt
def find_images(request):
    data = request.FILES['audio_data'] 
    #data:  <class 'django.core.files.uploadedfile.InMemoryUploadedFile'>
    audio_name = data.name 
    audio_tmp_path = os.path.join(MEDIA_ROOT, 'audio/%s'%audio_name)
    audio_tmp_path = default_storage.save(audio_tmp_path, ContentFile(data.read()))

    #ASR
    r = sr.Recognizer()
    with sr.AudioFile(audio_tmp_path) as source:
        audio = r.record(source)
    result = r.recognize_google(audio,language='zh-tw')
    tags = extract_places(result)

    #save audio to DB
    AudioFile.objects.create(\
        **{'name':audio_name,
        'tags':(',').join(tags),
        'parse':result,
        'audio_file':data}
    ) 

    #download images
    output_dir = os.path.join(STATICFILES_DIRS[0],'downloads/')
    tags_for_down = []
    for tag in tags:
        if not os.path.exists(os.path.join(output_dir,tag)):
            tags_for_down.append(tag)
    if len(tags_for_down) > 0:
        download_images(tags_for_down,limit=2,output_dir=output_dir)

    #image response
    image_dir = os.path.join(output_dir,tags[0])
    image_file = os.path.basename(glob.glob('%s/*'%image_dir)[0])
    image_file = os.path.join(image_dir,image_file)
    print('image_file: ',image_file)
    try:
        with open(image_file, "rb") as f:
            return HttpResponse(f.read(), content_type="image/jpeg")
    except IOError:
        red = Image.new('RGBA', (1, 1), (255,0,0,0))
        response = HttpResponse(content_type="image/jpeg")
        red.save(response, "JPEG")
        return response
