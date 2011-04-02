import re

####################################################################################################

USA_FULL_EPISODES_SHOW_LIST = 'http://video.usanetwork.com/'
NAMESPACE = {'media':'http://search.yahoo.com/mrss/'}

ICON = 'icon-default.jpg'
ART  = 'art-default.jpg'

####################################################################################################

def Start():
    Plugin.AddPrefixHandler('/video/usanetwork', MainMenu, 'USA Network', ICON, ART)
    Plugin.AddViewGroup('InfoList', viewMode='InfoList', mediaType='items')

    MediaContainer.art = R(ART)
    MediaContainer.title1 = 'USA Network'
    DirectoryItem.thumb = R(ICON)
    DirectoryItem.viewGroup = 'InfoList'
    WebVideoItem.thumb = R(ICON)

    HTTP.CacheTime = CACHE_1HOUR
    HTTP.Headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; en-us) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27'

####################################################################################################
def MainMenu():
    dir = MediaContainer()
    content = HTML.ElementFromURL(USA_FULL_EPISODES_SHOW_LIST, errors='ignore')

    for item in content.xpath('//div[@id="find_it_branch_Full_Episodes"]//ul/li'):
        title = item.xpath('./a')[0].text.strip()
        titleUrl = item.xpath('./a')[0].get('href')

        page = HTTP.Request(titleUrl).content
        titleUrl2 = re.compile('var _rssURL = "(.+?)";').findall(page)[0].replace('%26', '&')

        titleUrl2 = titleUrl2 + '&networkid=103'
        if titleUrl2.count('34855') == 0: # excludes monk which is no longer full episodes
            dir.Append(Function(DirectoryItem(VideoPage, title), pageUrl=titleUrl2, dummyUrl=titleUrl))

    return dir

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
