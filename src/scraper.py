import os
import ssl
import torch
import PyPDF2
import traceback
import urllib.request
import pypdfium2 as pdfium

from PIL import Image
from time import sleep
from io import BytesIO
from TTS.api import TTS
from bs4 import BeautifulSoup
from pytesseract import image_to_string

file_path = os.path.join(os.getcwd(), "pdfs")
context = ssl._create_unverified_context() # Ignore SSL certificate errors
device = "cuda" if torch.cuda.is_available() else "cpu"

# Init TTS
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

def collect_links(url):

    webpage_html = urllib.request.urlopen(url, context=context).read()

    webpage = BeautifulSoup(webpage_html, "html.parser")

    a_elements = webpage.find_all('a', href=lambda href: href and href.startswith('/Portals/'))

    hrefs = [f"{url}{a['href']}" for a in a_elements]

    return hrefs

def download_pdf(links):
    try:
        for link in links[:1]: # get the first link which is latest pdf
            link_splitted = link.split("/")
            pdf_name = link_splitted[6].split("?")[0]

            # check pdfid.txt file is created if it is not create it and write 0.pdf to it
            if not os.path.exists('pdfid.txt'):
                with open('pdfid.txt', 'w') as f:
                    f.write("0.pdf")
                    f.close()

            # read the last pdf name which is downloaded and highes number
            with open('pdfid.txt', 'r') as f:
                last_pdf_name = int(f.read().split('.')[0])
                f.close()

            # if current downloaded pdf is higher than the last one, download it because it is the latest
            if int(pdf_name.split('.')[0]) > last_pdf_name:

                file_name = f"{link_splitted[4]}-{link_splitted[5]}-{pdf_name}"
                save_path = os.path.join(file_path, file_name)

                # write the current pdf name to the file
                with open('pdfid.txt', 'w') as f:
                    f.write(pdf_name)
                    f.close()

                # download the pdf
                with urllib.request.urlopen(link, context=context) as response:
                    with open(save_path, 'wb') as out_file:
                        out_file.write(response.read())

                return True

            sleep(0.1)
        return False
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        return False

def extract_text_with_pytesseract(list_dict_final_images):

    image_list = [list(data.values())[0] for data in list_dict_final_images]
    image_content = []

    for index, image_bytes in enumerate(image_list):

        image = Image.open(BytesIO(image_bytes))
        raw_text = str(image_to_string(image))
        image_content.append(raw_text)

    return "\n".join(image_content)

def convert_pdf_to_images(file_path, scale=300/72):

    pdf_file = pdfium.PdfDocument(file_path)
    page_indices = [i for i in range(len(pdf_file))]

    renderer = pdf_file.render(
        pdfium.PdfBitmap.to_pil,
        page_indices = page_indices,
        scale = scale,
    )

    list_final_images = []

    for i, image in zip(page_indices, renderer):

        image_byte_array = BytesIO()
        image.save(image_byte_array, format='jpeg', optimize=True)
        image_byte_array = image_byte_array.getvalue()
        list_final_images.append(dict({i:image_byte_array}))

    return list_final_images

def convert_text_to_audio(text, language):
    # read pdf id from the text located in the pdfid.txt file

    with open('pdfid.txt', 'r') as f:
        last_pdf_name = f.read().split('.')[0]
        f.close()

    tts.tts_to_file(text=text, speaker_wav="audios/audio.wav", language=language, file_path=f"pdfs/{last_pdf_name}.wav")

if __name__ == "__main__":
    #TODO: in final step make this script run in a loop and check the website every 1 hour
    links = collect_links("https://basimevi.gov.ct.tr")
    is_downloaded = download_pdf(links)
    if is_downloaded:
        pdf_file = os.path.join(file_path, os.listdir(file_path)[0])
        image_pdf_pages = convert_pdf_to_images(pdf_file)
        extracted_text = extract_text_with_pytesseract(image_pdf_pages)
        convert_text_to_audio(extracted_text, "tr")