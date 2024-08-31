from flask import render_template, Blueprint, request, redirect, url_for
from ...database import Session
from ...database.models.bot_model import Bot
from ...database.models.user_model import User
from ...bot.bot_factory import BotFunctions
from ..auth import session
import logging

logger: logging.Logger = logging.getLogger("Sokkatto.manager")

manager = Blueprint("manager", __name__, url_prefix="/manager")
session_instance = Session()
bot_functions = BotFunctions()

@manager.route("/makebot", methods=["POST", "GET"])
async def makebot():
    if request.method == "POST":
        logger.debug("Requesting information")
        name = request.form.get("name")
        ip = request.form.get("ip")
        port = request.form.get("port")
        steam_id = request.form.get("steam_id")
        token = request.form.get("token")
        
        if not name or not ip or not port or not steam_id or not token:
            logger.debug("Missing information needed to connect!")
            return "Enter credentials!"
            
        logged_in_username = session.get("username")
        logged_in_user = session_instance.query(User).filter(User.username == logged_in_username).first()
        
        check = session_instance.query(Bot).filter_by(token=token).first()
        
        if not check: 
            logger.debug("Bot does not yet exist, creating new bot")
            commit = Bot(bot_to_user_id=logged_in_user.user_id, name=name, ip=ip, port=port, steam_id=steam_id, token=token)
            session_instance.add(commit)
            session_instance.commit()
            logger.debug("Bot saved to database under name: ", name)        
        return redirect(url_for("manager.index"))
    
    return render_template("makebot.html")

@manager.route("/", methods=["POST", "GET"])
async def index():
    if request.method == "POST":
        bot_id = request.form.get("bot_id")
        bot_creds = session_instance.query(Bot).filter(Bot.bot_id == bot_id).first()
        
        (
            map, 
            name, 
            players, 
            max_players, 
            size, 
            time
        ) = await bot_functions.getGlobalInfo(
            bot_creds.ip, 
            bot_creds.port, 
            bot_creds.steam_id, 
            bot_creds.token
        )
        
        return render_template(
            'dashboard.html', 
            map=map, 
            name=name, 
            players=players, 
            max_players=max_players, 
            size=size, 
            time=time
        )

    logged_in_username = session.get("username")
    logged_in_user = session_instance.query(User).filter(User.username == logged_in_username).first()
    bots = session_instance.query(Bot).filter_by(bot_to_user_id=logged_in_user.user_id).all()
    
    return render_template("bots.html", bot_ids=bots)