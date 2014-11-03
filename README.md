python-cmus-remote
==================

A cmus-remote implementation in Python

# Usage
```
In [1]: import cmus
In [2]: c = cmus.CmusRemote()
In [3]: c.status()
Out[4]: 
{'aaa_mode': 'album',
 'album': 'The Poison',
 'albumartist': 'Bullet For My Valentine',
 'artist': 'Bullet For My Valentine',
 'comment': 'Amazon.com Song ID: 206998831',
 'continue': True,
 'date': '2005',
 'discnumber': 1,
 'duration': 348,
 'file': "/home/fsc/music/Bullet For My Valentine - Tears Don't Fall.mp3",
 'genre': 'Pop',
 'play_library': True,
 'play_sorted': False,
 'position': 3,
 'repeat': False,
 'repeat_current': False,
 'replaygain': 'disabled',
 'replaygain_limit': True,
 'replaygain_preamp': 6.0,
 'replaygain_track_gain': '-11.0 dB',
 'shuffle': False,
 'softvol': False,
 'status': 'playing',
 'title': "Tears Don't Fall",
 'tracknumber': 4,
 'vol_left': 70,
 'vol_right': 70}
```
