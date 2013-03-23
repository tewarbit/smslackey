import re
import logging

TRANSLATE_RULES_FIRST = [
  ('with a chance of a', 'chance'),
  (' with a windchill as low as ', ', wchill '),
  ("thunderstorm", "t-storm"),
  (" and a chance of ", "/"),
  (" in the morning", ""),
  ("High of ", "H "),
  ("Low of", "L"),
  ("with", "w"),
  (" in the evening", ""),
  (" and ", "/"),
  ("Partly", "Part"),
  ("Mostly", "Most")
]

TRANSLATE_RULES_SECOND = [
  ("snow showers", "s-showers"),
  (", then", ","),
  ("overcast", "ocast")
]

def render(content):
  logging.info("Rendering weather response: " + content)
  
  content = apply_translation(content, TRANSLATE_RULES_FIRST)

  # is it short enough?
  if len(content) <= 160: return content

  # need to trim more. we do two passes because the second pass makes it
  # more unreadable - so we avoid it if possible
  content = apply_translation(content, TRANSLATE_RULES_SECOND)

  # is it short enough now?
  if len(content) <= 160: return content
  
  # nothing else to trim out, just crop it
  return content[0:157] + "..."


def apply_translation(content, rules):
  for rule in rules:
    content = content.replace(rule[0], rule[1])

  return content  