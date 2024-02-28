from flask import Flask, jsonify, request
import os
import logging
from concurrent.futures import ThreadPoolExecutor
# from run_ocr import ocr_function
from run_model import filter_excel_embed

app = Flask(__name__)

def perform_ocr_task(doc_path):
    print(doc_path)
    result = filter_excel_embed(doc_path)
    print(result)
    return result

@app.route('/perform_ocr',  methods=['GET', 'POST'])
def perform_ocr():
    try:
        # if 'file' not in request.files:
        #     return jsonify({'error': 'No file provided'}), 400

        # file = request.files['file']
        # print(file)
        # Process the file (perform OCR, etc.)
        # Your OCR function can use the file object directly, e.g., ocr_function(file)
        perform_ocr_task(r"Alight.pdf")
        # Return some response if needed
        # model_prediction()
        return jsonify({'result': 'OCR processing successful'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# @app.route('/perform_ocr',  methods=['GET', 'POST'])
# def perform_ocr():
#     try:
#         if 'file' not in request.files:
#             return jsonify({'error': 'No file provided'}), 400

#         file = request.files['file']
#         print("perform file 5001",file)
#         if file.filename == '':
#             return jsonify({'error': 'No selected file'}), 400

#         if file:
#             print("inside file")
#             file_path = os.path.join(os.getcwd(), 'uploaded_file.pdf')  # Save the file temporarily
#             file.save(file_path)

#             # num_threads = request.form.get('num_threads', default=4, type=int)

#             with ThreadPoolExecutor(max_workers=1) as executor:
#                 future = executor.submit(perform_ocr_task, file_path)
#                 result = future.result()

#             os.remove(file_path)  # Remove the temporary file

#             return jsonify({'result': result})
#     except Exception as e:
#         logging.info(f"{e}")
#         return jsonify({"error":str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5003, host='0.0.0.0')
