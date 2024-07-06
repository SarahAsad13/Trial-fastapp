from fastapi import FastAPI, File, UploadFile, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from py2neo import Graph
import pandas as pd
import spacy

# Initialize FastAPI app
app = FastAPI()

# Initialize Neo4j connection
uri = "bolt://localhost:7687"  
username = "neo4j"  # Update with your Neo4j username
password = "hello123"  # Update with your Neo4j password
graph = Graph(uri, auth=(username, password))

# Load NLP models and components
nlp = spacy.load("en_core_web_sm")

# Allowing CORS Headers
origins = ["http://localhost:3000", "*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Root endpoint
@app.get('/')
async def root():
    return {'message': 'This is the root of the app'}

# Endpoint to upload a resume
@app.post("/upload_resume/")
async def upload_resume(file: UploadFile = File(...)):
    try:
        # Save uploaded resume locally
        filename = file.filename
        with open(filename, "wb") as f:
            f.write(file.file.read())
        
        return {"message": "Resume uploaded successfully.", "filename": filename}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to parse and process uploaded resume
@app.post("/parse_resume/")
async def parse_resume(file_name: str):
    try:
        # Process the resume (example: extract entities using NER)
        entities = extract_entities_from_resume(file_name)
        
        # Store entities in Neo4j database
        store_entities_in_neo4j(entities)
        
        return {"message": "Resume processed and entities stored successfully."}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to extract entities from resume
@app.post("/extract_entities/")
async def extract_entities(file: UploadFile = File(...)):
    try:
        # Save uploaded resume locally
        filename = file.filename
        with open(filename, "wb") as f:
            f.write(file.file.read())
        
        # Process the resume to extract entities
        entities = extract_entities_from_resume(filename)
        
        return {"entities": entities}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to store entities in Neo4j database
@app.post("/store_entities/")
async def store_entities(entities: list):
    try:
        # Store entities in Neo4j
        store_entities_in_neo4j(entities)
        
        return {"message": "Entities stored in Neo4j successfully."}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to download data from Neo4j
@app.get("/download_data")
async def download_data():
    try:
        # Example query to retrieve data from Neo4j
        query = """
        MATCH (n:Node)-[r:RELATIONSHIP]->(m:OtherNode)
        RETURN n, r, m
        """
        result = graph.run(query).data()

        # Convert Neo4j result to pandas DataFrame
        df = pd.DataFrame(result)

        # Prepare data for download (e.g., to CSV)
        csv_data = df.to_csv(index=False)

        # Prepare HTTP response with CSV data for download
        response = Response(content=csv_data)
        response.headers["Content-Disposition"] = 'attachment; filename="neo4j_data.csv"'
        response.headers["Content-Type"] = "text/csv"
        
        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Function to extract entities from resume using NER
def extract_entities_from_resume(filename):
    # Example: Use spaCy NER to extract entities
    doc = nlp(open(filename).read())
    entities = [ent.text for ent in doc.ents]
    return entities

# Function to store entities in Neo4j database
def store_entities_in_neo4j(entities):
    # Example: Create Cypher query and execute it with Py2neo
    for entity in entities:
        query = f"MERGE (e:Entity {{name: '{entity}'}})"
        graph.run(query)

# Run the FastAPI app with uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
