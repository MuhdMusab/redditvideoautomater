# Reddit Video Automater

Automates the extraction of Reddit posts and transforms them into engaging short-form video content

**Reddit has changed their api, and this script may not function as expected**

## Getting started

### Clone the repository
```sh
git clone https://github.com/MuhdMusab/redditvideoautomater.git
cd ./redditvideoautomater
```

### Install packages
To install most python dependencies easily, run the following command after cloning:

```pip install -r requirements.txt```

### Install FFmpeg
Install FFmpeg from the [FFmpeg download page](https://ffmpeg.org/download.html) and add FFmpeg to the path.

### Set up Reddit app
- Go to the [Reddit Apps Panel](https://www.reddit.com/prefs/apps/).
- Click `create app...` or if you already created an app use it's credentials or click `create another app...`.
- Select `script` and fill other form sections.
- Click `create app`.
- Get client id from under the app name and client secret from `secret` section.

Run the script
```sh
python3 app.py
```
