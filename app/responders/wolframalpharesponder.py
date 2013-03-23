import logging
import xml.etree.ElementTree as ET

from app.clients import wolframalphaclient
from app.types.messages import SimpleSmsResponse

class WolframAlphaResponder:
  def respond(self, request):
    answer = self.get_answer(request.query)
    if not answer: return None

    return SimpleSmsResponse(answer)

  
  def get_answer(self, query):
    response = wolframalphaclient.query(query)
    root = ET.fromstring(response)
    logging.info("The root of the tree is: " + root.tag)

    answer = self.get_answer_text(root)

    if not answer or len(answer) <= 160: return answer

    answer = answer.replace("congruent", " congr. ")
    answer = answer.replace("\n", " ")
    return answer[0:157] + "..."


  def get_answer_text(self, root):
    answer_next = False
    for child in root:
      if answer_next:
        return child[0][0].text

      if 'id' in child.attrib and child.attrib['id'] == 'Input':
        answer_next = True

    return None