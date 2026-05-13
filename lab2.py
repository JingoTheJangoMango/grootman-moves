import tidalapi




def main():

    session = tidalapi.Session()
    session.login_oauth_simple()

    playlist_lis = playlist_collector(session)

    for playlist_id in playlist_lis:
        
        track_id_lis = track_collector(session, playlist_id)
        playlist_name = playlist_namer(session)

        playlist_creator(session, playlist_name, track_id_lis)



def playlist_collector(session):

    playlist_lis = []

    for x in session.user.playlists():
        playlist_lis.append(x.id)

    return playlist_lis



def track_collector(session, playlist_id):

    track_count = session.playlist(playlist_id).get_tracks_count()
    track_id_lis = []
    answer = input(f"The track count is {track_count}, split the playlist:(Y/N)")

    if answer.lower() == "y":

        for track_id in session.playlist(playlist_id):
            track_id_lis.append(track_id.id)

            if len(track_id) == track_count // 2:
                break
    else:
        print('Playlist Skipped')

    return track_id_lis



def  playlist_namer(session):

    playlist_lis = session.user.favorites.playlists(order="DATE", limit=10, order_direction="DESC")
    playlist_name_lis = []

    for playlist in playlist_lis:
        if playlist.name.is_digit():
            playlist_name_lis.append(playlist.name)

    playlist_name_lis.sort(reverse=True)

    return playlist_name_lis[0]



def playlist_creator(session, playlist_name, track_id_lis):

    playlist = session.user.LoggedInUser.create_playlist(f"{playlist_name}", "")
    session.playlist.UserPlaylist(playlist.id).add(track_id_lis)

    print('Playlist Created')



def track_remover(session, playlist_id_lis, track_id_lis):
    pass







main()