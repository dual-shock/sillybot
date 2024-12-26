import asyncio
import json
import datetime
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
    Message,
    Embed,
    EmbedField,
    EmbedAuthor,
    EmbedAttachment,
    AllowedMentions,
    VoiceState
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
            await self.send_join(event)
    
    @listen(VoiceUserMove)
    async def on_voice_user_move(self, event: VoiceUserMove):
        if event.author.guild.id == self.paintcordID and event.new_channel.id != 1277714626959642721:
            await self.send_join(event)

    @listen(VoiceStateUpdate)
    async def on_voice_state_update(self, event: VoiceStateUpdate): return event


    #*METHODS
    async def create_request_interaction(self, ctx: Union[SlashContext, ContextMenuContext], sender: Union[Member, User], recipient: Union[Member, User], mention_sender: bool=False):
        sender_str = sender.mention if mention_sender else sender.display_name
        
        #! CTX.send == person who STARTED request thread
        #! USED_COMPONENT.CTX == person who ACCEPTED/DECLINED request
        #both can be ephemeral, as an answer to interaction
        
        if type(recipient.voice) is not VoiceState:
            await ctx.send(f"hi {sender_str}, the person you're trying to request is not in a voice channel, silly", ephemeral=True) 
            return

        if type(recipient.voice) is VoiceState: #!if reciever is in a vc 
            recipients_vc = recipient.voice.channel
            req_recipient_actrow = ActionRow(
                Button(
                    custom_id="accept_request",
                    style=ButtonStyle.GREEN,
                    label="Accept request",),
                Button(
                    custom_id="decline_request",
                    style=ButtonStyle.RED,
                    label="Decline request",))
            components: list[ActionRow] = [req_recipient_actrow]

            #!embed
            req_msg_obj = await self.paints_vcbots.send(f"{sender_str} is requesting {recipient.mention} to join {recipients_vc.mention}", components=components)
            
            if ctx.channel.id != self.paints_vcbots.id: await ctx.send(f"your request has been sent in {self.paints_vcbots.mention}", ephemeral=True)
            else: await ctx.send("your request has been sent", ephemeral=True)

            async def interactor_identity(attempted_comp_interaction: Component) -> bool:
                if attempted_comp_interaction.ctx.user.id == recipient.id: 
                    return True
                else:
                    await attempted_comp_interaction.ctx.send(f"this request isnt for you, silly. its for {recipient.display_name}.", ephemeral=True)
                    return False 
                
            try: 
                req_comp_interaction: Component = await self.Silly.wait_for_component(
                    components = req_recipient_actrow, 
                    check=interactor_identity, 
                    timeout = 300) #? seconds
            except TimeoutError:
                #TODO make a mark seen component 
                await req_msg_obj.edit(#!embed
                    components=[], #? None
                    content="this request has timed out, silly")
            else: 
                if req_comp_interaction.ctx.custom_id == "accept_request":
                    async def check_vc_joiner(voice_event: VoiceStateUpdate) -> bool:
                        if voice_event.after is not None: 
                            if voice_event.after.member.id == sender.id and int(voice_event.after.guild.id) == self.paintcordID:
                                return True
                        else: return False
                    if type(sender.voice) is VoiceState:
                        if int(sender.voice.guild.id) == self.paintcordID:#!embed
                            await req_msg_obj.edit(components=[], content=f"the request has been accepted. Moving {sender.display_name} to {recipients_vc.mention}.")
                            await sender.move(recipients_vc.id)#!embed
                            await req_msg_obj.edit(components=[], content=f"moved {sender.display_name} to {recipients_vc.mention}.")
                        elif int(sender.voice.guild.id) is not self.paintcordID:#!embed
                            await req_msg_obj.edit(components=[], content=f"the request has been accepted. Waiting 5 minutes for {sender.mention} to join any server VC.")
                            try: 
                                await self.Silly.wait_for("on_voice_state_update", timeout=300, checks=check_vc_joiner)
                            except TimeoutError:  #!embed
                                await req_msg_obj.edit(components=[], content=f"{sender.display_name} did not join a vc in time")
                            else:#!embed
                                await req_msg_obj.edit(components=[], content=f"the request has been accepted. Moving {sender.display_name} to {recipients_vc.mention}.")
                                await sender.move(recipients_vc.id)#!embed
                                await req_msg_obj.edit(components=[], content=f"moved {sender.display_name} to {recipients_vc.mention}.")
                    elif type(sender.voice) is not VoiceState:#!embed
                        await req_msg_obj.edit(components=[], content=f"the request has been accepted. Waiting 5 minutes for {sender.mention} to join any server VC.")
                        try: 
                            await self.Silly.wait_for("on_voice_state_update", timeout=300, checks=check_vc_joiner)
                        except TimeoutError:  #!embed
                            await req_msg_obj.edit(components=[], content=f"{sender.display_name} did not join a vc in time")
                        else:#!embed
                            await req_msg_obj.edit(components=[], content=f"the request has been accepted. moving {sender.display_name} to {recipients_vc.mention}.")
                            await sender.move(recipients_vc.id)#!embed
                            await req_msg_obj.edit(components=[], content=f"moved {sender.display_name} to {recipients_vc.mention}.")
                elif req_comp_interaction.ctx.custom_id == "decline_request":
                    await req_comp_interaction.ctx.send("you quietly declined the request, the declined user will not be notified and the request will time out.", ephemeral=True)
                    await asyncio.sleep(240)#!embed
                    await req_msg_obj.edit(components=[], content="this request has timed out, silly")  
                else: #! something unexpected happened
                    pass

    async def create_invite_interaction(self, ctx: Union[SlashContext, ContextMenuContext], sender: Union[Member, User], recipient: Union[Member, User], mention_sender: bool=False):
        sender_str = sender.mention if mention_sender else sender.display_name
        if type(sender.voice) is not VoiceState:
            await ctx.send("you cant invite someone to your vc when you're not in a vc, silly", ephemeral=True)
            return
        
        if type(sender.voice) is VoiceState:
            senders_vc = sender.voice.channel
            inv_recipient_actrow = ActionRow(
                Button(
                    custom_id="accept_invite",
                    style=ButtonStyle.GREEN,
                    label="Accept invite",),
                Button(
                    custom_id="decline_invite",
                    style=ButtonStyle.RED,
                    label="Decline invite",))
            components: list[ActionRow] = [inv_recipient_actrow]

            inv_msg_obj = await self.paints_vcbots.send(f"{sender_str} has invited {recipient.mention} to join {senders_vc.mention}", components=components)

            if ctx.channel.id != self.paints_vcbots.id: await ctx.send(f"your invite has been sent in {self.paints_vcbots.mention}", ephemeral=True)
            else: await ctx.send("your invite has been sent", ephemeral=True)

            async def interactor_identity(attempted_comp_interaction: Component) -> bool:
                if attempted_comp_interaction.ctx.user.id == recipient.id: 
                    return True
                else:
                    await attempted_comp_interaction.ctx.send(f"this invite isnt for you, silly. its for {recipient.display_name}.", ephemeral=True)
                    return False

            try: 
                inv_comp_interaction: Component = await self.Silly.wait_for_component(
                    components = inv_recipient_actrow, 
                    check=interactor_identity, 
                    timeout = 300) #? seconds
            except TimeoutError:
                #TODO make a mark seen component
                await inv_msg_obj.edit(
                    components=[], #? None
                    content="this invite has timed out, silly")
            else:
                if inv_comp_interaction.ctx.custom_id == "accept_invite":
                    async def check_vc_joiner(voice_event: VoiceStateUpdate) -> bool:
                        if voice_event.after is not None: 
                            if voice_event.after.member.id == recipient.id and int(voice_event.after.guild.id) == self.paintcordID:
                                return True
                        else: return False
                
                    if type(recipient.voice) is VoiceState:
                        if int(recipient.voice.guild.id) == self.paintcordID:
                            await inv_msg_obj.edit(components=[], content=f"the invite has been accepted. Moving {recipient.display_name} to {senders_vc.mention}.")
                            await recipient.move(senders_vc.id)
                            await inv_msg_obj.edit(components=[], content=f"moved {recipient.display_name} to {senders_vc.mention}.")
                        elif int(recipient.voice.guild.id) is not self.paintcordID:
                            await inv_msg_obj.edit(components=[], content=f"the invite has been accepted. Waiting 5 minutes for {recipient.mention} to join any server VC.")
                            try: 
                                await self.Silly.wait_for("on_voice_state_update", timeout=300, checks=check_vc_joiner)
                            except TimeoutError:  
                                await inv_msg_obj.edit(components=[], content=f"{recipient.display_name} did not join a vc in time")
                            else:
                                await inv_msg_obj.edit(components=[], content=f"the invite has been accepted. Moving {recipient.display_name} to {senders_vc.mention}.")
                                await recipient.move(senders_vc.id)
                                await inv_msg_obj.edit(components=[], content=f"moved {recipient.display_name} to {senders_vc.mention}.")
                    elif type(recipient.voice) is not VoiceState:
                        await inv_msg_obj.edit(components=[], content=f"the invite has been accepted. Waiting 5 minutes for {recipient.mention} to join any server VC.")
                        try: 
                            await self.Silly.wait_for("on_voice_state_update", timeout=300, checks=check_vc_joiner)
                        except TimeoutError:  
                            await inv_msg_obj.edit(components=[], content=f"{recipient.display_name} did not join a vc in time")
                        else:
                            await inv_msg_obj.edit(components=[], content=f"the invite has been accepted. moving {recipient.display_name} to {senders_vc.mention}.")
                            await recipient.move(senders_vc.id)
                            await inv_msg_obj.edit(components=[], content=f"moved {recipient.display_name} to {senders_vc.mention}.")
                elif inv_comp_interaction.ctx.custom_id == "decline_invite":
                    await inv_comp_interaction.ctx.send("you quietly declined the invite, the declined user will not be notified and the invite will time out.", ephemeral=True)
                    await asyncio.sleep(240) #TODO this is approx, make variable to track exact
                    await inv_msg_obj.edit(components=[], content="this invite has timed out, silly")
                else: #! something unexpected happened
                    pass


    async def send_join(self, event: Union[VoiceUserJoin, VoiceUserMove]):
        MEMBER: Member = event.author
        CHANNEL = event.channel if type(event) == VoiceUserJoin else event.new_channel

        embed = Embed(
            author=EmbedAuthor(
                name="User join:"
                #icon_url=MEMBER.avatar.as_url(size=512)
            ),
            color=0x00aa00,
            #title=f"{MEMBER.dis} joined {CHANNEL.mention}",
            description=f"{MEMBER.mention} joined {CHANNEL.mention}",
            thumbnail=EmbedAttachment(
                url=MEMBER.avatar.as_url(
                    size=48
                )  ,
                height=48,
                width=48
            ),
            timestamp=datetime.datetime.now(),
            # fields=[
            #     EmbedField(
            #         name=" ",
            #         value=f"**{MEMBER.mention}** joined {CHANNEL.mention}",
            #         inline=True
            #     )
            # ]
            
        )
        
        await self.paints_joinlog.send(embed=embed, allowed_mentions=AllowedMentions.none())

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
        await ctx.defer(ephemeral=True)
        await self.Silly.log("request_to_join command triggered")
        sender: Member = ctx.author
        recipient: Member = user
        await self.Silly.log(f"sender: {sender.display_name}, recipient: {recipient.display_name}")
        await self.create_request_interaction(ctx=ctx, sender=sender, recipient=recipient)

    @user_context_menu(name="Request to join VC")
    async def request_to_join_userctx(self, ctx: ContextMenuContext):
        await ctx.defer(ephemeral=True)
        await self.Silly.log("Request to join VC user command triggered")
        recipient: Member = ctx.target
        sender: Member = ctx.author
        await self.Silly.log(f"sender: {sender.display_name}, recipient: {recipient.display_name}")
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
        await ctx.defer(ephemeral=True)
        sender: Member = ctx.author
        recipient: Member = user
        await self.create_invite_interaction(ctx=ctx,sender=sender,recipient=recipient)


    @user_context_menu(name="Invite to my VC")
    async def invite_to_vc_userctx(self, ctx: ContextMenuContext):
        await ctx.defer(ephemeral=True)
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