import pymupdf
import argparse
import pymupdf4llm
import pathlib
import os

def main():
    parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser(
        description='This Module extracts all the text from a documents. By Fabian Wieland.')
    parser.add_argument('filename')
    parser.add_argument("-p", "--page", help='Select a specific page to extract')
    parser.add_argument("-m",'--markdown', action='store_true', help='Retrieve your document content in Markdown')
    parser.add_argument("-s",'--save', action='store_true', help='Saves markdownfile (created with -m) utf-8 encoded as output.md')
   
    args = parser.parse_args()

    if os.path.isfile(args.filename):
        print(extract_content(args.filename, args))
    elif os.path.isdir(args.filename):
        print(extract_multi_file(args.filename,args))
    else:
        print("Error: No valid file or folder provided. Please provide a valid file or folder")

  

def extract_content(filename,options):
    doc = pymupdf.open(filename)  
    
    text=""
    if options.page:
        try:
         return doc.get_page_text(options.page)
        except:
         print("Error: {} is not a page in the provided document".format(options.page)) 
    elif (options.markdown):
        md_text = pymupdf4llm.to_markdown(filename)
        if(options.save):
            # Write the text to some file in UTF8-encoding
            pathlib.Path("output.md").write_bytes(md_text.encode())
        return md_text
    else:
        for page in doc:
            text+=page.get_text()
        return text
        
def extract_multi_file(filename,options):
            files = [f for f in os.listdir(filename) if os.path.isfile(os.path.join(filename,f))]
            text=''
            print(os.listdir(filename))
            for f in files:
                print(f)
                doc = pymupdf.open(os.path.join(filename,f))  
                for page in doc:
                        text+=page.get_text()
            return text

if __name__ == "__main__":
    main()
