import json
from datetime import datetime
import os
from typing import Any, Optional

import aiofiles
import discord
from discord import Embed, app_commands
from discord.ext import commands

from schemas.data import CommandEntry
from utils.util import create_codeblock, create_embed


class CCommandInfoButtons(discord.ui.View):
    def __init__(self, je: Optional[Embed] = None, be: Optional[Embed] = None, ee: Optional[Embed] = None):
        super().__init__(timeout=None)
        self.je.disabled = je is None
        self.be.disabled = be is None
        self.ee.disabled = ee is None
        self.je_embed = je
        self.be_embed = be
        self.ee_embed = ee

    @discord.ui.button(label="JE")
    async def je(self, interaction: discord.Interaction, item: discord.ui.Item):
        await interaction.response.edit_message(embed=self.je_embed)

    @discord.ui.button(label="BE")
    async def be(self, interaction: discord.Interaction, item: discord.ui.Item):
        await interaction.response.edit_message(embed=self.be_embed)

    @discord.ui.button(label="EE")
    async def ee(self, interaction: discord.Interaction, item: discord.ui.Item):
        await interaction.response.edit_message(embed=self.ee_embed)


class CCommandInfo(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="ccommand", description="コマンドの情報を表示します")
    async def ccommand(self, interaction: discord.Interaction, command: str):
        async with aiofiles.open(os.path.join(os.getenv("BASE_DIR", "."), "data/commands.json"), mode="rb") as fp:
            data: dict[str, Any] = json.loads(await fp.read())["command_data"]
            if command not in data:
                await interaction.response.send_message(
                    embed=create_embed(title="エラー", description="コマンドが不明です")
                )
                return
            d = CommandEntry.model_validate(data[command])

        embeds = {
            'je': None,
            'be': None,
            'ee': None
        }

        def create_edition_embed(edition: str) -> Optional[Embed]:
            if getattr(d.ver, edition) is not None:
                embed = Embed(
                    color=0xAA00BB,
                    title=f"/{command}",
                    description=d.desc,
                    timestamp=datetime.now(),
                )
                embed.set_author(name={
                    'je': 'Java Edition',
                    'be': 'Bedrock Edition',
                    'ee': 'Education Edition'
                }[edition])

                options = getattr(d.options, edition)
                embed.add_field(
                    name="使用法",
                    value=create_codeblock("/" + options if options != "-" else f"/{command}"),
                    inline=False,
                )

                example = getattr(d.exmp, edition)
                embed.add_field(
                    name="例",
                    value=create_codeblock(example if example != "-" else f"/{command}"),
                    inline=False,
                )
                return embed
            return None

        for edition in ['je', 'be', 'ee']:
            embeds[edition] = create_edition_embed(edition)

        view = None
        if d.is_diff:
            view = CCommandInfoButtons(embeds['je'], embeds['be'], embeds['ee'])

        # 最初に表示するEmbed(優先順位: JE > BE > EE)
        first_embed = embeds['je'] or embeds['be'] or embeds['ee']
        await interaction.response.send_message(embed=first_embed, view=view)

    @ccommand.autocomplete("command")
    async def ccommand_autocomplete(
        self, interaction: discord.Interaction, current: str
    ):
        async with aiofiles.open(os.path.join(os.getenv("BASE_DIR", "."), "data/commands.json"), mode="rb") as fp:
            data: dict[str, Any] = json.loads(await fp.read())["command_data"]

            return [
                app_commands.Choice(name=k, value=k)
                for k in data.keys()
                if k.startswith(current)
            ][:25]


async def setup(bot: commands.Bot):
    await bot.add_cog(CCommandInfo(bot))
