import logging

n = 5000

def chunk(msg):
  return [msg[i:i+n] for i in range(0, len(msg), n)]

def log(msg):
  chunks = chunk(msg)
  logging.info("There are %d chunks" % len(chunks))

  for chunk in chunks:
    logging.debug(chunk.decode("utf-8", "ignore"))