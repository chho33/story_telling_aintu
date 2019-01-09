import sys
from google_images_download import google_images_download
import speech_recognition as sr
from jieba_fast.analyse import extract_tags
import jieba_fast as jieba
jieba.set_dictionary("app/dictionary.txt")
jieba.load_userdict("app/dictionary.txt")

with open("app/dictionary.txt", "r") as f:
    places_list = [d.strip().split(' ')[0] for d in f.readlines() ]  

def asr_result(way="file",file_path=None):
    counter = 0
    r = sr.Recognizer()
    if way == "mic":
        with sr.Microphone() as source:
            print("請開始說話:")
            audio = r.listen(source)
    elif way == "file":
        with sr.AudioFile(file_path) as source:
            audio = r.record(source)  # read the entire audio file
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        result = r.recognize_google(audio,language='zh-tw')
        print("辨識結果: " + result)
        return result 
    except sr.UnknownValueError:
        counter +=1
        if way == "mic":
            print("無法辨識您說的話，請再說一次好嗎？")
            if counter < 10:
                return mic_asr_result() 
            else: return  
        elif way == "file":
            print("無法辨識您的音檔，請再上傳一次好嗎？")
            sys.exit()
    except sr.RequestError as e:
        print("API出現問題，請聯絡系統管理員。 問題描述: {0}".format(e))
        return 

mic_asr_result = lambda: asr_result(way="mic") 
file_asr_result = lambda file_path: asr_result(file_path,way="file") 

def extract_places(text,way="file"):
    places = []
    tmp = extract_tags(text,allowPOS=("n","ns")) 
    
    for t in tmp:
        if t in places_list:
            places.append(t)
    if len(places) == 0:
        print("沒有找到地點耶...，不然再說一次？")
        return asr_result(way=way)
    print("找到以下幾個地點: %s"%(','.join(places)))
    return places

def download_images(places,limit=10,output_dir="downloads"): 
    config = {
        "limit":limit,
        "output_directory":output_dir,
        "keywords":",".join(places)
    } 
    response = google_images_download.googleimagesdownload()
    absolute_image_paths = response.download(config)
