from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.event.message import FriendMessage
from graia.ariadne.message.element import At, Plain, Source, Element,Image
from graia.ariadne.model import  Group, Member, Friend
from graia.ariadne.event.mirai import NudgeEvent

from .data import stage3

from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema

import requests
import datetime
from datetime import datetime, timedelta
from io import BytesIO
import time
import PIL.Image
import PIL.ImageFont
import PIL.ImageDraw
from .img_utils import img_to_b64 ,circle_corner,merge_image
from .conf_utils import get_conf
channel = Channel.current()


from typing import Union

@channel.use(ListenerSchema(listening_events=[GroupMessage, FriendMessage]))
async def hello(app: Ariadne, sender: Group, message: MessageChain, target: Union[Member, Friend, str],):
    times = -1

    if str(message) =='、图':
        times=0
    elif str(message) =='、下图':
        times=1
    elif str(message) == '、下下图':
        times=2
    elif str(message) == '、下下下图':
         times=3

    if times >=0:
        GameURL = 'https://splatoon3.ink/data/schedules.json'
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        header= { 'User-Agent' : user_agent }
        GameMode = requests.get(GameURL,headers=header).json()
        now = datetime.now()
        game_file=GameMode
        gamemode_rule_name ={'Clam Blitz':'蛤蜊','Tower Control':'占塔','Splat Zones':'区域','Rainmaker':'抢鱼','Turf War':'涂地'}
        try: 
            Map1R = stage3[str(game_file['data']['regularSchedules']['nodes'][times]['regularMatchSetting']['vsStages'][0]['vsStageId'])]['cname']
            Map2R = stage3[str(game_file['data']['regularSchedules']['nodes'][times]['regularMatchSetting']['vsStages'][1]['vsStageId'])]['cname']

            GameModeR = '涂地'
            StartTimeR = str((datetime.strptime(game_file['data']['regularSchedules']['nodes'][times]['startTime'],"%Y-%m-%dT%H:%M:%SZ") + timedelta(hours=8)).hour) + '时'
            EndTimeR =   str((datetime.strptime(game_file['data']['regularSchedules']['nodes'][times]['endTime'],"%Y-%m-%dT%H:%M:%SZ") + timedelta(hours=8)).hour) + '时'
        

            Map1S = stage3[str(game_file['data']['bankaraSchedules']['nodes'][times]['bankaraMatchSettings'][0]['vsStages'][0]['vsStageId'])]['cname']
            Map2S = stage3[str(game_file['data']['bankaraSchedules']['nodes'][times]['bankaraMatchSettings'][0]['vsStages'][1]['vsStageId'])]['cname']
            GameModeS = gamemode_rule_name[ game_file['data']['bankaraSchedules']['nodes'][times]['bankaraMatchSettings'][0]['vsRule']['name']]
            if (len(GameModeS)) == 2:
                GameModeS=GameModeS[0]+'\n'+GameModeS[1]
            else:
                GameModeS='\n'+GameModeS[0]
    
            StartTimeS = str((datetime.strptime(game_file['data']['bankaraSchedules']['nodes'][times]['startTime'],"%Y-%m-%dT%H:%M:%SZ") + timedelta(hours=8)).hour) + '时'
            EndTimeS =   str((datetime.strptime(game_file['data']['bankaraSchedules']['nodes'][times]['endTime'],"%Y-%m-%dT%H:%M:%SZ") + timedelta(hours=8)).hour) + '时'  
            Map1L = stage3[str(game_file['data']['bankaraSchedules']['nodes'][times]['bankaraMatchSettings'][1]['vsStages'][0]['vsStageId'])]['cname']
            Map2L = stage3[str(game_file['data']['bankaraSchedules']['nodes'][times]['bankaraMatchSettings'][1]['vsStages'][1]['vsStageId'])]['cname']
        
            GameModeL = gamemode_rule_name[ game_file['data']['bankaraSchedules']['nodes'][times]['bankaraMatchSettings'][1]['vsRule']['name']]
            GameMode = GameModeL
            if (len(GameModeL)) == 2:
                GameModeL=GameModeL[0]+'\n'+GameModeL[1]
            else:
                GameModeL='\n'+GameModeL[0]
            StartTimeL, EndTimeL = StartTimeS, EndTimeS 
            StartTimeX = str((datetime.strptime(game_file['data']['xSchedules']['nodes'][times]['startTime'],"%Y-%m-%dT%H:%M:%SZ") + timedelta(hours=8)).hour) + '时'
            EndTimeX =   str((datetime.strptime(game_file['data']['xSchedules']['nodes'][times]['endTime'],"%Y-%m-%dT%H:%M:%SZ") + timedelta(hours=8)).hour) + '时'
            Map1X = stage3[str(game_file['data']['xSchedules']['nodes'][times]['xMatchSetting']['vsStages'][0]['vsStageId'])]['cname']
            Map2X = stage3[str(game_file['data']['xSchedules']['nodes'][times]['xMatchSetting']['vsStages'][1]['vsStageId'])]['cname']

            GameModeX = gamemode_rule_name[ game_file['data']['xSchedules']['nodes'][times]['xMatchSetting']['vsRule']['name']]
            GameMode = GameModeX
            if (len(GameModeX)) == 2:
                GameModeX=GameModeX[0]+'\n'+GameModeX[1]
            else:
                GameModeX='\n'+GameModeX[0]
            StartTimeX, EndTimeX = StartTimeX, EndTimeX
        except Exception as e:
            pass
            Map1R = stage3[str(game_file['data']['festSchedules']['nodes'][times]['festMatchSetting']['vsStages'][0]['vsStageId'])]['cname']
            Map2R = stage3[str(game_file['data']['festSchedules']['nodes'][times]['festMatchSetting']['vsStages'][1]['vsStageId'])]['cname']

            GameModeR = '涂地'
            StartTimeR = str((datetime.strptime(game_file['data']['festSchedules']['nodes'][times]['startTime'],"%Y-%m-%dT%H:%M:%SZ") + timedelta(hours=8)).hour) + '时'
            EndTimeR =   str((datetime.strptime(game_file['data']['festSchedules']['nodes'][times]['endTime'],"%Y-%m-%dT%H:%M:%SZ") + timedelta(hours=8)).hour) + '时'
        img_path = 'E:\\game\\bot\\inkbot\\src\\resource\\'

        img_path = get_conf('resource_path')
        base_img = PIL.Image.open(img_path+'misc/bg3.jpg')
        radii=20
        base_img = circle_corner(base_img, radii)
        base_sep=8
        scale=0.8
        base_xx=100
        base_yy=15
        endtime = datetime.now()
        starttime = endtime

        tmp_img = PIL.Image.open(img_path+stage3[str(game_file['data']['regularSchedules']['nodes'][times]['regularMatchSetting']['vsStages'][0]['vsStageId'])]['image'])
        base_img=merge_image(base_img,tmp_img,base_xx,base_yy,scale)
        base_xx_incr=base_xx+int(tmp_img.size[0]*scale)+base_sep
        tmp_img = PIL.Image.open(img_path+stage3[str(game_file['data']['regularSchedules']['nodes'][times]['regularMatchSetting']['vsStages'][1]['vsStageId'])]['image'],)
        base_img=merge_image(base_img,tmp_img,base_xx_incr,base_yy,scale)
        base_yy_incr=int(tmp_img.size[1]*scale)+base_sep+base_yy
        tmp_img=PIL.Image.open(img_path+'mode/regular.png')
        base_img=merge_image(base_img,tmp_img,base_xx_incr-35,int(base_yy_incr/2)-20,0.5)
        
        tmp_img = PIL.Image.open(img_path+stage3[str(game_file['data']['bankaraSchedules']['nodes'][times]['bankaraMatchSettings'][0]['vsStages'][0]['vsStageId'])]['image'])
        base_img=merge_image(base_img,tmp_img,base_xx,base_yy_incr,scale)
        tmp_img = PIL.Image.open(img_path+stage3[str(game_file['data']['bankaraSchedules']['nodes'][times]['bankaraMatchSettings'][0]['vsStages'][1]['vsStageId'])]['image'])
        base_img=merge_image(base_img,tmp_img,base_xx_incr,base_yy_incr,scale)
        tmp_img=PIL.Image.open(img_path+'mode/rank.png')
        base_img=merge_image(base_img,tmp_img,int(base_xx_incr)-35,int(base_yy_incr)+30,0.5)

        tmp_img = PIL.Image.open(img_path+stage3[str(game_file['data']['bankaraSchedules']['nodes'][times]['bankaraMatchSettings'][1]['vsStages'][0]['vsStageId'])]['image'])
        base_img=merge_image(base_img,tmp_img,base_xx,int(base_yy_incr*1.5)+65,scale)
        tmp_img = PIL.Image.open(img_path+stage3[str(game_file['data']['bankaraSchedules']['nodes'][times]['bankaraMatchSettings'][1]['vsStages'][1]['vsStageId'])]['image'])
        base_img=merge_image(base_img,tmp_img,base_xx_incr,int(base_yy_incr*1.5)+65,scale)
        tmp_img=PIL.Image.open(img_path+'mode/league1.png')
        base_img=merge_image(base_img,tmp_img,int(base_xx_incr)-35,int(base_yy_incr*2)+20,0.5)

        #x mode
        tmp_img = PIL.Image.open(img_path+stage3[str(game_file['data']['xSchedules']['nodes'][times]['xMatchSetting']['vsStages'][0]['vsStageId'])]['image'])
        base_img=merge_image(base_img,tmp_img,base_xx,448,scale)
        tmp_img = PIL.Image.open(img_path+stage3[str(game_file['data']['xSchedules']['nodes'][times]['xMatchSetting']['vsStages'][1]['vsStageId'])]['image'])
        base_img=merge_image(base_img,tmp_img,base_xx_incr,448,scale)
        tmp_img=PIL.Image.open(img_path+'mode/x.png')
        base_img=merge_image(base_img,tmp_img,int(base_xx_incr)-35,490,0.5)
        
        draw = PIL.ImageDraw.Draw(base_img)
        font = PIL.ImageFont.truetype(img_path+"font/youshebiaotihei.ttf", 45)
        draw.text((30,20 ), f"涂\n地", (255, 255, 255), font=font)
        draw.text((30,170), GameModeS, (255, 255, 255), font=font)
        draw.text((30,310), GameModeL, (255, 255, 255), font=font)
        draw.text((30,460), GameModeX, (255, 255, 255), font=font)
        base_img=base_img.resize((int(base_img.size[0]*0.8), int(base_img.size[1]*0.8)),PIL.Image.ANTIALIAS)
        #rgb_img = base_img.convert('RGB')
        message = MessageChain(At(target.id),Plain('\n所处时段:'+ StartTimeR+ '-' + EndTimeR),Image(base64=img_to_b64(base_img)))
        await app.send_message(sender, message)



