import time
####################################################################################################

VIDEO_PREFIX = "/video/drnu"
MUSIC_PREFIX = "/music/drnu"

APIURL = "http://www.dr.dk/NU/api/%s"
RADIO_NOWNEXT_URL = "http://www.dr.dk/tjenester/LiveNetRadio/datafeed/programInfo.drxml?channelId=%s"

NAME  = "DR NU"
ART   = 'art-default.jpg'
ICON  = 'DR_icon-default.png'
ICON_DR1 = "DR1_icon-default.png"
ICON_DR2 = "DR2_icon-default.png"
ICON_DRK = "DRK_icon-default.png"
ICON_DRR = "DR_RAMASJANG_icon-default.png"
ICON_DRU = "DR_UPDATE_icon-default.png"

EPG_TV = { "DR1":"http://www.dr.dk/Tjenester/epglive/epg.DR1.drxml",
		"DR2": "http://www.dr.dk/Tjenester/epglive/epg.DR2.drxml",
		"DRU": "http://www.dr.dk/Tjenester/epglive/epg.DRUpdate.drxml",
		"RAM": "http://www.dr.dk/Tjenester/epglive/epg.DRRamasjang.drxml",
		"DRK": "http://www.dr.dk/Tjenester/epglive/epg.DRK.drxml"
		}

HTTP.CacheTime = 3600

####################################################################################################

def Start():
	Plugin.AddPrefixHandler(VIDEO_PREFIX, VideoMainMenu, NAME, ICON, ART)
	Plugin.AddPrefixHandler(MUSIC_PREFIX, VideoMainMenu, NAME, ICON, ART)
	Plugin.AddViewGroup("InfoList", viewMode="InfoList", mediaType="items")
	Plugin.AddViewGroup("List", viewMode="List", mediaType="items")
	MediaContainer.art = R(ART)
	MediaContainer.title1 = NAME
	DirectoryItem.thumb = R(ICON)

def VideoMainMenu():
	dir = MediaContainer(viewGroup="List")

	dir.Append(Function(DirectoryItem(ProgramSerierMenu,"Programmer",subtitle="Alle Programserier", summary="",thumb=R(ICON),art=R(ART)),id=None,title="Programmer"))
	dir.Append(Function(DirectoryItem(NewestMenu,"Nyeste",subtitle="De nyeste videoer", summary="",thumb=R(ICON),art=R(ART)),id=None, title="Nyeste"))
	dir.Append(Function(DirectoryItem(SpotMenu,"Spot",subtitle="Spot light", summary="",thumb=R(ICON),art=R(ART)),id=None, title="Spot"))
	dir.Append(Function(DirectoryItem(MostViewedMenu,"Mest Sete",subtitle="Mest Sete", summary="",thumb=R(ICON),art=R(ART)),id=None, title="Mest Sete"))
	dir.Append(Function(DirectoryItem(LiveTVMenu, "Live TV", subtitle="Live TV", summary="", thumb=R(ICON), art=R(ART))))
	dir.Append(Function(DirectoryItem(LiveRadioMenu, "Live Radio", subtitle="Live Radio", summary="", thumb=R(ICON), art=R(ART))))

	return dir

def ProgramSerierMenu(sender,id,title):
	dir=MediaContainer(title1="DR NU", title2=title)
	
	JSONObject=JSON.ObjectFromURL(APIURL % "programseries.json")
	for program in JSONObject:
		slug=program["slug"]
		title=program["title"]
		if program["videoCount"] > 1:
			title = title + " (" + str(program["videoCount"]) + " afs.)"
		subtitle=", ".join(program["labels"])
		
		summary=program["description"]
		thumb=APIURL % "programseries/" + slug + "/images/600x600.jpg"
                Log("thumb=" + thumb)
		dir.Append(Function(DirectoryItem(ProgramMenu,title=title,subtitle=subtitle,thumb=thumb,summary=summary),id=slug, title=title))
	return dir


def NewestMenu(sender,id, title):
        return CreateVideoItem(sender, id=id, title=title, items=JSON.ObjectFromURL(APIURL % "videos/newest.json"))

def MostViewedMenu(sender,id, title):
        return CreateVideoItem(sender, id=id, title=title, items=JSON.ObjectFromURL(APIURL % "videos/mostviewed.json"))

def SpotMenu(sender,id, title):
        return CreateVideoItem(sender, id=id, title=title, items=JSON.ObjectFromURL(APIURL % "videos/spot.json"))

