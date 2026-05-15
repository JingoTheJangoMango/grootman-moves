import tidalapi
from tidalapi.types import PlaylistOrder
from tidalapi.types import OrderDirection

"""Potentional problems:
    1. Split tracks: Since the track collector splits the tracks based on a fixed number
        certain tracks may appear in a seperate playlist despite being in the same album. Please fix.

    2. The server side itself may pose problems, specifically regarding requests, Tidal is as tight as- 
        a nun when it comes to request rates.

    3. The playlist() function limit is only 50, eaning only 50 playlists can be collected. 
        I tried pagination, via the playlist_paginate() function but there seems to be a problem with it,
        as it keeps paginating the same 50 albums, so there could be something wrong with the offset funcions in the source code somewhere.
        Now as for the problem this causes, I wont be able to rename more than 50 albums within the collection, its alwasy the same ones-
        being renamed based any specific order.

"""


def main():

    session = tidalapi.Session()
    session.login_oauth_simple()
    counter = 0
    #playlist_name = playlist_namer(session)

    total_playlist_count = session.user.favorites.get_playlists_count()

    while counter < total_playlist_count:

        playlist_obj_lis = playlist_collector(session)
        
        #playlist_name = int(playlist_name)

        for playlist_obj in playlist_obj_lis:

            if playlist_obj.name.isdigit() or playlist_obj.name.endswith(".5"):

                track_id_lis = track_collector(session, playlist_obj)

                if len(track_id_lis):

                    playlist_creator(session, playlist_obj, track_id_lis)
                    track_remover(session, playlist_obj, track_id_lis)
                    playlist_renamer(session, playlist_obj)
                else:
                    playlist_renamer(session, playlist_obj)
        
        print("Batch Completed")
        counter += 50
        




def  playlist_namer(session):

    playlist_lis = session.user.favorites.playlists(order=PlaylistOrder.DateCreated, limit=10, order_direction=OrderDirection.Descending)
    playlist_name_lis = []

    for playlist in playlist_lis:
        if playlist.name.isdigit():
            playlist_name_lis.append(playlist.name)

    playlist_name_lis.sort(reverse=True)

    return playlist_name_lis[0]



def playlist_collector(session):
    #Collects all playlists in user's collection and adds them to a list that is returned

    playlist_obj_lis = []

    for playlist_obj in session.user.favorites.playlists(limit=50, order=PlaylistOrder.Name, order_direction=OrderDirection.Descending):

        if playlist_obj.name.isdigit():
            playlist_obj_lis.append(playlist_obj)
        elif playlist_obj.name.endswith(".5"):
            playlist_obj_lis.append(playlist_obj)

    return playlist_obj_lis



def track_collector(session, playlist_obj):
    #Uses playlist ids to get track count of respective playlists and then splits tracks in two based on prompt

    track_count = session.playlist(playlist_obj.id).get_tracks_count()
    track_id_lis = []
    #answer = input(f"The track count is {track_count}, split the playlist:(Y/N)")
    limit = 300

    if track_count >= limit:

        for track_obj in session.playlist(playlist_obj.id).tracks():
            track_id_lis.append(track_obj.id)

            if len(track_id_lis) == track_count // 2:
                break
    else:
        print('Playlist Skipped')

    return track_id_lis



def playlist_creator(session, playlist_obj, track_id_lis):

    playlist = session.user.create_playlist(f"{playlist_obj.name.zfill(4)}.5", "")
    playlist.add(track_id_lis)
    
    print("Playlist Created")



def track_remover(session, playlist_obj, track_id_lis):

    new_track_id_lis = [str(track) for track in track_id_lis]
    session.playlist(playlist_obj.id).delete_by_id(new_track_id_lis)

    print("All Tracks deleted")



def playlist_renamer(session, playlist_obj):
  

    if playlist_obj.name.endswith(".5"):
       
        session.playlist(playlist_obj.id).edit(f"{playlist_obj.name.zfill(6)}")
        print(f"Playlist {playlist_obj.name} renamed")
    else:
        session.playlist(playlist_obj.id).edit(f"{playlist_obj.name.zfill(4)}")
        print(f"Playlist {playlist_obj.name} Renamed")


main()