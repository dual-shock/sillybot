import asyncio
import json
from pathlib import Path
from typing import Union
from interactions import (
    Extension, 
    slash_command, 
    SlashContext,
    listen,
    OptionType, 
    slash_option,
    Member,
    User,
    ActionRow, 
    Button, 
    ButtonStyle, 
    is_owner, 
    check,
    user_context_menu,
    ContextMenuContext,
    Message
)

from interactions.api.events.discord import (
    VoiceStateUpdate,
    VoiceUserJoin,
    VoiceUserMove
)
from interactions.api.events import Component


#TODO let the sender cancel their request
#TODO When it times out, let it be marked as seen
#TODO make help thing
#!! My old theme is neon night


class vcReq(Extension):

    #*INIT
    def __init__(self, client):
        self.Silly = client
        asyncio.create_task(self.async_init())
        self.paintcordID = 1231133344822202468
        self.dev_channel = self.Silly.get_channel(1318190826458714214)
        self.paints_joinlog = self.Silly.get_channel(1319056168257060894)
        self.paints_vcbots = self.Silly.get_channel(1231136406026584084)
        self.secret_dungeon = self.Silly.get_channel(1277714626959642721)
    def drop(self):
        asyncio.create_task(self.async_drop())
        super().drop()
    async def async_init(self): print(f"- {self.__class__.__name__} loaded!")    
    async def async_drop(self): print(f"- {self.__class__.__name__} unloaded!")


    #*LISTENERS
    @listen(VoiceUserJoin)
    async def on_voice_user_join(self, event: VoiceUserJoin):
        if event.author.guild.id == self.paintcordID and event.channel.id != self.secret_dungeon.id:
            await self.paints_joinlog.send(f"{event.author.display_name} joined {event.channel.name}")
    
    @listen(VoiceUserMove)
    async def on_voice_user_move(self, event: VoiceUserMove):
        if event.author.guild.id == self.paintcordID and event.new_channel.id != 1277714626959642721:
            await self.paints_joinlog.send(f"{event.author.display_name} joined {event.new_channel.name}")

    @listen(VoiceStateUpdate)
    async def on_voice_state_update(self, event: VoiceStateUpdate): return event


    #*METHODS
    async def create_request_interaction(self, ctx: Union[SlashContext, ContextMenuContext], sender: Union[Member, User], recipient: Union[Member, User], mention_sender: bool=False):
        if recipient.voice is not None:
            recipient_vc = recipient.voice.channel
            req_recipient_actrow = ActionRow(
                Button(
                    style=ButtonStyle.GREEN,
                    label="Accept request",),
                Button(
                    style=ButtonStyle.RED,
                    label="Decline request",))
            components: list[ActionRow] = [req_recipient_actrow]

            if mention_sender: req_recipient_message = await self.paints_vcbots.send(f"{sender.display_name} is requesting {recipient.mention} to join {recipient_vc.mention}", components=components)
            else: req_recipient_message = await self.paints_vcbots.send(f"{sender.display_name} is requesting {recipient.mention} to join {recipient_vc.mention}", components=components)
            req_confirmation = await ctx.send(f"your request has been sent in {self.paints_vcbots.mention}", ephemeral=True)
            async def check_accepter(component: Component) -> bool:
                if component.ctx.user.id == recipient.id: return True
                else:
                    await component.ctx.send(f"this request isnt for you, silly. its for {recipient.display_name}.", ephemeral=True)
                    return False 
                
            try: used_component: Component = await self.Silly.wait_for_component(components = req_recipient_actrow,check=check_accepter, timeout = 60*5)
            except: await req_recipient_message.edit(components=[], content="this request has timed out, silly")
            else: 
                if used_component.ctx.component.label == "Accept request":
                    if sender.voice is not None: #if sender is in a vc
                        await sender.move(recipient_vc.id)
                        await req_recipient_message.edit(components=[], content=f"the request has been accepted. Moving {sender.display_name} to {recipient_vc.mention}.")
                    else: #if sender is not in a 
                        async def check_vc_joiner():
                            if sender.voice is not None: return True
                            else: return False
                        await req_recipient_message.edit(components=[], content=f"the request has been accepted. Waiting for 5 minutes to see if {sender.display_name} joins any vc.")
                        try: 
                            await self.Silly.wait_for("on_voice_state_update", timeout=60*5, checks=check_vc_joiner)
                            await sender.move(recipient_vc.id)
                        except TimeoutError:  
                            await req_recipient_message.edit(components=[], content=f"{sender.display_name} did not join a vc in time")
                else: #if used_component.ctx.component.label == "Decline request":
                    await ctx.send("you quietly declined the request, the declined user will not be notified and the request will time out.", ephemeral=True)
                    await asyncio.sleep(60*4) #TODO this is approx, make variable to track exact
                    await req_recipient_message.edit(components=[], content="This request has timed out, silly")
        else: 
            if mention_sender: await ctx.send(f"{sender.mention} the person you're trying to request is not in a voice channel", ephemeral=True) 
            else: await ctx.send("the person you're trying to request is not in a voice channel, silly", ephemeral=True) 


    async def create_invite_interaction(self, ctx: Union[SlashContext, ContextMenuContext], sender: Union[Member, User], recipient: Union[Member, User], mention_sender: bool=False):

        if sender.voice is not None: 
            print("sender of invite voice is not none")

            sender_vc = sender.voice.channel

            inv_recipient_actrow = ActionRow(
                Button(
                    style=ButtonStyle.GREEN,
                    label="Accept invite",),
                Button(
                    style=ButtonStyle.RED,
                    label="Decline invite",))
            components: list[ActionRow] = [inv_recipient_actrow]

            inv_recipient_message = await self.paints_vcbots.send(f"{recipient.mention}, you've been invited by {sender.display_name} to join {sender_vc.mention}", components=components)
            inv_confirmation = await ctx.send(f"your invite has been sent to {recipient.mention} in {self.paints_vcbots.mention}", ephemeral=True)

            async def check_accepter(component: Component) -> bool:
                if component.ctx.user.id == recipient.id: return True
                else:
                    await component.ctx.send(f"this invitation isnt for you, silly. its for {recipient.display_name}.", ephemeral=True)
                    return False
            
            try: used_component: Component = await self.Silly.wait_for_component(components = inv_recipient_actrow,check=check_accepter, timeout = 60*5)
            except: await inv_recipient_message.edit(components=[], content="this invitation has timed out, silly")
            else:
                if used_component.ctx.component.label == "Accept invite":
                    if recipient.voice is not None: #if recipient is in a vc
                        await recipient.move(sender_vc.id)
                        await inv_recipient_message.edit(components=[], content=f"the invitation has been accepted. Moving {recipient.display_name} to {sender_vc.mention}.")
                    else: #if recipient is not in a vc
                        async def check_vc_joiner():
                            if recipient.voice is not None: return True
                            else: return False
                        await inv_recipient_message.edit(components=[], content=f"the invitation has been accepted. Waiting for 5 minutes to see if {recipient.display_name} joins any vc.")
                        try:
                            await self.Silly.wait_for("on_voice_state_update", timeout=60*5, checks=check_vc_joiner)
                            await recipient.move(sender_vc.id)
                        except TimeoutError:
                            await inv_recipient_message.edit(components=[], content=f"{recipient.display_name} did not join a vc in time")
                else: #if used_component.ctx.component.label == "Decline invite":
                    await ctx.send("you quietly declined the invite, the declined user will not be notified and the invite will time out.", ephemeral=True)
                    await asyncio.sleep(60*4) #TODO this is approx, make variable to track exact
                    await inv_recipient_message.edit(components=[], content="This invite has timed out, silly")
        else: # if sender is not in a voice channel
            await ctx.send("you cant invite someone to your vc when you're not in a vc, silly", ephemeral=True)
            return



    #*COMMANDS
    #? command #1: '/request_to_join <user>'            
    @slash_command(
        name="request_to_join", 
        description="request to join someones vc"
    )
    @slash_option(
        name="user", 
        description="the member you're requesting to join",
        required=True,
        opt_type=OptionType.USER
    )
    async def request_to_join(self, ctx: SlashContext, user: Member):
        sender: Member = ctx.author
        recipient: Member = user
        await self.create_request_interaction(ctx=ctx, sender=sender, recipient=recipient)

    @user_context_menu(name="Request to join VC")
    async def request_to_join_userctx(self, ctx: ContextMenuContext):
        recipient: Member = ctx.target
        sender: Member = ctx.author
        await self.create_request_interaction(ctx=ctx, sender=sender, recipient=recipient, mention_sender=True)



    #? command #2: '/invite
    @slash_command(
        name="invite_to_vc",
        description="invite a member to join your vc"
    )
    @slash_option(
        name="user",
        description="the member you're inviting to your vc",
        required=True,
        opt_type=OptionType.USER
    )
    async def invite_to_vc(self, ctx: SlashContext, user: Member):
        sender: Member = ctx.author
        recipient: Member = user
        await self.create_invite_interaction(ctx=ctx,sender=sender,recipient=recipient)


    @user_context_menu(name="Invite to my VC")
    async def invite_to_vc_userctx(self, ctx: ContextMenuContext):
        recipient: Member = ctx.target
        sender: Member = ctx.author        
        await self.create_invite_interaction(ctx=ctx,sender=sender, recipient=recipient, mention_sender=True)


    #? command #3: '/scrape_catches'
    @slash_command(
        name="scrape_catches",
        description="get all the fish catches :D (from #bots)",
    )
    @check(is_owner())
    async def scrape_catches(self, ctx: SlashContext):
        with open(Path(__file__).with_name("newinv.json"), "w") as fp:
            count = 0
            newinv_data = {}
            bots_channel = self.Silly.get_channel(1314772261491838996)
            fish_bot_id = 1315082631225806879
            async for message in bots_channel.history(limit=None):
                if message.author.id == fish_bot_id and message.embeds is not None:
                    if len(message.embeds) != 0:
                        if message.embeds[0].description != None:
                            if "You caught" in  message.embeds[0].description:
                                count+=1
                                catch_user = str(message.interaction_metadata.user.id)

                                fish_name = message.embeds[0].description[17:][:-3]

                                #given all fish are between 10 and 600, there will always be
                                #an INT-INT-SPACE, never a letter, so just stripping the space
                                #returns the size, saves computing by not iterating is_digit()
                                #on the string
                                size_number = message.embeds[0].fields[0].value[:3]
                                #edge  where the fish is only 5cm (only one less than 10)
                                if size_number == "5 c":
                                    size_number = "5 "

                                size_number = size_number.strip()
                                size_number = int(size_number)
                                
                                try:
                                    newinv_data[catch_user]["inventory"].append({
                                        "name":fish_name,
                                        "size":size_number
                                        })  
                                except KeyError:
                                    newinv_data[catch_user] = {"inventory":[
                                        {"name":fish_name,
                                        "size":size_number }
                                    ]}
                                if count == 161: #there was 161 catches in the bots channel
                                    #from searching in disc, breaks to not scrape whole channel
                                    break
            print("FINAL COUNT", count)
            json.dump(newinv_data, fp,indent=4)
        await ctx.send("scraped some catches", ephemeral=True)
    


def setup(client):
    vcReq(client)