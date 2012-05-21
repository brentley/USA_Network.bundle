SHOW_LIST = "http://feed.theplatform.com/f/OyMl-B/PleQEkKucpUm/categories?&form=json&fields=order,title,fullTitle,label,:smallBannerUrl,:largeBannerUrl&fileFields=duration,url,width,height&sort=order"
EPISODE_FEED = "http://feed.theplatform.com/f/OyMl-B/8IyhuVgUXDd_/?&form=json&fields=guid,title,description,:subtitle,content,thumbnails,categories,:fullEpisode&fileFields=duration,url,width,height,contentType,fileSize,format&byCategories=Series/%s&byCustomValue={fullEpisode}{true}&count=true"

####################################################################################################

ICON = 'icon-default.png'
ART  = 'art-default.jpg'

####################################################################################################

def Start():
    Plugin.AddPrefixHandler('/video/usanetwork', MainMenu, 'USA Network', ICON, ART)
    
    ObjectContainer.art = R(ART)
    ObjectContainer.title1 = 'USA Network'
    DirectoryObject.thumb = R(ICON)

    HTTP.CacheTime = CACHE_1HOUR
    HTTP.Headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; en-us) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27'

####################################################################################################
def MainMenu():
    oc = ObjectContainer()
    show_list = JSON.ObjectFromURL(SHOW_LIST)

    for show in show_list['entries']:
        if "Series/" in show['plcategory$fullTitle']:
            title = show['title']
        else:
            continue
        oc.add(DirectoryObject(key=Callback(EpisodesPage, title=title), title=title))

    return oc

####################################################################################################
def EpisodesPage(title):
    oc = ObjectContainer(title2=title)
    episode_list = JSON.ObjectFromURL(EPISODE_FEED % String.Quote(title))
    
    for episode in episode_list['entries']:
        video_title = episode['title']
        summary = episode['description']
        show = title
        thumbs = SortImages(episode['media$thumbnails'])
        duration = int(float(episode['media$content'][0]['plfile$duration'])*1000)
        video_url = ChooseVideoURL(episode['media$content'])
        oc.add(EpisodeObject(url=video_url, title=video_title, show=show, summary=summary,
            thumb=Resource.ContentsOfURLWithFallback(url=thumbs, fallback=ICON)))
    
    if len(oc) == 0:
        return ObjectContainer(header="Empty", message="No Episodes found.")
    
    return oc
        
####################################################################################################
def SortImages(images=[]):
    
    sorted_thumbs = sorted(images, key=lambda thumb : int(thumb['plfile$height']), reverse=True)
    thumb_list = []
    for thumb in sorted_thumbs:
        thumb_list.append(thumb['plfile$url'])

    return thumb_list
    
####################################################################################################
def ChooseVideoURL(videos=[]):
    url = ''
    for video in videos:
        if video['plfile$format'] == "MPEG4":
            url = video['plfile$url']
            break
        else:
            continue
    return url