def ProgramMenu(sender,id, title):
	return CreateVideoItem(sender, id=id, title=title, items=JSON.ObjectFromURL(APIURL % "programseries/" + id + "/videos"))

def LiveTVMenu(sender):
	drRTMP = "rtmp://rtmplive.dr.dk/live"
	dir = MediaContainer(title1="DR NU - Live TV", title2="Live TV")	
	dir.Append(RTMPVideoItem(drRTMP, clip="livedr01astream3", width=830, height=467, live=True, title="DR1", summary=getTVLiveMetadata("DR1"), thumb=R(ICON_DR1) ) )
	dir.Append(RTMPVideoItem(drRTMP, clip="livedr02astream3", width=830, height=467, live=True, title="DR2", summary=getTVLiveMetadata("DR2"), thumb=R(ICON_DR2) ) )
	dir.Append(RTMPVideoItem(drRTMP, clip="livedr03astream3", width=830, height=467, live=True, title="DR Update", summary=getTVLiveMetadata("DRU"), thumb=R(ICON_DRU) ) )
	dir.Append(RTMPVideoItem(drRTMP, clip="livedr04astream3", width=830, height=467, live=True, title="DR K", summary=getTVLiveMetadata("DRK"), thumb=R(ICON_DRK) ) )
	dir.Append(RTMPVideoItem(drRTMP, clip="livedr05astream3", width=830, height=467, live=True, title="DR Ramsjang", summary=getTVLiveMetadata("RAM"), thumb=R(ICON_DRR) ) )
	return dir


def LiveRadioMenu(sender):
	drRTMP = "rtmp://live.gss.dr.dk/live/"
	dir=MediaContainer(title1="DR NU - Live Radio", title2="Live Radio")
	dir.Append(RTMPVideoItem(drRTMP, clip="Channel3_HQ", width=0, height=0, live=True, title="P1", summary=getRadioMetadata('P1'), thumb=R(ICON)))
	dir.Append(RTMPVideoItem(drRTMP, clip="Channel4_HQ", width=0, height=0, live=True, title="P2", summary=getRadioMetadata('P2'), thumb=R(ICON)))
	dir.Append(RTMPVideoItem(drRTMP, clip="Channel15_HQ", width=0, height=0, live=True, title="P3", summary=getRadioMetadata('P3'), thumb=R(ICON)))
	dir.Append(Function(DirectoryItem(LiveRadioP4Menu,"P4",subtitle="P4", summary="",thumb=R(ICON),art=R(ART))))
	dir.Append(RTMPVideoItem(drRTMP, clip="Channel25_HQ", width=0, height=0, live=True, title="DR P5", summary=getRadioMetadata('P5'), thumb=R(ICON)))
	dir.Append(RTMPVideoItem(drRTMP, clip="Channel29_HQ", width=0, height=0, live=True, title="DR P6 Beat", summary=getRadioMetadata('P6'), thumb=R(ICON)))
	dir.Append(RTMPVideoItem(drRTMP, clip="Channel21_HQ", width=0, height=0, live=True, title="DR P7 Mix", summary=getRadioMetadata('P7'), thumb=R(ICON)))
	dir.Append(RTMPVideoItem(drRTMP, clip="Channel24_HQ", width=0, height=0, live=True, title="DR Ramasjang Radio", summary=getRadioMetadata('RAM'), thumb=R(ICON)))
	dir.Append(RTMPVideoItem(drRTMP, clip="Channel26_HQ", width=0, height=0, live=True, title="DR R&B", summary=getRadioMetadata('ROB'), thumb=R(ICON)))
	dir.Append(RTMPVideoItem(drRTMP, clip="Channel18_HQ", width=0, height=0, live=True, title="DR Boogieradio", summary=getRadioMetadata('SK1'), thumb=R(ICON)))
	dir.Append(RTMPVideoItem(drRTMP, clip="Channel27_HQ", width=0, height=0, live=True, title="DR Rock", summary=getRadioMetadata('ROC'), thumb=R(ICON)))
	dir.Append(RTMPVideoItem(drRTMP, clip="Channel10_HQ", width=0, height=0, live=True, title="DR Dansktop", summary=getRadioMetadata('DAN'), thumb=R(ICON)))
	dir.Append(RTMPVideoItem(drRTMP, clip="Channel19_HQ", width=0, height=0, live=True, title="DR Jazz", summary=getRadioMetadata('JAZ'), thumb=R(ICON)))
	dir.Append(RTMPVideoItem(drRTMP, clip="Channel23_HQ", width=0, height=0, live=True, title="DR Klassisk", summary=getRadioMetadata('DAB'), thumb=R(ICON)))
	dir.Append(RTMPVideoItem(drRTMP, clip="Channel2_HQ", width=0, height=0, live=True, title="DR Nyheder", summary=getRadioMetadata('NEWS'), thumb=R(ICON)))	
	return dir

