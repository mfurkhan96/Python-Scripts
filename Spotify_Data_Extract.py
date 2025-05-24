import base64 ### For Encoding
import requests ### For API calls get,put,post


client_id="f91e47a37a594eb1bffe5162de7e7776"
client_secret="12af95b20ad84c5cb92fae44f55b553b"

####### Function to get API Token  ###########################

def get_token():
  url="https://accounts.spotify.com/api/token"
  client_creds=(client_id+":"+client_secret).encode('utf-8')
  headers={"Authorization": "Basic "+str(base64.b64encode(client_creds),'utf-8'),
           "Content-Type": "application/x-www-form-urlencoded" }
  data={"grant_type": "client_credentials"}
  result=requests.post(url,headers=headers,data=data)
  return result.json()["access_token"]

########### Get token in a desired format To pass token in API call in below format #####################
def get_auth_token():
  token=get_token()
  print(token)

  headers={'Authorization': 'Bearer '+ token}
  return headers

headers=get_auth_token()

######### To get playlist id's ####################
val=requests.get("https://api.spotify.com/v1/search?q=ACDC&type=playlist&limit=20",headers=headers)
op_json=val.json()

### To get artist playlist id
##val=requests.get("https://api.spotify.com/v1/search?q=ACDC&type=artist&limit=20",headers=headers)



for i in op_json["playlists"]["items"]:
  if i is not None:
    #print(i["external_urls"]["spotify"].split("/")[-1])
    pass


def get_playlist_data():

#### Take 1 sample playlist id
  playlist_id="4wcxruxAfoisJXX0UMwUSN"

  url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"

  playlist_data=requests.get(url,headers=headers)
  playlist_data=playlist_data.json()
  #print(playlist_data)

##### Extract song details from playlist data
  all_songs=[]

  for i in playlist_data["items"]:
    #print(i["track"])
    track = i['track']
    if track and track['id']:  # Skip removed or unavailable tracks
      song={
          'id':track['id'],
          'artists':[artist['name'] for artist in track['artists']],
          'album':track['album']['name'],
          'album_id':track['album']['id'],
          'name':track['name'],
          'duration_ms':track['duration_ms'],
          'external_urls':track['external_urls']['spotify'],
          'preview_url':track['preview_url'],
          'artist_id':[artist['id'] for artist in track['artists']],
          'release_date':track['album']['release_date']
           }
    all_songs.append(song)
  return all_songs

### Get All songs in list format
all_songs=get_playlist_data()

print(all_songs)
