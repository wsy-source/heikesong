EXTRACTION_PROMPT = """
You are a professional reviewer in the field of Scientific research and medical applications of genomes, single-cell and spatial transcriptomes
I'll give you some documentation. You need to review this paper and extract the entity information I need
Note the correctness, clarity, importance, potential impact, and quality of the entity's information.
Note All extracted information are nouns and answer in Chinese

Required Entity Information: Species,Root Organ,Topic,Disease

The output follows the format:
Species:  **\n
Root Organ: **  \n
Organ: **\n
Topic: **\n  
Disease: **


Begin! 
document: {input_documents}    
conceptual entity : <answer question in chinese>
"""

REFINE_PROMPT = """
    "Your job is to extract conceptual entities\n"
    "We have provided concept entity up to a certain point: {existing_answer}\n"
    "We have the opportunity to refine the concept entity"
    "(only if needed) with some more context below.\n"
    "------------\n"
    "{input_documents}\n"
    "------------\n"
    "Given the new context, refine the original concept entity\n"
    "The output follows the format:\n
        Species: <such as dog>\n
        Root Organ: <such as blood>\n  
        Organ: <such as blood>\n  
        Topic: <such as immunology>\n    
        Disease: <Disease information presented in the article>"
    "If the context isn't useful, return the original concept entity. \n"
"""
