from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.event.message import FriendMessage
from graia.ariadne.message.element import At, Plain, Source, Element,Image
from graia.ariadne.model import  Group, Member, Friend
from graia.ariadne.event.mirai import NudgeEvent

from .data import stage3,weapons3

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
    if str(message) =='、工':
        times=0
    elif str(message) =='、下工':
        times=1
    elif str(message) == '、下下工':
        times=2
    elif str(message) == '、下下下工':
         times=3

         

    if times >=0:
        GameURL = 'https://splatoon3.ink/data/schedules.json'
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        header= { 'User-Agent' : user_agent }
        GameMode = requests.get(GameURL,headers=header).json()
        now = datetime.now()
        salmon_file=GameMode
        img_path = get_conf('resource_path')

        base_img = PIL.Image.open(img_path+ 'misc/bgx.jpg').convert("RGBA")
        radii=20
        base_sep=8
        scale=1.5
        base_xx=20
        base_yy=60
        draw = PIL.ImageDraw.Draw(base_img)
        font = PIL.ImageFont.truetype(img_path+"font/youshebiaotihei.ttf", 20) 
        timecol=30

        Map = stage3[str(salmon_file['data']['coopGroupingSchedule']['regularSchedules']['nodes'][times]['setting']['coopStage']['name'])]['image']
        MapName = stage3[str(salmon_file['data']['coopGroupingSchedule']['regularSchedules']['nodes'][times]['setting']['coopStage']['name'])]['name']

        stime = (datetime.strptime(salmon_file['data']['coopGroupingSchedule']['regularSchedules']['nodes'][times]['startTime'],"%Y-%m-%dT%H:%M:%SZ") + timedelta(hours=8)).strftime("%d日%H时")
        etime = (datetime.strptime(salmon_file['data']['coopGroupingSchedule']['regularSchedules']['nodes'][times]['endTime'],"%Y-%m-%dT%H:%M:%SZ") + timedelta(hours=8)).strftime("%d日%H时")
        #draw.text((base_xx,timecol-10), stime +' - '+ etime, (255, 255, 255), font=font)
        font = PIL.ImageFont.truetype(img_path+"font/msyh.ttc", 40)
        draw.text((base_xx,timecol-20), MapName, (255, 255, 255), font=font)

  

        tmp_img = PIL.Image.open(img_path+Map)
        base_x = int(tmp_img.size[0]*scale)+base_sep*2
        base_y = int(tmp_img.size[1]*scale)+base_sep*2
        timecol=base_y+base_yy    

        #draw.text((base_xx,timecol), stime +' - '+ etime, (255, 255, 255), font=font)
        #draw.text((base_xx,timecol-10), MapName, (255, 255, 255), font=font)
        #地图图片位置
        base_img = merge_image(base_img,tmp_img,base_xx,base_yy,scale)

        #武器初始位置=地图位置+空格
        base_wep_y = base_yy
        base_wep_x = base_x+base_xx
        k=0
 
        for j in salmon_file['data']['coopGroupingSchedule']['regularSchedules']['nodes'][times]['setting']['weapons']:
            tmp_img = PIL.Image.open(img_path+'weapons/'+weapons3[j['name']]['wimg'])
            if j['name']=='Random':
              wep_rate=1
            else:
              wep_rate=0.25
            base_img=merge_image(base_img,tmp_img,base_wep_x,base_wep_y,0.35)
            k=k+1	
            if k==2:
                base_wep_y=base_wep_y+int(tmp_img.size[1]*wep_rate)+base_sep*2
                base_wep_x=base_x+base_xx+base_sep
            elif k==1 or k==3:
                base_wep_x=base_wep_x+int(tmp_img.size[0]*wep_rate)+base_sep*4
        base_img = base_img.crop((0,0,base_img.size[0]-60,base_img.size[1]/2)) #	
        base_img = circle_corner(base_img, radii)
        message = MessageChain(At(target.id),Plain('\n打工安排:'+ stime+ '-' + etime),Image(base64=img_to_b64(base_img)))
        await app.send_message(sender, message)
 
       
        
