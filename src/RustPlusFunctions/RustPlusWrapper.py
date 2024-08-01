
from rustplus import RustSocket, convert_xy_to_grid
from flask import Flask
from markupsafe import Markup
import base64
from io import BytesIO


async def popAPIWrapper(IP: str, port: str, SteamID: int, PlayerToken: int):
    socket = RustSocket(ip=IP, port=port, steam_id=SteamID, player_token=PlayerToken)
    await socket.connect()
    info = await socket.get_info()
    await socket.disconnect()  # Disconnect the socket when done
    return info

async def activeEvents(IP: str, port: str, SteamID: int, PlayerToken: int):
    socket = RustSocket(ip=IP, port=port, steam_id=SteamID, player_token=PlayerToken)
    await socket.connect()

    event_type_names = {
        1: "Player",
        2: "Explosion",
        3: "Vending Machine",
        4: "Chinook",
        5: "Cargo Ship",
        6: "Crate",
        7: "Generic Radius",
        8: "Patrol Helicopter",
    }

    events = await socket.get_current_events()
    for event in events:
        event_type = event.type
        if event_type in event_type_names:
            event_name = event_type_names[event_type]
            map_size = await socket.get_info()
            grid = convert_xy_to_grid((event.x, event.y), map_size.size)
            if event is None and grid is None:
                event = "I do not exist"
                grid = "I do not exist either"
                await socket.disconnect()
                return event, grid
            else:
                await socket.disconnect()
                return event, grid

async def serverInfo(IP: str, port: str, SteamID: int, PlayerToken: int):
    socket = RustSocket(ip=IP, port=port, steam_id=SteamID, player_token=PlayerToken)
    await socket.connect()
    
    rustInfo = await socket.get_info()
    timeObj = await socket.get_time()
    map = await socket.get_map(False, False, False)
    image_buffer = BytesIO()
    map.save(image_buffer, format='PNG')
    image_data = base64.b64encode(image_buffer.getvalue()).decode('utf-8')
    html_code = f'<img src="data:image/png;base64,{image_data}" width="500" height="500">'

    safe_html_code = Markup(html_code)
    name = rustInfo.name
    players = rustInfo.players
    maxPlayers = rustInfo.max_players
    size = rustInfo.size
    time = timeObj.time
    return safe_html_code, name, players, maxPlayers, size, time
