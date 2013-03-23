import webapp2
import logging
import string
import app.config.config

from google.appengine.ext import db

class StorageRequestHandler(webapp2.RequestHandler):
  def get(self, *args):
    num = args[0]
    path = args[1]
    logging.info("Number requested is: " + num)
    logging.info("Path requested is: " + path)

    if path == "notes":
      self.renderNotesTable(num)
    elif path == "recordings":
      self.renderRecordingsTable(num)


  def renderRecordingsTable(self, author):
    recordings = db.GqlQuery("SELECT * "
                             "FROM Recording "
                             "WHERE author = '" + author + "' "
                             "ORDER BY date DESC")

    rowcount = 1
    recordings_content = ""
    for recording in recordings:
      if (rowcount % 2 == 0):
        recordings_content = recordings_content + '<tr class="even">'
      else:
        recordings_content = recordings_content + "<tr>"

      recordings_content = recordings_content + "<td>" + recording.date.strftime("%I:%M:%S%p %m/%d/%Y") + "</td>"
      recordings_content = recordings_content + "<td>" + recording.name + "</td>"
      recordings_content = recordings_content + '<td><a href="' + recording.url + '.mp3">' + recording.name + '</a></td>'
      recordings_content = recordings_content + "</tr>"
      rowcount+=1


    html = string.Template("""
      <html>
        <head>
          <title>$number's recordings</title>
          <link rel="stylesheet" type="text/css" href="../../www/css/notes.css">
        </head>
        <body>
          <div class="pageheader"> $number's Wise Sayings</div>
          <table cellspacing='0'>
            <thead>
              <tr>
                <th>Date</th>
                <th>Name</th>
                <th>Resource</th>
              </tr>
            </thead>
            <tbody>
              $notes
            </tbody>
          </table>
        </body>
      </html>""")
    self.response.out.write(html.substitute(number=author, notes=recordings_content))  


  def renderNotesTable(self, author):
    notes = db.GqlQuery("SELECT * "
                        "FROM Note "
                        "WHERE author = '" + author + "' "
                        "ORDER BY date DESC")

    rowcount = 1
    notes_content = ""
    for note in notes:
      if (rowcount % 2 == 0):
        notes_content = notes_content + '<tr class="even">'
      else:
        notes_content = notes_content + "<tr>"

      notes_content = notes_content + "<td>" + note.date.strftime("%I:%M:%S%p %m/%d/%Y") + "</td><td>" + note.content + "</td>"
      notes_content = notes_content + "</tr>"
      rowcount+=1


    html = string.Template("""
      <html>
        <head>
          <title>$number's notes</title>
          <link rel="stylesheet" type="text/css" href="../../www/css/notes.css">
        </head>
        <body>
          <div class="pageheader"> $number's Brilliant Ideas</div>
          <table cellspacing='0'>
            <thead>
              <tr>
                <th>Date</th>
                <th>Note</th>
              </tr>
            </thead>
            <tbody>
              $notes
            </tbody>
          </table>
        </body>
      </html>""")
    self.response.out.write(html.substitute(number=author, notes=notes_content))    

  def post(self):
    self.get()
