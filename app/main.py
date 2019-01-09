from utils import *
limit = 2
text = mic_asr_result()
places = extract_places(text)
download_images(places,limit=limit)
