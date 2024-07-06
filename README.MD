# Resume Processing and Entity Extraction FastAPI App

This FastAPI application processes PDF resumes, extracts information using Named Entity Recognition (NER), and stores the extracted information in a Neo4j graph database.

## Setup

1. Create a virtual environment:
    
    python -m venv venv
    

2. Activate the virtual environment:
   
    source venv/bin/activate
    

3. Install the required packages:
    
    pip install -r requirements.txt
   

3. Download the spaCy language model:
    
    python -m spacy download en_core_web_sm
    

4. Ensure Neo4j is up and running at localhost:7687.

5. Start the FastAPI app:
   
    uvicorn main:app --reload
    

## Endpoints

1. **Root Endpoint**: 
    - URL: `/`
    - Method: `GET`
    - Description: Returns a welcome message.

2. **Upload Resume**:
    - URL: `/upload_resume/`
    - Method: `POST`
    - Description: Uploads a resume file.
    - Request: `UploadFile`

3. **Parse and Process Uploaded Resume**:
    - URL: `/parse_resume/`
    - Method: `POST`
    - Description: Parses and processes the uploaded resume.
    - Request: `file_name` (str)

4. **Extract Entities from Resume**:
    - URL: `/extract_entities/`
    - Method: `POST`
    - Description: Extracts entities from the uploaded resume.
    - Request: `UploadFile`

5. **Store Entities in Neo4j**:
    - URL: `/store_entities/`
    - Method: `POST`
    - Description: Stores extracted entities in Neo4j.
    - Request: `entities` (list)

6. **Download Data from Neo4j**:
    - URL: `/download_data`
    - Method: `GET`
    - Description: Downloads data from Neo4j in CSV format.

## License

This project is licensed under the MIT License.
