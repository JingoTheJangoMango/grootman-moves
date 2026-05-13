import tidalapi
import time
def main():

    session = tidalapi.Session()
    session.login_oauth_simple()

    playlist_lis = playlist_collector(session)

    for playlist_id in playlist_lis:
        pass




def playlist_collector(session):

    playlist_lis = []

    for x in session.user.playlists():
        playlist_lis.append(x.id)

    return playlist_lis

def track_collector(session, playlist_id):

    track_count = session.playlist(playlist_id).get_tracks_count()
    track_id_lis = []

    if track_count > 400:

        for track_id in session.playlist(playlist_id):
            track_id_lis.append(track_id)

            if len(track_id):
                pass



