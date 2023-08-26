SUMMARY_PROMPT = """
You are a researcher in the field of Scientific research and medical applications of genomes, single-cell and spatial transcriptomes  who is good at summarizing papers using concise statements and Translate the final result into Chinese

user requirements: 
    1. The report contain should contain the following: 1.Base Information 2. Abstract 3. Background 4. Methods 5. Article Overview
    2. list all the authors' names 
  
output sample: 
     Base Information:
         Title: xxx
         Authors: xxx 
         Affiliation: xxx
         Keywords: xxx 
         URLs: https://doi.org/10.1038/s41588-020-0636-z
     Summary:
         a. The research background of this document:xxx
         b. Previous methods:xxx
         c. The research method proposed in this paper:xxx
         d. How the method performs in terms of tasks and performance:xxx
     Background:
         a. Themes and features:xxx
         b. Historical development:xxx
         c. Previous methods:xxx
         d. Deficiencies of previous studies:xxx
     Method:
         a. The theoretical basis of this study:xxx
         b. The technical route of this article (step by step):xxx
         c. Innovativeness, performance and effort of the method:xxx
         d. Research conclusion:xxx
     Overview of the full text: xxx
     
Begin!
Document: {input_documents}
Report: 
"""

# SUMMARY_PROMPT2 = """
# You are a researcher in the field of biology who is good at summarizing papers using concise statements
# Be sure to use chinese answers (proper nouns need to be marked in English), statements as concise and academic as possible, do not have too much repetitive information, numerical values using the original numbers, be sure to strictly follow the format, the corresponding content output to xxx, in accordance with \n line feed
#
# output requirements:
#     0. The output should contain three categories: Basic information, summary, and full-text summary
#     1. Mark the title of the paper (translate in chinese)
#     2. list all the authors' names (use English)
#     3. mark the first author's affiliation
#     4. mark the keywords of this article (use English)
#     5. link to the paper, Github code link (if available, fill in Github:None if not)
#     6. summarize according to the following four points and each point should be divided into abcd to explain .(proper nouns need to be marked in English)
#         - (1):What is the research background of this article?
#         - (2):What are the past methods? What are the problems with them? Is the approach well motivated?
#         - (3):What is the research methodology proposed in this paper?
#         - (4):On what task and what performance is achieved by the methods in this paper? Can the performance support their goals?
#     7. The full-text summary should be based on the document and a summary summary
#     8. If there is no language requirement, the default is to use Chinese to answer, and English should be used for nouns, such as author keywords and other information
# Follow the format of the output that follows:
# Base Information:
#     1. Title: xxx\n\n
#     2. Authors: xxx\n\n
#     3. Affiliation: xxx\n\n
#     4. Keywords: xxx\n\n
#     5. Urls: xxx or xxx , xxx \n\n
# Summary: \n\n
#     - (1):xxx;\n
#         a.xxx
#         b.xxx
#         c.xxx
#         b.xxx
#     - (2):xxx;\n
#         a.xxx
#         b.xxx
#         c.xxx
#         b.xxx
#     - (3):xxx;\n
#         a.xxx
#         b.xxx
#         c.xxx
#         b.xxx
#     - (4):xxx.
#         a.xxx
#         b.xxx
#         c.xxx
#         b.xxx\n
# Overview of the full text: xxx
# .
# This is my document:
# {input_documents}
# """
