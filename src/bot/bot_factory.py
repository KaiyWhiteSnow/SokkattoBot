from rustplus import RustSocket
from markupsafe import Markup
import base64
from io import BytesIO
import logging 

class BotFunctions():    

    logger: logging.Logger = logging.getLogger("Sokkatto.factory")
    async def getGlobalInfo(self, ip: str, port: str, steam_id: int, token: int):
        logging.debug(__name__, " has been called")
        s = RustSocket(
            ip=ip, 
            port=port, 
            steam_id=steam_id, 
            player_token=token
        )
        
        logging.debug("Created socket instance")
        try: 
            await s.connect()
        except Exception as e:
            logging.error("The following error has occured during connection: ", e)
            logging.info("Maybe see if server is running currently?")
            return "Error has occured!"
        
        time = await s.get_time()
        info = await s.get_info()
        map = await s.get_map(False, False, False)
        image_buffer = BytesIO()
        map.save(image_buffer, format='PNG')
        image_data = base64.b64encode(image_buffer.getvalue()).decode('utf-8')
        html_code = f'<img src="data:image/png;base64,{image_data}" width="500" height="500">'
        safe_html_code = Markup(html_code)
        logging.debug("Information fetched, disconnecting socket")
        await s.disconnect()
        logging.debug("Socket disconnected")
        return safe_html_code, info.name, info.players, info.max_players, info.size, time
        
    async def getTime(self, ip: str, port: str, steam_id: int, token: int):
        logging.debug(__name__, " Has been called")
        s = RustSocket(
            ip=ip, 
            port=port, 
            steam_id=steam_id, 
            player_token=token
        )
        logging.debug("Socket instance created")
        s.connect()
        logging.debug("Socket connected")
        time = await s.get_time()
        logging.debug("Information fetched, disconnecting")
        s.disconnect()
        logging.debug("Socket disconnected")
        return time
    
    