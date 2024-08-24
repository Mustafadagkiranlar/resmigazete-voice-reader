import os
import ssl
import PyPDF2
import urllib.request
import pypdfium2 as pdfium

from PIL import Image
from io import BytesIO
from time import sleep
from bs4 import BeautifulSoup
from pytesseract import image_to_string

file_path = os.path.join(os.getcwd(), "pdfs")
context = ssl._create_unverified_context() # Ignore SSL certificate errors

def collect_links(url):

    webpage_html = urllib.request.urlopen(url, context=context).read()

    webpage = BeautifulSoup(webpage_html, "html.parser")

    a_elements = webpage.find_all('a', href=lambda href: href and href.startswith('/Portals/'))

    hrefs = [f"{url}{a['href']}" for a in a_elements]

    return hrefs

def download_pdf(links):

    #TODO: IN PRODUCTION CODE, YOU SHOULD USE A FOR LOOP TO DOWNLOAD ALL PDFs REMOVE [:1]
    try:
        for link in links[:10]:
            link_splitted = link.split("/")
            pdf_name = link_splitted[6].split("?")[0]
            file_name = f"{link_splitted[4]}-{link_splitted[5]}-{pdf_name}"
            save_path = os.path.join(file_path, file_name)

            with urllib.request.urlopen(link, context=context) as response:
                with open(save_path, 'wb') as out_file:
                    out_file.write(response.read())
            sleep(0.1)
        return True
    except Exception as e:
        print(e)
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

if __name__ == "__main__":
    # links = collect_links("https://basimevi.gov.ct.tr")
    # if download_pdf(links) == True:
        # TODO: you need to find the newly downloaded pdf file and read it in this implementation it is the one with the index 1
        # find pdf path to convert it into images
        pdf_file = os.path.join(file_path, os.listdir(file_path)[1])
        image_pdf_pages = convert_pdf_to_images(pdf_file)
        extracted_text = extract_text_with_pytesseract(image_pdf_pages)
        print(extracted_text)

