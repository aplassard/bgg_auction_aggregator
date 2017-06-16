import urllib2
import xml.etree.ElementTree as ET
import time
import sys

geeklist_url='http://www.boardgamegeek.com/xmlapi/geeklist/'

def construct_item_url(geeklist, game):
    geeklist_id = geeklist.attrib['objectid']
    game_id = game.attrib['id']
    url = 'https://boardgamegeek.com/geeklist/'+geeklist_id+'/item/'+game_id+'#item'+game_id
    return url

def get_wishlist_items(user='aplassard'):
    wishlist_url='http://www.boardgamegeek.com/xmlapi/collection/'+user+'?wishlist=1'
    response = urllib2.urlopen(wishlist_url)
    xml = response.read()
    root = ET.fromstring(xml)
    game_ids = map(lambda x: x.attrib['objectid'], root)
    return set(game_ids)

def get_geeklists():
    meta_geeklist = geeklist_url+'66420'
    response = urllib2.urlopen(meta_geeklist)
    xml = response.read()
    root = ET.fromstring(xml)
    geeklists = filter(lambda x: x.attrib.has_key('objectid'), root)
    return geeklists

def get_games(geeklist):
    try:
        geeklist_id = geeklist.attrib['objectid']
        url = geeklist_url+geeklist_id
        response = urllib2.urlopen(url)
        xml = response.read()
        root = ET.fromstring(xml)
        games = filter(lambda x: x.attrib.has_key('objectid'), root)
    except:
        games = []
        print 'Something died in', geeklist.attrib['objectname']

    return games

def main():
    user = sys.argv[1] if len(sys.argv)>1 else 'aplassard'
    game_ids = get_wishlist_items(user)
    print len(game_ids),'games were found on the wishlist for', user
    geeklists = get_geeklists()
    aggregated_games = []
    for geeklist in geeklists:
        time.sleep(0.1)
        games = get_games(geeklist)
        aggregated_games.append((geeklist,games))

    for ag in aggregated_games:
        gl = ag[0]
        gl_name = gl.attrib['objectname']
        games = ag[1]
        for game in games:
            game_name = game.attrib['objectname']
            game_id = game.attrib['objectid']
            if game_id in game_ids:
                item_url = construct_item_url(gl, game)
                print game_name, item_url



if __name__=='__main__':
    main()
