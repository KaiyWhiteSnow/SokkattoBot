from flask import render_template, request, redirect, url_for, session
from ...database import session as db_session
from ...database.models.bot_model import Bot
from ...database.models.user_model import User
from ...database.models.smart_switch_model import Switch
from ...bot.bot_functions import BotFunctions
from . import manager
from .forms import MakeBotForm, MakeSwitchForm
import logging


logger = logging.getLogger("Sokkatto.manager")
bot_functions = BotFunctions()


@manager.route("/makebot", methods=["POST", "GET"])
async def makebot():
    form = MakeBotForm()
    if form.validate_on_submit():
        logger.debug("Requesting information")
        name = form.name.data
        ip = form.ip.data
        port = form.port.data
        steam_id = form.steam_id.data
        token = form.token.data
        
        logged_in_username = session.get("username")
        logged_in_user = db_session.query(User).filter(User.username == logged_in_username).first()
        
        check = db_session.query(Bot).filter_by(token=token).first()
        
        if not check: 
            logger.debug("Bot does not yet exist, creating new bot")
            new_bot = Bot(
                bot_to_user_id=logged_in_user.user_id, 
                name=name, 
                ip=ip, 
                port=port, 
                steam_id=steam_id, 
                token=token
            )
            db_session.add(new_bot)
            db_session.commit()
            logger.debug(f"Bot saved to database under name: {name}")        
        return redirect(url_for("manager.index"))
    
    return render_template("bot/makebot.html", form=form)


@manager.route("/makeswitch", methods=["POST", "GET"])
async def make_switch():
    form = MakeSwitchForm()
    if form.validate_on_submit():
        switch_key = form.switch_key.data
        switch_name = form.switch_name.data
        
        check = db_session.query(Switch).filter_by(switch_key=switch_key).first()
        if not check:
            bot_id = session.get("bot_id")
            new_switch = Switch(switch_to_bot_id=bot_id, switch_name=switch_name, switch_key=switch_key)
            db_session.add(new_switch)
            db_session.commit()
            return redirect(url_for("manager.index"))
        # TODO: Handle switch already existing later
    return render_template("switches/makeswitch.html", form=form)


@manager.route("/dashboard", methods=["POST", "GET"])
async def dashboard():
    if request.method == "POST":
        if request.form.get("add_switch"):
            return redirect(url_for("manager.make_switch"))
        else: 
            return "death"
    bot_id = session.get("bot_id")
    bot_creds = db_session.query(Bot).filter(Bot.bot_id == bot_id).first()
    bot_switches = db_session.query(Switch).filter_by(switch_to_bot_id=bot_id)
    
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
            'main/dashboard.html', 
            map=map, 
            name=name, 
            players=players, 
            max_players=max_players, 
            size=size, 
            time=time,
            bot_switches=bot_switches
        )
    
    
@manager.route("/", methods=["POST", "GET"])
async def index():
    if request.method == "POST":
        bot_id = request.form.get("bot_id")
        session["bot_id"] = bot_id
    
        return redirect(url_for("manager.dashboard"))
        
    logged_in_username = session.get("username")
    logged_in_user = db_session.query(User).filter(User.username == logged_in_username).first()
    bots = db_session.query(Bot).filter_by(bot_to_user_id=logged_in_user.user_id).all()
    
    return render_template("bot/bots.html", bot_ids=bots)