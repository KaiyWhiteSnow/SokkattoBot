from RustPlusFunctions.RustPlusWrapper import popAPIWrapper, activeEvents, serverInfo
from flask import render_template, Blueprint, request, redirect, url_for
from Database.Database import Session
from Database.BotModel import Bots
from Database.UserModel import Users

from User import session

RustPlus = Blueprint("rustplus", __name__)
session_instance = Session()

@RustPlus.route("/makebot", methods=["POST", "GET"])
async def makeBot():
    if request.method == "POST":
        Name = request.form.get("Name")
        Ip = request.form.get("Ip")
        Port = request.form.get("Port")
        SteamID = request.form.get("SteamID")
        Token = request.form.get("Token")
        
        logged_in_username = session.get("username")
        logged_in_user = session_instance.query(Users).filter(Users.Username == logged_in_username).first()
        
        check = session_instance.query(Bots).filter_by(Token=Token).first()
        
        if not check: 
            # Set the 'Id' attribute when creating a new Bots instance
            commit = Bots(Id=logged_in_user.User_ID, Name=Name, Ip=Ip, Port=Port, SteamID=SteamID, Token=Token)
            session_instance.add(commit)
            session_instance.commit()
        return redirect(url_for("rustplus.index"))
    return render_template("makeBot.html")

@RustPlus.route("/", methods=["POST", "GET"])
async def index():
    if request.method == "POST":
        BotID = request.form["BotID"]
        Bot = session_instance.query(Bots).filter(Bots.BotID == BotID).first()

        safe_html_code, name, players, maxPlayers, size, time = await serverInfo(Bot.Ip, Bot.Port, Bot.SteamID, Bot.Token)
        
        return render_template(
            'bot.html', 
            safe_html_code=safe_html_code, 
            name=name, 
            players=players, 
            maxPlayers=maxPlayers, 
            size=size, 
            time=time
        )

    logged_in_username = session.get("username")
    logged_in_user = session_instance.query(Users).filter(Users.Username == logged_in_username).first()
    bots = session_instance.query(Bots).filter_by(Id=logged_in_user.User_ID).all()
    
    return render_template("bots.html", bot_ids=bots)