import os
import sys
import json
import spotipy
import webbrowser
import spotipy.util as util
from json.decoder import JSONDecodeError

# Get the username from terminal
username = sys.argv[1]

# User ID: 12166626141

# Erase cashe and prompt user permission

client_id = input('Please enter client_id from Spotify_Dev Page')
client_secret = input('Please enter client_secret from Spotify_Dev Page')
redirect_uri = input('Please enter redirect_uri you will use')

try: 
	token = util.prompt_for_user_token(username,\
		client_id=client_id,\
		client_secret=client_secret,\
		redirect_uri=redirect_uri)
except: 
	os.remove(f'.cache-{username}')
	token = util.prompt_for_user_token(username,\
		client_id=client_id,\
		client_secret=client_secret,\
		redirect_uri=redirect_uri)

# Create spotifyObject

spotifyObject = spotipy.Spotify(auth=token)

user = spotifyObject.current_user()


displayName = user['display_name']
followers = user['followers']['total']

while True:

	print('\n\n')
	print(f'Welcome to Spotipy {displayName}!')
	print(f'You have {str(followers)} followers.\n')
	print('Type "research" to search for an artist or type "exit" to exit.')

	choice = input('Please enter here: ')

	if choice == "research":
		print()
		searchQuery = input('What is the name of the artist you would like to research?: ')
		print()

		search_results = spotifyObject.search(\
			searchQuery,\
			limit=1,\
			offset=0,\
			type="artist"\
			)
		#print(json.dumps(search_results, sort_keys=True, indent=4))

		print('\n\nLets take a look at the artist details.\n\n')

		# Artist Details
		artist = search_results['artists']['items'][0]
		print('The artist you searched for is ' +  str(artist['name']))
		print(str(artist['name']) + ' has ' + str(artist['followers']['total']) + ' followers!')
		print('The best genere to describe ' + str(artist['name']) + ' is ' + str(artist['genres'][0]) + '\n\n')
		webbrowser.open(artist['images'][0]['url'])

		# Album and Track details
		artist_id = artist['id']
		album_results = spotifyObject.artist_albums(\
			artist_id=artist_id,\
			album_type='album',\
			limit=20,\
			offset=0\
			)

		print('Lets also take a look at the album details!\n\n')

		albums = album_results['items']
		album_id = []
		album_artwork = []
		album_count = 0

		for iterator in albums:
			print('Album ' + str(album_count) + ': ' + iterator['name'])
			album_id.append(iterator['id'])
			album_artwork.append(iterator['images'][0]['url'])
			album_count+=1

		while True:

			album_selection = input(\
				'Enter the cooresponding number for the album artwork you would like to see. \n' \
				+ 'You may also exit by typing "exit": ')

			if album_selection == 'exit':
				break
			elif int(album_selection) in list(range(0,album_count)):
				webbrowser.open(album_artwork[int(album_selection)])
			else:
				print('Please follow the directions!')


	# Break program if the user inputs 1
	elif choice == "exit": 
		break

	else: 
		print('Please follow the directions')

# -----------------------------------------------------------------
### print json variables in a way the user can read

# print(json.dumps(VARIABLE, sort_keys=True, indent=4))

# -----------------------------------------------------------------
### Settings before running script
