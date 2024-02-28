import concurrent.futures
import os
import queue
import time
import locale
locale.setlocale(locale.LC_ALL, 'C')
import tesserocr
from pdf2image import convert_from_bytes


def ocr_function(doc_path):
    tesserocr_queue = queue.Queue()
    print("tesserocr", doc_path)
    final_text = {}
    def perform_ocr(img):
        tess_api = None
        # print("tess_api",tess_api)
        try:
            #print('Perform OCR started.')
            tess_api = tesserocr_queue.get(block=True, timeout=300)
            #print('Api Acquired')
            tess_api.SetImage(img[1])
            text = tess_api.GetUTF8Text()
            final_text[img[0]+1] = text
            #print('OCR performed')
            # print("text",text)
            return text
        except tesserocr_queue.Empty:
            # print('Empty exception caught!')
            return None
        finally:
            if tess_api is not None:
                # print("final")
                tesserocr_queue.put(tess_api)
                #print('Api released')


    def run_performance_test(ocr_images, num_threads):
        # print("performance")
        # Setup Queue
        for _ in range(num_threads):
            # print(_)
            # print(tesserocr.get_languages('/usr/share/tesseract-ocr/4.00/tessdata'))
            # print(tesserocr.tesseract_version())
            tesserocr_queue.put(tesserocr.PyTessBaseAPI('/usr/share/tesseract-ocr/4.00/tessdata'))

        # Perform OCR using ThreadPoolExecutor
        start = time.time()
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            res = executor.map(perform_ocr, ocr_images)
            #final_text.append(res)
        end = time.time()

        # Restoring queue
        for _ in range(num_threads):
            api = tesserocr_queue.get(block=True)
            api.End()

        tesserocr_queue.queue.clear()
        return end - start

    # Pdf to image
    print(doc_path)
    try:
        with open(doc_path, 'rb') as raw_pdf:
            print(raw_pdf)
            ocr_entities = convert_from_bytes(raw_pdf.read(), dpi=500, thread_count=4,grayscale=True)
            ocr_entities = list(enumerate(ocr_entities))
    # print(ocr_entities)
    except Exception as e:
        print("Error:",e)

    for i in range(10, 11):
        print(f'Starting OCR extraction with {i} threads')
        total_time = run_performance_test(ocr_entities, i)
        print(f'OCR extraction {i} threads and took {str(total_time)} time')
    
    # print(f'Starting performance test with {i} threads')
    # total_time = run_performance_test(ocr_entities, i)
    # print(f'Performed test with {i} threads and took {str(total_time)} time')
    return final_text

# ocr_function("D:\doc_extraction_openai\Alight.pdf")