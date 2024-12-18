import asyncio
from interactions import (
    Extension, 
    slash_command, 
    SlashContext,
    listen,
    OptionType, 
    slash_option,
    Member,ActionRow, Button, ButtonStyle, )
from interactions.api.events.discord import (
    VoiceStateUpdate
)
from interactions.api.events import Component







class vcReq(Extension):
    def __init__(self, client):
        self.client = client
        asyncio.create_task(self.async_init())
        self.dev_channel = self.client.get_channel(1318190826458714214)
    def drop(self):
        asyncio.create_task(self.async_drop())
        super().drop()
    async def async_init(self):
        print(f"- {self.__class__.__name__} loaded!")    
    async def async_drop(self):
        print(f"- {self.__class__.__name__} unloaded!")
        pass


    @listen(VoiceStateUpdate)
    async def on_voice_state_update(self, event: VoiceStateUpdate):
        print(event.before, event.after)
        if event.before is not None: 
            channel_left = event.before.channel.name
            member_left = event.before.member.mention
            await self.dev_channel.send(f"GLOBAL VoiceState update, {member_left} left {channel_left}")
        if event.after is not None: 
            channel_left = event.after.channel.name
            member_left = event.after.member.mention
            await self.dev_channel.send(f"GLOBAL VoiceState update, {member_left} joined {channel_left}")
        return event
            
    @slash_command(
        name="req", 
        description="request to join someones vc or request for someone to join your vc"
    )
    @slash_option(
        name="user", 
        description="the member you're requesting to join",
        required=True,
        opt_type=OptionType.USER
    )
    async def req(self, ctx: SlashContext, user: Member):
        SENDER = ctx.author
        RECIPIENT = user
        # if recipient of the request is in a voice channel
        if RECIPIENT.voice is not None:
            SENDER_REQUESTED_VC = RECIPIENT.voice.channel

            req_recipient_actrow = ActionRow(
                Button(
                    style=ButtonStyle.GREEN,
                    label="Accept request",
                ),
                Button(
                    style=ButtonStyle.RED,
                    label="Deny request",
                )
            )
            components: list[ActionRow] = [req_recipient_actrow]
            # request RECIPIENT if they allow author to join, valid for 5 minutes, see used_component
        
            no_mic_channel = self.client.get_channel(1279254041662197820)
            req_recipient_message = await ctx.send(f"{SENDER.mention} is requesting {RECIPIENT.mention} to join {SENDER_REQUESTED_VC.name}", components=components, ephemeral=False)
            
            # persisent check to make sure only recipient can answer the request, and create an invite
            async def check(component: Component) -> bool:
                if component.ctx.user.id == RECIPIENT.id: 
                    await self.dev_channel.send("the component interactor and request recipient are the same")
                    return True
                else:
                    await self.dev_channel.send("the component interactor and request recipient are NOT the same")
                    await component.ctx.send(f"Sorry, you're not the recipient of this request. {component.ctx.user} is.", ephemeral=True)
                    return False 
                
            try: used_component: Component = await self.client.wait_for_component(components = req_recipient_actrow,check=check, timeout = 60*5)
            except: await req_recipient_message.edit(components=components, content="Request timed out")
            else: 
                if used_component.ctx.component.label == "Accept request":
                    await self.dev_channel.send("the request to join was ACCEPTED by the RECIPIENT")
                    if SENDER.voice is not None: #if SENDER is in a vc
                        await self.dev_channel.send("the REQUESTOR is in a vc, and is getting moved")
                        await SENDER.move(SENDER_REQUESTED_VC.id)
                        await req_recipient_message.edit(components=[], content=f"The request has been accepted. Moving the requestor to the recipients channel.")
                    else: #if SENDER is not in a vc
                        await req_recipient_message.edit(components=[], content=f"The request has been accepted. Waiting for 5 minutes to see if the requestor joins.")
                        await self.dev_channel.send("the REQUESTOR is NOT in a vc, and is NOT getting moved")
                        await self.dev_channel.send("waiting for 5 minutes to see if they join a vc")
                        try: 
                            await self.client.wait_for("on_voice_state_update", timeout=60*5)
                            await self.dev_channel.send("voice state event detected by waiter")
                            await SENDER.move(SENDER_REQUESTED_VC.id)
                        except TimeoutError: 
                            await self.dev_channel.send("the REQUESTOR did not join a vc in time")
                else: #used_component.ctx.component.label == "Deny request":
                    await self.dev_channel.send("the request to join was DENIED by the RECIPIENT")
                    await ctx.send("You quietly denied the request, the denied user will not be notified.", ephemeral=True)
                    await req_recipient_message.delete()
                    

        else: # if recipient of the request is not in a voice channel
            await ctx.send("The person you're trying to request is not in a voice channel", ephemeral=True) 
        


def setup(client):
    vcReq(client)