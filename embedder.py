import os                                                                                                                                                                                     
import base64                                                                                                                                                                                 
from typing import List, Dict, Any, Tuple                                                                                                                                                     
from dotenv import load_dotenv                                                                                                                                                                
from pinecone import Pinecone                                                                                                                                                                 
from langchain_community.document_loaders import (                                                                                                                                            
    UnstructuredWordDocumentLoader,                                                                                                                                                           
    UnstructuredExcelLoader,                                                                                                                                                                  
    PyPDFLoader,                                                                                                                                                                              
    TextLoader,                                                                                                                                                                               
    CSVLoader                                                                                                                                                                                 
)                                                                                                                                                                                             
from langchain.text_splitter import RecursiveCharacterTextSplitter                                                                                                                            
from langchain_mistralai import MistralAIEmbeddings                                                                                                                                           
from langchain_pinecone import PineconeVectorStore                                                                                                                                            
from langchain.schema import Document                                                                                                                                                         
import fitz  # PyMuPDF for PDF image extraction                                                                                                                                               
from PIL import Image                                                                                                                                                                         
import io                                                                                                                                                                                     
from openai import OpenAI                                                                                                                                                                     
import pandas as pd                                                                                                                                                                           
                                                                                                                                                                                              
load_dotenv()                                                                                                                                                                                 
                                                                                                                                                                                              
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")                                                                                                                                                  
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")                                                                                                                                                
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")                                                                                                                                              
INDEX_NAME = "opto-fra"                                                                                                                                                                       
                                                                                                                                                                                              
def initialize_pinecone() -> Pinecone:                                                                                                                                                        
    pc = Pinecone(api_key=PINECONE_API_KEY)                                                                                                                                                   
    if INDEX_NAME not in pc.list_indexes().names():                                                                                                                                           
        print("Index not found, creating new index")                                                                                                                                          
        pc.create_index(                                                                                                                                                                      
            name=INDEX_NAME,                                                                                                                                                                  
            dimension=1024,                                                                                                                                                                   
            metric="cosine",                                                                                                                                                                  
            spec=ServerlessSpec(cloud="aws", region="us-east-1")                                                                                                                              
        )                                                                                                                                                                                     
    else:                                                                                                                                                                                     
        print(f"Index already exists")                                                                                                                                                        
    return pc                                                                                                                                                                                 
                                                                                                                                                                                              
def get_file_extension(file_path: str) -> str:                                                                                                                                                
    return os.path.splitext(file_path)[1].lower()                                                                                                                                             
                                                                                                                                                                                              
def encode_image_to_base64(image_bytes: bytes) -> str:                                                                                                                                        
    """Convert image bytes to base64 string for OpenAI API"""                                                                                                                                 
    return base64.b64encode(image_bytes).decode('utf-8')                                                                                                                                      
                                                                                                                                                                                              
def describe_image_with_openai(image_bytes: bytes, client: OpenAI) -> str:                                                                                                                    
    """Use OpenAI's vision model to describe an image"""                                                                                                                                      
    try:                                                                                                                                                                                      
        base64_image = encode_image_to_base64(image_bytes)                                                                                                                                    
                                                                                                                                                                                              
        response = client.chat.completions.create(                                                                                                                                            
            model="gpt-4o",  # or "gpt-4-vision-preview"                                                                                                                                      
            messages=[                                                                                                                                                                        
                {                                                                                                                                                                             
                    "role": "user",                                                                                                                                                           
                    "content": [                                                                                                                                                              
                        {                                                                                                                                                                     
                            "type": "text",                                                                                                                                                   
                            "text": "Please provide a detailed description of this image, focusing on key elements, text content if any, charts, diagrams, or any important visual information that would be useful for document search and retrieval."                                                                                                                                      
                        },                                                                                                                                                                    
                        {                                                                                                                                                                     
                            "type": "image_url",                                                                                                                                              
                            "image_url": {                                                                                                                                                    
                                "url": f"data:image/jpeg;base64,{base64_image}"                                                                                                               
                            }                                                                                                                                                                 
                        }                                                                                                                                                                     
                    ]                                                                                                                                                                         
                }                                                                                                                                                                             
            ],                                                                                                                                                                                
            max_tokens=500                                                                                                                                                                    
        )                                                                                                                                                                                     
        print(f"Image description response: {response.choices[0].message.content}")                                                                                                           
        return response.choices[0].message.content                                                                                                                                            
    except Exception as e:                                                                                                                                                                    
        print(f"Error describing image: {e}")                                                                                                                                                 
        return "Image description unavailable"                                                                                                                                                
                                                                                                                                                                                              
