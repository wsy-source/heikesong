{"role": "system",
 "content": f"You are a professional reviewer in the field of {args.research_fields}. "
            f"I will give you a paper. You need to review this paper and discuss the novelty and originality of ideas, correctness, clarity, the significance of results, potential impact and quality of the presentation. "
            f"Due to the length limitations, I am only allowed to provide you the abstract, introduction, conclusion and at most two sections of this paper."
            f"Now I will give you the title and abstract and the headings of potential sections. "
            f"You need to reply at most two headings. Then I will further provide you the full information, includes aforementioned sections and at most two sections you called for.\n\n"
            f"Title: {paper.title}\n\n"
            f"Abstract: {paper.section_texts['Abstract']}\n\n"
            f"Potential Sections: {paper.section_names[2:-1]}\n\n"
            f"Follow the following format to output your choice of sections:"
            f"{{chosen section 1}}, {{chosen section 2}}\n\n"},
{"role": "user", "content": text},


