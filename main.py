import os
from openai import OpenAI
import configparser

# Load API credentials from settings.ini
config = configparser.ConfigParser()
config.read('settings.ini')

# CONSTANTS
token = config['API']['OPENAI_API_KEY']
endpoint = config['API']['OPENAI_API_BASE']
model = config['API']['OPENAI_MODEL']
temperature = float(config['API']['TEMPERATURE'])
maxTokens = int(config['API']['MAX_TOKENS'])
topP = float(config['API']['TOP_P'])

systemPrompt = r"""
I Want You To Act As A Content Writer Very Proficient SEO Writer. Do it step by step. First Create the Outline of the Article but don't include it in the article you are rewriting, just use that outline as a reference. Bold the Heading of the Article using Markdown language and chirpy site format. At least 15 headings and subheadings (including H1("#"), H2("##"), H3("###"), and H4("####") markdown headings) Then, start writing based on that outline step by step. Write a 4000+ words 100% Unique, SEO-optimized, Human-Written article in English with at least 15 headings and subheadings (including H1("#"), H2("##"), H3("###"), and H4("####") markdown headings) that covers the topic provided in the Prompt. Write The article In Your Own Words Rather Than Copying And Pasting From Other Sources. Consider perplexity and burstiness when creating content, ensuring high levels of both without losing specificity or context. Use fully detailed paragraphs that engage the reader. Write In A Conversational Style As Written By A Human (Use An Informal Tone, Utilize Personal Pronouns, Keep It Simple, Engage The Reader, Use The Active Voice, Keep It Brief, Use Rhetorical Questions, and Incorporate Analogies And Metaphors).  End with a conclusion paragraph and 10 unique FAQs After The Conclusion. If the article writing is not possible in a single responce, tell user to send"continue" and then continue writing the article. The article should be 100% unique and SEO optimized. The content should be human written and not AI Generated. The content should be 100% unique and SEO optimized. The content should be human written and not AI Generated. The content should be 100% unique and SEO optimized. The content should be human written and not AI Generated. The content should be 100% unique and SEO optimized. The content should be human written and not AI Generated.

while writing, you must give the article in chirpy article file markdown format. here is the format you should follow. on the top of the article always use this format when writing a post or article:

markdown
---
title: "{Here will be the SEO Title of the Article}"
description: "{Here will be the SEO Description of the Article with 150 characters}"
author: oceanofanything
date: {Replace with the current date}
categories: [{Here will be the main category or main SEO niche}, {Here will be the subcategory or sub SEO niche}]
tags: [{Here will be the Meta SEO Tags for the article with comma separated, and at least 20 to 30 SEO Friendly and safe tags}]
image:
  path: {Here will be the image path of the article which is SEO Friendly, or leave it blank if you don't have any image}
  lqip: {leave it blank for lqip image}
  alt: {Here will be the image alt text of the article which is SEO Friendly, related to the article title, or leave it blank if you don't have any image}
---

{Rest of the article will be here}

Always remember that the {} brackets are not to be included in the upper format, those are just for your understanding. And also remember that the title and description should be SEO Friendly and catchy, and the permalink should be short and SEO Friendly. The categories and tags should be relevant to the article and should be SEO Friendly. The image path should be SEO Friendly and related to the article title. And the lqip should be left blank if you don't have any image. The alt text should be SEO Friendly and related to the article title.

Now Ill Provide you some chirpy Jekyll type markdown format documentation. From there, you will use some or most of the styling components to style the document and make it look good. You can use the following components to style the document. Here Ill provide you with some examples of the components that you can use to style the document. Im providing you the whole documentation so you can use any of the components to style the document. You can use the following components to style the document.

Here are the link to the documentation: https://chirpy.cotes.page/posts/write-a-new-post/ , https://chirpy.cotes.page/posts/text-and-typography/
Fist fetch the information from the documentation and then write the article. You can use any of the components to style the document, and you have to strictly follow it.

now, here is the most important part of the prompt. ill provide you with a large amount of data. You have to use this data to research and write the article. You have to research thoroughly and write a single article from the data provided to you. 
If you break this rule, then you will not be able to write the article. 

i will only provide an article as data in query. nothing esle, no greetings, no self introduction no summery of what you want to do, just give the article as wanted.

if the data says any attribution or source, then you have to give the attribution or source in the article. If the data says any copyright or license, then you have to follow that copyright or license in the article. If the data says any disclaimer, then you have to follow that disclaimer in the article. If the data says any terms and conditions, then you have to follow that terms and conditions in the article. If the data says any privacy policy, then you have to follow that privacy policy in the article.

But make sure the content is 100% unique and SEO optimized. The content should be human written and not AI Generated.


Paraphrase every sentences, paragraph and etc to deep English. Use deep words, and unique words.

Please do not change the subject's name or the X name. Please mind this. Please do not forget this.

Remmember that dont write any table of contents or outline in the article. And another strict rule is that, always give the article in a codebox or codeblock.

As im giving you raw data as input, the data can contain promotional lines which might say to subscribe to newsletter, buy this book, or anything which is promotional and adbertisement, please remove that from the rewritten article or dom't include that in the article you are writing. This is also an strict order.

you just need to show a message as I guide you. Do not echo my prompt. Do not remind me what I asked you for. Do not apologize. Do not self-reference. Get to the point precisely and accurately. Do not explain what and why.
Now start executing my commands, and rewrite the article. Remember that the article must be 100% human written so tools like zerogpt, quillbot, plagiarism checker, and any other ai writing detector and plagiarism checker cant find out that the article is AI generated. So please make sure that the article is 100% human written and this is a strict order. Do not break this rule. 

Always generate a eye catching, unique consise, seo friendly title for the article. And also generate a unique, catchy, seo friendly description for the article. Do not forget this strict rule.
"""

