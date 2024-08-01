from rustplus import RustSocket
from markupsafe import Markup
import base64
from io import BytesIO
class BotFunctions():    
    async def getGlobalInfo(self, ip: str, port: str, steam_id: int, token: int):
        s = RustSocket(
            ip=ip, 
            port=port, 
            steam_id=steam_id, 
            player_token=token
        )
        time = await s.get_time()
        info = await s.get_info()
        map = await s.get_map(False, False, False)
        map.save(BytesIO(), format='PNG')
        image_data = base64.b64encode(BytesIO().getvalue()).decode('utf-8')
        html_code = f'<img src="data:image/png;base64,{image_data}" width="500" height="500">'
        safe_html_code = Markup(html_code)
        
        return safe_html_code, info.name, info.players, info.max_players, info.size, time
        
    async def getTime(self, ip: str, port: str, steam_id: int, token: int):
        s = RustSocket(
            ip=ip, 
            port=port, 
            steam_id=steam_id, 
            player_token=token
        )
        return await s.get_time()
    
    