import os, sys
import webapp2

import sys
sys.path.insert(0, 'tweepy.zip')

import tweepy

bgrpdict={
  'ABN':'AB-ve (negative)',
  'ABP':'AB+ve (positive)',
  'AN' :'A-ve (negative)',
  'AP' :'A+ve (positive)',
  'BN' :'B-ve (negative)',
  'BP' :'B+ve (positive)',
  'ON' :'O-ve (negative)',
  'OP' :'O+ve (positive)',
};

class MainPage(webapp2.RequestHandler):

  def posttweet(self, tweetmsg):
    # Redacted before posting on github as it's a secure passcode.
    consumer_key="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    consumer_secret="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    access_token="XXXXXXXXXXXXXXXXXXXXXXXXXX"
    access_token_secret="XXXXXXXXXXXXXXXXXXXXXXXXXX"
    try:
      auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
      auth.set_access_token(access_token, access_token_secret)
      api = tweepy.API(auth)
      api.update_status(tweetmsg)
      return 1
    except Exception:
      sys.stderr.write('Auth failed or no write permission on app')
      return 0

  def get(self):
    self.response.headers['Content-Type'] = 'text/plain'
    msg=self.request.get("message")
    bloodgrp=city=contactnum=contactinfo=''
    ret=1
    helpreq=0
    if msg:
      try:
        reslist=msg.split()
        #bloodgrp=reslist[0]
        #city=reslist[1]
        #contactnum=reslist[2]
        #contactinfo=reslist[3]
        bloodgrp=(reslist[0][:3]) if len(reslist[0]) > 4 else reslist[0]
        city=(reslist[1][:15]) if len(reslist[1]) > 15 else reslist[1]
        contactnum=(reslist[2][:15]) if len(reslist[2]) > 15 else reslist[2]
        contactinfo=(reslist[3][:25]) if len(reslist[3]) > 25 else reslist[3]
      except IndexError:
        pass
    if msg.lower() == 'help':
        helpreq=1
    if helpreq or bloodgrp=='' or \
          bloodgrp.upper() not in ['ABN','ABP','AN','AP','BN','BP','ON','OP'] \
          or city=='' or contactnum=='' \
          or contactinfo=='' :
      self.response.write( "Usage: #reqblood BLOODGROUP CITY CONTACTNUM CONTACTNAME.")
      self.response.write( " BLOODGROUP any of ABN/ABP/AN/AP/BN/BP/ON/OP\n")
      return
    else:
      tweetmsg="Reqd "+bgrpdict[bloodgrp.upper()]+" in #"+city+". Contact: "+contactnum+" "+contactinfo
      sys.stderr.write('tweetmsg ['+tweetmsg+']')
      ret=self.posttweet(tweetmsg)

    if ret and helpreq!=1:
      self.response.write( "Posted: "+tweetmsg+"\n")
    else:
      self.response.write( "Apologies! Tweet posting failed. Please try after sometime.\n")

app = webapp2.WSGIApplication([('/', MainPage),], debug=True)