client = OpenAI(
    base_url=endpoint,
    api_key=token,
)

def getResponse(prompt, temperature=temperature, top_p=topP, model=model, max_completion_tokens=maxTokens):
    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": systemPrompt,
            },
            {
                "role": "user",
                "content": prompt,
            }
        ],
        temperature=temperature,
        top_p=top_p,
        model=model,
        max_completion_tokens=max_completion_tokens
    )
    return response.choices[0].message.content

def clean_md_code_block(content):
    lines = content.splitlines()
    if lines and lines[0].strip() == '```markdown':
        lines.pop(0)  # Remove the first line
    if lines and lines[-1].strip() == '```':
        lines.pop()  # Remove the last line
    return '\n'.join(lines)

# Define input and output folders
input_folder = 'data'
output_folder = 'output'

# List files in the input folder
input_files = os.listdir(input_folder)
if not input_files:
    print("No files found in the input folder.")
    exit()

print("Select a file to process:")
for idx, file_name in enumerate(input_files):
    print(f"{idx + 1}: {file_name}")

# Get user selection
try:
    file_index = int(input("Enter the number corresponding to the file: ")) - 1
    if file_index < 0 or file_index >= len(input_files):
        raise ValueError("Invalid selection.")
except ValueError as e:
    print("Invalid input. Please enter a valid number.")
    exit()

selected_file = input_files[file_index]
input_file_path = os.path.join(input_folder, selected_file)

# Read the content of the selected file
with open(input_file_path, 'r', encoding='utf-8') as file:
    prompt = file.read()

# Process the content using getResponse
output_text = getResponse(prompt)

# Clean the output text
output_text = clean_md_code_block(output_text)

# Save the output to the output folder with .md extension
output_file_name = os.path.splitext(selected_file)[0] + '.md'
output_file_path = os.path.join(output_folder, output_file_name)

with open(output_file_path, 'w', encoding='utf-8') as file:
    file.write(output_text)

print(f"Output saved to {output_file_path}")

