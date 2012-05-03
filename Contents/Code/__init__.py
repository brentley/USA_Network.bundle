SHOW_LIST = "http://feed.theplatform.com/f/OyMl-B/PleQEkKucpUm/categories?&form=json&fields=order,title,fullTitle,label,:smallBannerUrl,:largeBannerUrl&fileFields=duration,url,width,height&sort=order"
EPISODE_FEED = "http://feed.theplatform.com/f/OyMl-B/8IyhuVgUXDd_/?&form=json&fields=guid,title,description,:subtitle,content,thumbnails,categories,:fullEpisode&fileFields=duration,url,width,height,contentType,fileSize,format&byCategories=Series/%s&byCustomValue={fullEpisode}{true}&count=true"

####################################################################################################

ICON = 'icon-default.jpg'
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
    oc = MediaContainer()
    showlist = JSON.ObjectFromURL(SHOW_LIST)

    for show in showlist:
        if "Series/" in show['plcategory$fullTitle']:
            title = show['title']
        else:
            continue
        oc.add(DirectoryObject(key=Callback(EpisodesPage, title), title=title))

    return oc

####################################################################################################
def VideoPage(sender, pageUrl, dummyUrl):
    dir = MediaContainer(title2=sender.itemTitle)
    content = XML.ElementFromURL(pageUrl, errors='ignore')

    for item in content.xpath('//item'):
        try:
            vidUrl = item.xpath('./media:content/media:player', namespaces=NAMESPACE)[0].get('url')
            vidUrl = vidUrl.replace('&dst=rss||', '')
            vidUrl = vidUrl.replace('http://video.nbcuni.com/player/?id=', dummyUrl + 'index.html?id=')
            title = item.xpath('./title')[0].text.strip()

            dir.Append(WebVideoItem(vidUrl, title=title))
        except:
            pass

    return dir
