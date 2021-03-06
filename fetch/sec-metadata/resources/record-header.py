import os
import uuid
import hashlib
import time

resourcePath = os.getcwd() + "/fetch/sec-metadata/resources/"

def main(request, response):

  ## Get the query parameter (key) from URL ##
  ## Tests will record POST requests (CSP Report) and GET (rest) ##
  if request.GET:
    key = request.GET['file']
  elif request.POST:
    key = request.POST['file']

  ## Convert the key from String to UUID valid String ##
  testId = hashlib.md5(key).hexdigest()

  ## Handle the header retrieval request ##
  if 'retrieve' in request.GET:
    response.writer.write_status(200)
    response.writer.end_headers()
    header_value = request.server.stash.take(testId)
    if header_value != None:
      response.writer.write(header_value)

    response.close_connection = True

  ## Record incoming Sec-Metadata header value
  else:
    ## Return empty string as a default value ##
    header = request.headers.get("Sec-Metadata", "")
    try:
      request.server.stash.put(testId, header)
    except KeyError:
      ## The header is already recorded
      pass

    ## Prevent the browser from caching returned responses and allow CORS ##
    response.headers.set("Access-Control-Allow-Origin", "*")
    response.headers.set("Cache-Control", "no-cache, no-store, must-revalidate")
    response.headers.set("Pragma", "no-cache")
    response.headers.set("Expires", "0")

    ## Add a valid ServiceWorker Content-Type ##
    if key.startswith("serviceworker"):
      response.headers.set("Content-Type", "application/javascript")

    ## Return a valid .vtt content for the <track> tag ##
    if key.startswith("track"):
      return "WEBVTT"

    ## Return a valid SharedWorker ##
    if key.startswith("sharedworker"):
      response.headers.set("Content-Type", "application/javascript")
      file = open(resourcePath + "sharedWorker.js", "r")
      shared_worker = file.read()
      file.close()
      return shared_worker

    ## Return a valid font content and Content-Type ##
    if key.startswith("font"):
      file = open("fonts/Ahem.ttf", "r")
      font = file.read()
      file.close()
      return font

    ## Return a valid audio content and Content-Type ##
    if key.startswith("audio"):
      response.headers.set("Content-Type", "audio/mpeg")
      file = open("media/sound_5.mp3", "r")
      audio = file.read()
      file.close()
      return audio

    ## Return a valid video content and Content-Type ##
    if key.startswith("video"):
      response.headers.set("Content-Type", "video/mp4")
      file = open("media/A4.mp4", "r")
      video = file.read()
      file.close()
      return video

    ## Return a valid style content and Content-Type ##
    if key.startswith("style") or key.startswith("embed") or key.startswith("object"):
      response.headers.set("Content-Type", "text/html")
      return "<html>EMBED!</html>"

    ## Return a valid image content and Content-Type for redirect requests ##
    if key.startswith("redirect"):
      response.headers.set("Content-Type", "image/jpeg")
      file = open("media/1x1-green.png", "r")
      image = file.read()
      file.close()
      return image

    ## Return a valid dedicated worker
    if key.startswith("worker"):
      response.headers.set("Content-Type", "application/javascript")
      return "self.postMessage('loaded');"

    ## Return a valid XSLT
    if key.startswith("xslt"):
      response.headers.set("Content-Type", "text/xsl")
      return """<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
  <xsl:template match="@*|node()">
    <xsl:copy>
      <xsl:apply-templates select="@*|node()"/>
    </xsl:copy>
  </xsl:template>
</xsl:stylesheet>"""

