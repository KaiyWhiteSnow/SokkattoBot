from rustplus import RustSocket

class BotFactory():
    _socket: RustSocket
    ip: str
    port: str
    player_id: int
    player_token: int
    
    def __init__(
        self,
        ip: str,
        port: str,
        player_id: int,
        player_token: int
    ) -> None:
        self.ip = ip
        self.port = port
        self.player_id = player_id
        self.player_token = player_token
        
    
    async def getGlobalInfo(self):
        s = RustSocket(
            ip=self.ip, 
            port=self.port, 
            steam_id=self.player_id, 
            player_token=self.player_token
        )
        time = await s.get_time()
        info = await s.get_info()
        team_info = await s.get_team_info()
        
        return time, info, team_info
        
    async def getTime(self):
        s = RustSocket(
            ip=self.ip, 
            port=self.port, 
            steam_id=self.player_id, 
            player_token=self.player_token
        )
        return await s.get_time()
    
    