def LiveRadioP4Menu(sender):
	drRTMP = "rtmp://live.gss.dr.dk/live/"
	dir=MediaContainer(title1="DR NU - P4", title2="P4")
	dir.Append(RTMPVideoItem(drRTMP, clip="Channel18_HQ", width=0, height=0, live=True, title="P4 København", summary='', thumb=R(ICON)))	
	dir.Append(RTMPVideoItem(drRTMP, clip="Channel11_HQ", width=0, height=0, live=True, title="P4 Sjælland", summary='', thumb=R(ICON)))
	dir.Append(RTMPVideoItem(drRTMP, clip="Channel14_HQ", width=0, height=0, live=True, title="P4 Østjylland", summary='', thumb=R(ICON)))
	dir.Append(RTMPVideoItem(drRTMP, clip="Channel12_HQ", width=0, height=0, live=True, title="P4 Syd", summary='', thumb=R(ICON)))
	dir.Append(RTMPVideoItem(drRTMP, clip="Channel17_HQ", width=0, height=0, live=True, title="P4 Fyn", summary='', thumb=R(ICON)))
	dir.Append(RTMPVideoItem(drRTMP, clip="Channel10_HQ", width=0, height=0, live=True, title="P4 Nordjylland", summary='', thumb=R(ICON)))
	dir.Append(RTMPVideoItem(drRTMP, clip="Channel9HQ", width=0, height=0, live=True, title="P4 Midt & Vest", summary='', thumb=R(ICON)))
	dir.Append(RTMPVideoItem(drRTMP, clip="Channel13_HQ", width=0, height=0, live=True, title="P4 Trekanten", summary='', thumb=R(ICON)))
	dir.Append(RTMPVideoItem(drRTMP, clip="Channel6_HQ", width=0, height=0, live=True, title="P4 Bornholm", summary='', thumb=R(ICON)))
	dir.Append(RTMPVideoItem(drRTMP, clip="Channel15_HQ", width=0, height=0, live=True, title="P4 Esbjerg", summary='', thumb=R(ICON)))
	dir.Append(RTMPVideoItem(drRTMP, clip="Channel11_HQ", width=0, height=0, live=True, title="P4 NordvestSjælland", summary='', thumb=R(ICON)))
	return dir	

def CreateVideoItem(sender,id, title, items):
	dir=MediaContainer(title1="DR NU", title2=title)
	for item in items:
		key=APIURL % "videos/" + str(item["id"])
		thumb=APIURL % "videos/" + str(item["id"]) + "/images/600x600.jpg"
		if 'imagePath' in item:
			art="http://dr.dk/nu" + item["imagePath"]
		elif 'programSerieSlug' in item:
			art="http://dr.dk/nu/api/programseries/" + item['programSerieSlug'] + "/images/1024x768.jpg"
		else:
			art=thumb

		if 'spotTitle' in item:
			title=item["spotTitle"]
		else:
			title=item["title"]

		if 'isPremiere' in item:
			isPremiere = item["isPremiere"]
		elif 'premiere' in item:
			isPremiere = item['premiere']

		if isPremiere:
			title = title + " *PREMIERE* "
			
		if 'spotSubTitle' in item:
			summary=item["spotSubTitle"]
			subtitle=None
		else:
			summary=item["description"]
			subtitle=item["broadcastChannel"] + ": " + item["formattedBroadcastTime"]
			if 'duration' in item:
				subtitle = subtitle + " ["+ item["duration"] + "]"

		if 'videoResourceUrl' in item:
			video=item["videoResourceUrl"]
                else:
			video =JSON.ObjectFromURL(key)["videoResourceUrl"]
		
                ## Log("title=" + str(title) + ", subtitle=" + str(subtitle) + ", thumb=" + str(thumb) + ", summary=" + str(summary) + ", id=" + str(video)) 
		dir.Append(Function(VideoItem(GetVideos, title=title,subtitle=subtitle, summary=summary, art=art, thumb=thumb), id=video))     
		##addVideos(sender,video,title,subtitle,summary,art,thumb,dir)
	return dir