def extract_images_from_pdf(file_path: str) -> List[Tuple[bytes, int, Dict]]:                                                                                                                 
    """Extract images from PDF and return image data with page numbers"""                                                                                                                     
    images = []                                                                                                                                                                               
    try:                                                                                                                                                                                      
        pdf_document = fitz.open(file_path)                                                                                                                                                   
                                                                                                                                                                                              
        for page_num in range(len(pdf_document)):                                                                                                                                             
            page = pdf_document[page_num]                                                                                                                                                     
            image_list = page.get_images()                                                                                                                                                    
                                                                                                                                                                                              
            for img_index, img in enumerate(image_list):                                                                                                                                      
                # Get image data                                                                                                                                                              
                xref = img[0]                                                                                                                                                                 
                pix = fitz.Pixmap(pdf_document, xref)                                                                                                                                         
                                                                                                                                                                                              
                # Convert to PIL Image and then to bytes                                                                                                                                      
                if pix.n - pix.alpha < 4:  # GRAY or RGB                                                                                                                                      
                    img_data = pix.tobytes("png")                                                                                                                                             
                    images.append((                                                                                                                                                           
                        img_data,                                                                                                                                                             
                        page_num + 1,  # 1-indexed page number                                                                                                                                
                        {                                                                                                                                                                     
                            "image_index": img_index,                                                                                                                                         
                            "source": file_path,                                                                                                                                              
                            "page": page_num + 1,                                                                                                                                             
                            "type": "image"                                                                                                                                                   
                        }                                                                                                                                                                     
                    ))                                                                                                                                                                        
                pix = None  # Clean up                                                                                                                                                        
                                                                                                                                                                                              
        pdf_document.close()                                                                                                                                                                  
    except Exception as e:                                                                                                                                                                    
        print(f"Error extracting images from PDF: {e}")                                                                                                                                       
                                                                                                                                                                                              
    return images                                                                                                                                                                             
                                                                                                                                                                                              
def extract_images_from_docx(file_path: str) -> List[Tuple[bytes, str, Dict]]:                                                                                                                
    """Extract images from DOCX files"""                                                                                                                                                      
    images = []                                                                                                                                                                               
    try:                                                                                                                                                                                      
        from docx import Document as DocxDocument                                                                                                                                             
        import zipfile                                                                                                                                                                        
                                                                                                                                                                                              
        # Open docx as zip file to extract images                                                                                                                                             
        with zipfile.ZipFile(file_path, 'r') as docx_zip:                                                                                                                                     
            # Look for image files in the media folder                                                                                                                                        
            image_files = [f for f in docx_zip.namelist() if f.startswith('word/media/')]                                                                                                     
                                                                                                                                                                                              
            for idx, img_file in enumerate(image_files):                                                                                                                                      
                img_data = docx_zip.read(img_file)                                                                                                                                            
                images.append((                                                                                                                                                               
                    img_data,                                                                                                                                                                 
                    f"image_{idx}",                                                                                                                                                           
                    {                                                                                                                                                                         
                        "image_index": idx,                                                                                                                                                   
                        "source": file_path,                                                                                                                                                  
                        "image_file": img_file,                                                                                                                                               
                        "type": "image"                                                                                                                                                       
                    }                                                                                                                                                                         
                ))                                                                                                                                                                            
    except Exception as e:                                                                                                                                                                    
        print(f"Error extracting images from DOCX: {e}")                                                                                                                                      
                                                                                                                                                                                              
    return images                                                                                                                                                                             
                                                                                                                                                                                              
def load_document_with_images(file_path: str) -> Tuple[List[Document], List[Tuple[bytes, Any, Dict]]]:                                                                                        
    """Load document and extract images separately"""                                                                                                                                         
    ext = get_file_extension(file_path)                                                                                                                                                       
    documents = []                                                                                                                                                                            
    images = []                                                                                                                                                                               
                                                                                                                                                                                              
    # Load text content                                                                                                                                                                       
    if ext == ".pdf":                                                                                                                                                                         
        loader = PyPDFLoader(file_path)                                                                                                                                                       
        documents = loader.load()                                                                                                                                                             
        images = extract_images_from_pdf(file_path)                                                                                                                                           
    elif ext == ".docx":                                                                                                                                                                      
        loader = UnstructuredWordDocumentLoader(file_path)                                                                                                                                    
        documents = loader.load()                                                                                                                                                             
        images = extract_images_from_docx(file_path)                                                                                                                                          
    elif ext == ".xlsx":                                                                                                                                                                      
        loader = UnstructuredExcelLoader(file_path)                                                                                                                                           
        documents = loader.load()                                                                                                                                                             
        # Excel files might contain charts/images, but they're complex to extract                                                                                                             
        # For now, we'll focus on text content                                                                                                                                                
    elif ext == ".txt":                                                                                                                                                                       
        loader = TextLoader(file_path)                                                                                                                                                        
        documents = loader.load()                                                                                                                                                             
    elif ext == ".csv":                                                                                                                                                                       
        loader = CSVLoader(file_path)                                                                                                                                                         
        documents = loader.load()                                                                                                                                                             
    else:                                                                                                                                                                                     
        raise ValueError(f"Unsupported file format: {ext}")                                                                                                                                   
                                                                                                                                                                                              
    return documents, images                                                                                                                                                                  
                                                                                                                                                                                              
