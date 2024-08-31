from rustplus import RustSocket
from markupsafe import Markup
import base64
from io import BytesIO
import logging 

class BotFunctions():    

    logger: logging.Logger = logging.getLogger("Sokkatto.factory")
    async def getGlobalInfo(self, ip: str, port: str, steam_id: int, token: int):
        self.logger.debug(__name__, " has been called")
        s = RustSocket(
            ip=ip, 
            port=port, 
            steam_id=steam_id, 
            player_token=token
        )
        
        self.logger.debug("Created socket instance")
        try: 
            await s.connect()
        except Exception as e:
            self.logger.error("The following error has occured during connection: ", e)
            self.logger.info("Maybe see if server is running currently?")
            return "Error has occured!"
        
        time = await s.get_time()
        info = await s.get_info()
        map = await s.get_map(False, False, False)
        image_buffer = BytesIO()
        map.save(image_buffer, format='PNG')
        image_data = base64.b64encode(image_buffer.getvalue()).decode('utf-8')
        html_code = f'<img src="data:image/png;base64,{image_data}" width="500" height="500">'
        safe_html_code = Markup(html_code)
        self.logger.debug("Information fetched, disconnecting socket")
        await s.disconnect()
        self.logger.debug("Socket disconnected")
        return safe_html_code, info.name, info.players, info.max_players, info.size, time
        
    async def getTime(self, ip: str, port: str, steam_id: int, token: int):
        self.logger.debug(__name__, " Has been called")
        s = RustSocket(
            ip=ip, 
            port=port, 
            steam_id=steam_id, 
            player_token=token
        )
        self.logger.debug("Socket instance created")
        s.connect()
        self.logger.debug("Socket connected")
        time = await s.get_time()
        self.logger.debug("Information fetched, disconnecting")
        s.disconnect()
        self.logger.debug("Socket disconnected")
        return time
    
    async def getServerName(self, ip: str, port: str, steam_id: int, token: int):
        s = RustSocket(
            ip=ip, 
            port=port, 
            steam_id=steam_id, 
            player_token=token
        )
        self.logger.debug("Socket instance created")
        s.connect()
        server_info = s.get_info()
        s.disconnect()
        return server_info.name
        