def addVideos(sender,id,title,subtitle,summary,art,thumb,dir):
	content = JSON.ObjectFromURL(id)
        for video in content["links"]:
		uri=video["uri"]
		tempclip = uri.split(":")
		Log(uri)
		clip = 'http://vodfiles.dr.dk/' + tempclip[2]	
		dir.Append(Function(VideoItem(GetVideo, title=title + " (" + str(video["bitrateKbps"]) + " bKps)", subtitle=subtitle, summary=summary, art=art, thumb=thumb),clip=clip))
		dir.Append(RTMPVideoItem(tempclip[0] + ":" + tempclip[1], clip=tempclip[2],title=title + " ( RTPM:"+ str(video["bitrateKbps"]) + " bKps)", subtitle=subtitle, summary=summary, art=art, thumb=thumb))

def GetVideo(sender, clip):
       	Log("Showing " + clip)
	return Redirect(clip)
        

def GetVideos(sender,id):
	content = JSON.ObjectFromURL(id)
	
	map = dict()
	for video in content["links"]:
		quality=int(video["bitrateKbps"])
		uri = video["uri"]
		map[quality] = uri
	Log("quality: " + str(map))
	bestUri = map[sorted(map)[0]]
	tempclip = bestUri.split(":")
	clip = 'http://vodfiles.dr.dk/' + tempclip[2]
	Log("Showing " + clip)
	return Redirect(clip)
	
def getRadioMetadata(channelId):
	JSONobj = JSON.ObjectFromURL(RADIO_NOWNEXT_URL % channelId)
	title_now = ""
	description_now = ""
	start_now = ""
	stop_now = "" 
	title_next = "" 
	description_next = "" 
	start_next = ""
	stop_next = ""
	
	try: 
		title_now = String.StripTags(JSONobj['currentProgram']['title']).replace("'","\'")
	except : pass

	try:
		description_now = "\n" +String.StripTags(JSONobj['currentProgram']['description']).replace("'","\'")
	except: pass

	try:
		start_now = "'\n" +JSONobj['currentProgram']['start'].split('T')[1].split(':')[0]+":"+JSONobj['currentProgram']['start'].split('T')[1].split(':')[1]
		stop_now = "-"+JSONobj['currentProgram']['stop'].split('T')[1].split(':')[0]+":"+JSONobj['currentProgram']['stop'].split('T')[1].split(':')[1]
	except: pass

	try:
		title_next = "\n\n" + String.StripTags(JSONobj['nextProgram']['title']).replace("'","\'")
	except : pass
	try:	
		description_next = "\n" + String.StripTags(JSONobj['nextProgram']['description']).replace("'","\'")
	except : pass
	try:	
		start_next = "\n" + JSONobj['nextProgram']['start'].split('T')[1].split(':')[0]+":"+JSONobj['nextProgram']['start'].split('T')[1].split(':')[1]
		stop_next = "-" + JSONobj['nextProgram']['stop'].split('T')[1].split(':')[0]+":"+JSONobj['nextProgram']['stop'].split('T')[1].split(':')[1]
	except: pass
	except:
		Log.Debug("Fejl i Datafeed")	
		
		
	strNowNext = title_now + description_now + start_now + stop_now + title_next + description_next + start_next + stop_next
		
	Log.Debug(strNowNext)
	return strNowNext

def getTVLiveMetadata(channelID):
	
	programs = XML.ElementFromURL(EPG_TV[channelID], isHTML=False, errors='ignore')
	
	for program in programs.iter('program'):
		info = program.find('pro_publish')
		starttime = info.findtext('ppu_start_timestamp_presentation').split('.')
		stoptime = info.findtext('ppu_stop_timestamp_presentation').split('.')
		dtStart = time.mktime(time.strptime(starttime[0], '%Y-%m-%dT%H:%M:%S'))
		dtStop = time.mktime(time.strptime(stoptime[0], '%Y-%m-%dT%H:%M:%S'))
		if time.gmtime(dtStart) < time.gmtime() and time.gmtime(dtStop) > time.gmtime():
			title = program.findtext('pro_title') + "\n\n" + info.findtext('ppu_description')
			break
		else:
			title = "Ophold i sendefladen"
	return title
	
	

	