def create_image_documents(images: List[Tuple[bytes, Any, Dict]], openai_client: OpenAI) -> List[Document]:                                                                                   
    """Convert images to Document objects with descriptions"""                                                                                                                                
    image_documents = []                                                                                                                                                                      
                                                                                                                                                                                              
    for img_data, location, metadata in images:                                                                                                                                               
        try:                                                                                                                                                                                  
            description = describe_image_with_openai(img_data, openai_client)                                                                                                                 
                                                                                                                                                                                              
            # Create a document for the image description                                                                                                                                     
            image_doc = Document(                                                                                                                                                             
                page_content=f"[IMAGE DESCRIPTION] {description}",                                                                                                                            
                metadata={                                                                                                                                                                    
                    **metadata,                                                                                                                                                               
                    "content_type": "image_description",                                                                                                                                      
                    "location": str(location)                                                                                                                                                 
                }                                                                                                                                                                             
            )                                                                                                                                                                                 
            image_documents.append(image_doc)                                                                                                                                                 
            print(f"Processed image at location {location}")                                                                                                                                  
                                                                                                                                                                                              
        except Exception as e:                                                                                                                                                                
            print(f"Failed to process image at location {location}: {e}")                                                                                                                     
                                                                                                                                                                                              
    return image_documents                                                                                                                                                                    
                                                                                                                                                                                              
def process_document_with_images(file_path: str, openai_client: OpenAI) -> List[Document]:                                                                                                    
    """Process document including both text and image content"""                                                                                                                              
    # Load documents and extract images                                                                                                                                                       
    documents, images = load_document_with_images(file_path)                                                                                                                                  
                                                                                                                                                                                              
    # Split text documents                                                                                                                                                                    
    splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=250)                                                                                                             
    text_chunks = splitter.split_documents(documents)                                                                                                                                         
                                                                                                                                                                                              
    # Process images and create image documents                                                                                                                                               
    image_documents = create_image_documents(images, openai_client)                                                                                                                           
                                                                                                                                                                                              
    # Combine text chunks and image documents                                                                                                                                                 
    all_chunks = text_chunks + image_documents                                                                                                                                                
                                                                                                                                                                                              
    print(f"Created {len(text_chunks)} text chunks and {len(image_documents)} image descriptions")                                                                                            
    return all_chunks                                                                                                                                                                         
                                                                                                                                                                                              
def store_embeddings(index_name: str, chunks: List[Document], embeddings):                                                                                                                    
    """Store both text and image description embeddings"""                                                                                                                                    
    texts = [chunk.page_content for chunk in chunks]                                                                                                                                          
    metadatas = [chunk.metadata for chunk in chunks]                                                                                                                                          
                                                                                                                                                                                              
    PineconeVectorStore.from_texts(                                                                                                                                                           
        texts=texts,                                                                                                                                                                          
        embedding=embeddings,                                                                                                                                                                 
        metadatas=metadatas,                                                                                                                                                                  
        index_name=INDEX_NAME,                                                                                                                                                                
        namespace=index_name                                                                                                                                                                  
    )                                                                                                                                                                                         
    print(f"Stored {len(texts)} chunks (text + image descriptions) into index: {index_name}")                                                                                                 
                                                                                                                                                                                              
def process_and_embed_document(file_path: str, company_name: str) -> str:                                                                                                                                        
    """Orchestrate the entire process of processing and embedding a document"""                                                                                                               
    try:                                                                                                                                                                                      
        # Initialize services                                                                                                                                                                 
        initialize_pinecone()                                                                                                                                                                 
        openai_client = OpenAI(api_key=OPENAI_API_KEY)                                                                                                                                        
                                                                                                                                                                                              
        # Process document                                                                                                                                                                    
        print(f"Processing document: {file_path}")                                                                                                                                            
        chunks = process_document_with_images(file_path, openai_client)                                                                                                                       
                                                                                                                                                                                              
        # Initialize embeddings                                                                                                                                                               
        embeddings = MistralAIEmbeddings(                                                                                                                                                     
            model="mistral-embed",                                                                                                                                                            
            mistral_api_key=MISTRAL_API_KEY                                                                                                                                                   
        )                                                                                                                                                                                     
                                                                                                                                                                                              
        print("Finished creating embeddings model")                                                                                                                                           
        print(f"Total chunks to store: {len(chunks)}")                                                                                                                                        
                                                                                                                                                                                              
        # Store embeddings                                                                                                                                                                    
        store_embeddings(company_name, chunks, embeddings)                                                                                                                                    
        return f"Successfully processed and embedded document: {file_path}"                                                                                                                   
                                                                                                                                                                                              
    except Exception as e:                                                                                                                                                                    
        print(f"Error processing document {file_path}: {e}")                                                                                                                                  
        raise e