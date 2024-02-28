import time
import os
import run_ocr as ro
from multiprocessing.pool import ThreadPool
import re
import pandas as pd

def get_page_text(pageNo,pdf_data):
    encode_pageno = []
    encode_para = []
    try:
        pdf_page_data = re.sub(r""+"\.\\n\\n"+"|\.\s+\\n\\n|\\n\\n[A-Za-z]\.|\\n\\n\([A-Za-z]\)|\\n\\n[A-Za-z]\)|\\n\\n\d{0,2}\.|\\n\\n\(\d{0,2}\)|\\n\\n\d{0,2}\)"+"|"+"\\n\\n"+"(?=[MDCLXVI])M{0,4}(?:CM|CD|D?C{0,3})(?:XC|XL|L?X{0,3})(?:IX|IV|V?I{0,3})"+"\s+"+"|"+"\\n\\n\("+"(?=[MDCLXVI])M{0,4}(?:CM|CD|D?C{0,3})(?:XC|XL|L?X{0,3})(?:IX|IV|V?I{0,3})\)"+"\s+"+"|"+"\\n\\n\("+"(?=[MDCLXVI])M{0,4}(?:CM|CD|D?C{0,3})(?:XC|XL|L?X{0,3})(?:IX|IV|V?I{0,3})"+"\s+"+"|"+"\\n\\n"+"(?=[MDCLXVI])M{0,4}(?:CM|CD|D?C{0,3})(?:XC|XL|L?X{0,3})(?:IX|IV|V?I{0,3})\)"+"\s+"+"|"+"\\n\\n"+"(?=[MDCLXVI])M{0,4}(?:CM|CD|D?C{0,3})(?:XC|XL|L?X{0,3})(?:IX|IV|V?I{0,3})"+"\\."+"\s+"+"|"+":\\n\\n"+"|"+":\s+\\n\\n","@#$&",pdf_data[pageNo])
        for line in pdf_page_data.split("@#$&"):
            time.sleep(1)
        #pdf_page_data = re.sub("\. \\n\\n","\.\\n\\n",pdf_data[keys])
        #for line in pdf_page_data.split(".\n\n"):
            text_Val = line.strip()
            if text_Val != ' ' and text_Val != '' and len(text_Val.split(" ")) > 5 :
                encode_pageno.append(pageNo)
                encode_para.append(text_Val)
    except Exception as e:
        print(e)
        raise
    finally:
        return encode_pageno, encode_para


def model_prediction(doc_input):
    global df
  
    if '.pdf' in doc_input or '.PDF' in doc_input:
    #print("run_Model->",os.path.isfile(doc_input))
        start = time.time()
        try:
            cnt = 0
            if os.path.isfile(doc_input):
                try:
                #pdf_data = run_PDF_ext2.convert_pdf_to_txt(doc_input)
                    pdf_data = ro.ocr_function(doc_input)
                    #
                    # print(ro.ocr_function(doc_input))
                except Exception as e:
                    print(e)
                    cnt = cnt + 1
                    time.sleep(0.5)
        except Exception as e:
            print(e)
            raise
        
    else:
        # logger.info("\n -->File Format not supported!")
        exit()
    encode_pageno = []
    encode_para = []
    print(f"pdf has {len(pdf_data.keys())} pages")
    #   write_json(f"In Document Extraction process" ,25, os.path.basename(doc_input))
    
    with ThreadPool(processes=10) as pool:
        results = pool.starmap(get_page_text, map(lambda x: (x,pdf_data.copy()), pdf_data.keys()))
        for res in results:
            if res:
                encode_pageno.extend(res[0])
                encode_para.extend(res[1])
    
    encode_data = pd.DataFrame({'PageNo': encode_pageno, 'Para': encode_para})
    encode_data = encode_data.sort_values('PageNo')
    # print(encode_data) 
    encode_data.to_csv("encodedata.csv") #Generate CSV file ######
    print(f"Document Extraction Time--> {time.time()-start}")
    #   logger.info(f"Document Extraction Time--> {time.time()-start}")
    del encode_pageno, encode_para

    #   df_exp_ms = pd.DataFrame({"input":msmarco_input_list,"ep":expected_output})
    #   df_exp_ms = df_exp_ms.drop_duplicates(subset=['input','ep'], keep="first")

    #   write_json(f"In Semantic process",50,os.path.basename(doc_input))
    
    start = time.time()
    # print(encode_data)
    # encode_data.to_excel('encode_data.xlsx', index=False)
    return encode_data
        
# model_prediction("D:\doc_extraction_openai\Alight.pdf")

def filter_excel_embed(doc_input):
    json_data = {
        "search_value":["Insurance"],
        "conditions":[">="],
        "expt_value":["1 Million"],
        "category":["Insurance"]             
        }

    # Assuming sys.xlsx is your Excel file
    df = pd.read_excel("synonyms_dic.xlsx")

    # Initialize an empty dataframe to store the filtered data
    filtered_df = pd.DataFrame()

    for i, search_value in enumerate(json_data["search_value"]):
        # Find the corresponding key_no from the sys.xlsx dataframe
        key_no = df[df["Search_Value"].str.lower() == search_value.lower()]["Key_No"].values

        # If key_no is found, filter the data based on that key_no
        if key_no.any():
            key_no = key_no[0]
            search_value_data = df[df["Key_No"] == key_no]

            # Append the filtered data to the new dataframe
            filtered_df = pd.concat([filtered_df, search_value_data])

    # Display the resulting dataframe
    # filtered_df.to_excel("filtered_df.xlsx")
    # print(filtered_df)
    encode_df = model_prediction(doc_input)
    # encode_df = pd.read_excel("D:\doc_extraction_openai\embedding_code\output\encode_data.xlsx")   #.drop(['unnamed 0'],axis=1)
    # print(encode_df)

    search_values = filtered_df["Search_Value"].unique()

    # Filter rows in encode_df based on the presence of search values in Para column
    filtered_encode_df = encode_df[encode_df["Para"].str.contains('|'.join(search_values), case=False)]
    # type(filtered_encode_df)

    # filtered_encode_df
    filtered_encode_df.to_csv("csv_filtered_encode_df.csv", index=False)
        # upload_folder=run_Azure_conn.LOCAL_BLOB_PATH
        # temp_path = os.path.join(upload_folder,"synonyms_dic.xlsx")
        # filtered_df = pd.DataFrame()
        # encode_data = model_prediction(doc_input)
        # for i, search_value in enumerate(json_data["search_value"]):
        #     key_no = df[df["Search_Value"].str.lower() == search_value.lower()]["Key_No"].values

        #     # If key_no is found, filter the data based on that key_no
        #     if key_no.any():
        #         key_no = key_no[0]
        #         search_value_data = df[df["Key_No"] == key_no]

        #         # Append the filtered data to the new dataframe
        #         filtered_df = pd.concat([filtered_df, search_value_data])
        # search_values = filtered_df["Search_Value"].unique()
        
        # filtered_encode_df = encode_data[encode_data["Para"].str.contains('|'.join(search_values), case=False)]
    
    return filtered_encode_df