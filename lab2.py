import tidalapi
from tidalapi.types import PlaylistOrder
from tidalapi.types import OrderDirection

"""Potentional problems:
    1. Split tracks: Since the track collector splits the tracks based on a fixed number
        certain tracks may appear in a seperate playlist despite being in the same album. Please fix.

    2. The server side itself may pose problems, specifically regarding requests, Tidal is as tight as- 
        a nun when it comes to request rates.

    3. The playlist() function limit is only 50, meaning only 50 playlists can be collected. 
        I tried pagination, via the playlist_paginate() function, but there seems to be a problem with it,
        as it keeps paginating the same 50 playlists, so there could be something wrong with the offset parameter in the source code somewhere, or alternatively its server side.
        Now as for the problem this causes, I wont be able to rename more than 50 playlists within the collection, as it's always the same ones-
        being renamed based any specific order.

"""


def main():

    session = tidalapi.Session()
    session.login_oauth_simple()

    playlist_lis = playlist_collector(session)
    playlist_name = playlist_namer(session)
    playlist_name = int(playlist_name)

    for playlist_id in playlist_lis:

        track_id_lis = track_collector(session, playlist_id)

        if len(track_id_lis):

            playlist_name += 1

            playlist_creator(session, playlist_name, track_id_lis)
            print("Playlist Created")




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

    playlist_lis = []

    for playlist_obj in session.user.favorites.playlists(limit=10):
        playlist_lis.append(playlist_obj.id)

    return playlist_lis



def track_collector(session, playlist_id):
    #Uses playlist ids to get track count of respective playlists and then splits tracks in two based on prompt

    track_count = session.playlist(playlist_id).get_tracks_count()
    track_id_lis = []
    answer = input(f"The track count is {track_count}, split the playlist:(Y/N)")

    if answer.lower() == "y":

        for track_obj in session.playlist(playlist_id).tracks():
            track_id_lis.append(track_obj.id)

            if len(track_id_lis) == track_count // 2:
                break
    else:
        print('Playlist Skipped')

    return track_id_lis



def playlist_creator(session, playlist_name, track_id_lis):

    string_name = str(playlist_name)

    playlist = session.user.create_playlist(f"{string_name.zfill(4)}", "")
    playlist.add(track_id_lis)




def track_remover(session, playlist_id, track_id_lis):
    pass

