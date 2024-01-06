import disnake
from disnake.ext import commands
from datetime import datetime


class CreateEmbedModal(disnake.ui.Modal):
    def __init__(self):
        components = [
            disnake.ui.TextInput(
                label="Title",
                placeholder="Embed title",
                custom_id="embed_title",
                style=disnake.TextInputStyle.short,
                max_length=45,
                required=False
            ),
            disnake.ui.TextInput(
                label="Description",
                placeholder="Embed description",
                custom_id="embed_description",
                style=disnake.TextInputStyle.paragraph,
                max_length=4000,
                required=False
            ),
            disnake.ui.TextInput(
                label="Color",
                placeholder="#000000",
                custom_id="embed_hex_color",
                style=disnake.TextInputStyle.short,
                max_length=9,
                min_length=7,
                required=True
            ),
            disnake.ui.TextInput(
                label="Thumbnail",
                placeholder="Image URL",
                custom_id="embed_thumbnail_url",
                style=disnake.TextInputStyle.short,
                max_length=45,
                required=False
            ),
            disnake.ui.TextInput(
                label="Image",
                placeholder="Image URL",
                custom_id="embed_image_url",
                style=disnake.TextInputStyle.short,
                max_length=45,
                required=False
            )
        ]
        
        super().__init__(title="Create Embed", custom_id="create_embed_modal", components=components)
        
    async def callback(self, inter: disnake.ModalInteraction):
        embed = disnake.Embed(
            title=inter.text_values.get("embed_title"),
            description=inter.text_values.get("embed_description"),
            color=await commands.ColorConverter().convert(inter, inter.text_values.get("embed_hex_color")),
            timestamp=datetime.now()
        )
        
        embed.set_footer(
            text=inter.author.name,
            icon_url=inter.author.avatar.url
        )
        
        embed.set_thumbnail(inter.text_values.get("embed_thumbnail_url"))
        embed.set_image(inter.text_values.get("embed_image_url"))
        
        await inter.response.send_message(embed=embed)