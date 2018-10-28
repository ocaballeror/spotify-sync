# Spotify sync
Small app to sync your local music library with spotify.

## Setup
Follow the usual setup for spotify apps from [the official documentation](https://developer.spotify.com/documentation/web-api/quick-start/).

When you have signed up to the spotify developer program, go to
[your dashboard](https://developer.spotify.com/dashboard/applications) and
create a new app to get your authentication tokens. Give the app whatever name
you like (not important) and you should get a client ID and client secret to
use. Go to "Edit settings" and add a new "Redirect URI". This URI can be
anything, for example `http://localhost/`.

Now that you have your client ID, secret and redirect URI, copy
`config.json.template` to `config.json` and paste the values in the appropriate
keys and you are ready to go.

## Python stuff
An unspoken rule among the python community forces me to instruct you on how to
install dependencies.

In case you forgot how to do it, you just have to run
```
pip install requirements.txt
```
and you're good to go. That was easy.

## Running
No extra arguments, no nonsense, just run
```
python sync.py <your-username>
```
and the script will get to work.

When you run it for the first time, it will open a browser window to let you
authenticate your Spotify account. Accept the permissions request, and paste
the URL you were redirected to into the console. You can now go to your Spotify
library and see new albums start to pop up.

## Credit
All credit must go to the [spotipy](https://github.com/plamere/spotipy)
library, which made all of this possible.
