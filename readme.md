# Pokemon Go Keyboard

Play Pokemon Go with your keyboard in a browser

![Shot](assets/shot.png)

Environment
------------
- Python 2
- Xcode 7

Usage
------------
```bash
1. Create new Xcode project with Single View Application (or any one you like)
2. Run the app on the phone that runs Pokemon Go
3. Xcode menu -> Debug -> Simulate Location -> add GPX File to Project,
   add location.gpx to it and click location option.
4. cd path-to-clone
5. [sudo] pip install -r requirements.txt
6. ./run.py
7. Drag the marker or use your arrow keys to control your location
8. If you would like to show nearby pokemons, please run with username and
   password (a seperate username would be better to avoid getting banned). 
```

```bash
usage: run.py [-h] [-a AUTH_SERVICE] [-u USERNAME] [-p PASSWORD] [-H HOST]
              [-P PORT] [-d] [-o]

optional arguments:
  -h, --help            show this help message and exit
  -a AUTH_SERVICE, --auth-service AUTH_SERVICE
                        Auth Service
  -u USERNAME, --username USERNAME
                        Username
  -p PASSWORD, --password PASSWORD
                        Password
  -H HOST, --host HOST  Web server host
  -P PORT, --port PORT  Web server port
  -d, --debug           Debug Mode
  -o, --open            open browser
```

TODO
----
- Display nearby pokemons, pokestops and gyms

Credits
-------
[Pokemon-Go-Controller](https://github.com/kahopoon/Pokemon-Go-Controller)
[PokemonGo-Map](https://github.com/AHAAAAAAA/PokemonGo-Map)
