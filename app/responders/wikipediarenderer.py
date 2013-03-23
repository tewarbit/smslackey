import re
import logging

def render(content):
  content = re.sub(r'\([^)]*\)', '', content).strip() #remove everything between parens
  content = re.sub(' +', ' ', content) #remove double spaces

  # if its short enough, we can just return
  if len(content) <= 160: return content

  
  # otherwise, we have to trim it down
  sentences = content.split(".")
  if (len(sentences) == 1): return content[0:157] + "..."

  content = sentences[0]
  if (len(content) > 160): return content[0:157] + "..."

  content_buffer = content
  i = 1
  while not content_buffer > 160:
    content_buffer += sentences[i]
    i += 1
    if not len(content_buffer > 160):
      content = content_buffer

  return content
