import discord
from discord.ext import commands
from datetime import datetime, timedelta
import asyncio
from discord import app_commands
import uuid
from typing import Optional
from discord.ext import tasks

client = commands.Bot(intents=discord.Intents.all(), command_prefix="cm!")
txt = discord.Embed


status = discord.Activity(type=discord.ActivityType.playing, name="コマンドとPythonを勉強中")


class SampleView(discord.ui.View):
    def __init__(self, timeout=None):
        super().__init__(timeout=timeout)


@client.event
async def on_ready():
    start_notice_channel = await client.fetch_channel(965098244193542154)  # 965098244193542154 # <-コマ研DISBORD用チャンネル
    SJST_time = datetime.now()
    start_embed = discord.Embed(
        title="BOTが起動しました！",
        description="なお起動後のBUMPは通知されないので自分で2時間計ってBUMPしてください！ \n ",
        color=0xffd700,
        timestamp=SJST_time
    )
    start_embed.add_field(
        name="BOT has been activated!",
        value="You should measure 2 hours and BUMP by yourself because you are not notified of the BUMP after startup!"
    )
    print("BOTが起動しました")
    await client.tree.sync()
    await client.change_presence(activity=status)
    await start_notice_channel.send(embed=start_embed)


@client.event
async def on_message(message):
    if message.author.id == 302050872383242240:  # 302050872383242240:<-DISBORD ID
        embeds = message.embeds
        if embeds is not None and len(embeds) != 0:
            if "表示順をアップしたよ" in embeds[0].description:
                JST_time = datetime.now()
                master = JST_time + timedelta(hours=2)
                fmaster = master.strftime(" %Y/%m/%d %H:%M:%S ")
                notice_channel = await client.fetch_channel(965098244193542154)  # 965098244193542154 # <-コマ研DISBORD用チャンネル
                bump_file = discord.File("bump.png", filename="bump.png")

                bump_notice_embed = discord.Embed(
                    title="BUMPを検知しました",
                    description=f"次は {fmaster} 頃に通知するね～ \n ",
                    color=0x00bfff,
                    timestamp=JST_time
                )
                bump_notice_embed.add_field(
                    name="BUMP detected",
                    value=f"The next time you can BUMP is {fmaster}"
                )

                another_channel_bump_notice_embed = discord.Embed(
                    title="別のチャンネルでBUMPを検知しました",
                    description=f"次はここのチャンネルで {fmaster} 頃に通知するね～ \n ",
                    color=0x00bfff,
                    timestamp=JST_time
                )
                another_channel_bump_notice_embed.add_field(
                    name="BUMP detected on another channel",
                    value=f"The next time you can BUMP is {fmaster} in this channel"
                )

                caution_another_channel_bump_notice_embed = discord.Embed(
                    title="ここのチャンネルでBUMPしないでね",
                    description=f"次からは {notice_channel.mention} でBUMPしてね \n ",
                    color=0xff4500,
                    timestamp=JST_time
                )
                caution_another_channel_bump_notice_embed.add_field(
                    name="Don't BUMP on this channel here",
                    value=f"Next time, BUMP at {notice_channel.mention}!"
                )

                bump_embed = discord.Embed(
                    title="BUMPの時間だよ(^O^)／",
                    description="BUMPの時間になったよ♪ \n </bump:947088344167366698> って打ってね \n \n なお他のサーバーで30分以内にBumpしてる場合はBump出来ない可能性があります。 \n ",
                    color=0x00ffff,
                    timestamp=master
                )
                bump_embed.add_field(
                    name="It's BUMP time (^O^)/",
                    value="It's BUMP time♪ \n Please send </bump:947088344167366698> \n \n If you bumped within 30 minutes on another server, you may not be able to bump."
                )
                bump_embed.set_image(url="attachment://bump.png")

                if message.channel.id == 965098244193542154:  # 965098244193542154 # <-コマ研DISBORD用チャンネル
                    await message.channel.send("＼(^o^)／", embed=bump_notice_embed)
                    await asyncio.sleep(7200)  # 7200に変更すること
                    await message.channel.send("BUMP TIME !!", file=bump_file, embed=bump_embed)

                else:
                    await notice_channel.send("＼(^o^)／", embed=another_channel_bump_notice_embed)
                    await message.channel.send(embed=caution_another_channel_bump_notice_embed)
                    await asyncio.sleep(7200)  # 7200に変更すること
                    await notice_channel.send("BUMP TIME !!", file=bump_file, embed=bump_embed)

# kugiri----------------------------------------------------------------

        # メッセージの内容をチェック
    if "https://discord.com/channels/" in message.content:
        # メッセージリンクが含まれている場合
        try:
            link = message.content.split("https://discord.com/channels/")[1].split(" ")[0].split("\n")[0]
            guild_id, channel_id, message_id = map(int, link.split("/"))
        except Exception:
            return

        # メッセージリンクが現在のサーバーに属しているかどうかをチェック
        if message.guild.id != guild_id:
            # 現在のサーバー以外のリンクには反応しない
            return
        try:
            # リンク先のメッセージオブジェクトを取得
            target_channel = client.get_guild(guild_id).get_channel(channel_id)
            target_message = await target_channel.fetch_message(message_id)

            # リンク先のメッセージオブジェクトから、メッセージの内容、送信者の名前とアイコンなどの情報を取得
            content = target_message.content
            author = target_message.author
            name = author.name
            icon_url = author.avatar.url if author.avatar else author.default_avatar.url
            timestamp = target_message.created_at
            target_message_link = f"https://discord.com/channels/{guild_id}/{channel_id}/{message_id}"

            if content == "":
                content = "本文なし"

            # Embedオブジェクトを作成
            embed = discord.Embed(
                description=content,
                color=0x00bfff,
                timestamp=timestamp
            )
            embed.set_author(name=name, icon_url=icon_url)
            embed.set_footer(text=f"From #{target_message.channel}")

            # 画像添付ファイルがある場合、最初の画像をEmbedに追加
            if target_message.attachments:
                attachment = target_message.attachments[0]  # 最初の添付ファイルを取得
                if any(attachment.filename.lower().endswith(image_ext) for image_ext in ['png', 'jpg', 'jpeg', 'gif', 'webp']):
                    embed.set_image(url=attachment.url)  # 画像をEmbedに設定

            # ボタンコンポーネントを使ったViewオブジェクトを作成
            view = SampleView(timeout=None)
            view.add_item(discord.ui.Button(label="メッセージ先はこちら", style=discord.ButtonStyle.link, url=target_message_link))

            # EmbedとViewをメッセージとして送信
            await message.channel.send(embed=embed, view=view)

            # リンク先のメッセージがembedだった場合は、元のembedも表示する
            for original_embed in target_message.embeds:
                await message.channel.send(embed=original_embed, view=view)

        except Exception as e:
            print(f"エラーらしい: {e}")
# kugiri----------------------------------------------------------------

        # メッセージの内容をチェック
    if message.channel.id == 965095619838488576:
        if message.author.bot:
            pass
        elif message.content.startswith("ぬるぽ"):
            await message.channel.send("ｶﾞﾌﾞｯ")
        elif client.user in message.mentions:
            await message.channel.send(f"{message.author.mention}呼んだ？\nわからないことがあったら【/chelp】を実行してね")
        elif message.content.startswith("!d bump"):
            await message.channel.send("そのコマンドは<t:1648767600:F>にサ終しました(笑)")
        elif message.content.startswith("/bump"):
            await message.channel.send(embed=discord.Embed(title="BUMPを実行出来てないよ!!", color=0x00bfff, timestamp=datetime.now()))
        elif message.content.startswith("oruvanoruvan"):
            await message.channel.send("ஒருவன் ஒருவன் முதலாளி\nஉலகில் மற்றவன் தொழிலாளி\nவிதியை நினைப்பவன் ஏமாளி\nஅதை வென்று முடிப்பவன் அறிவாளி\n \nபூமியை வெல்ல ஆயுதம் எதற்கு\nபூப்பறிக்க கோடரி எதற்கு\nபொன்னோ பொருளோ போர்க்களம் எதற்கு\nஆசை துறந்தால் அகிலம் உனக்கு")
    elif message.channel.id == 965098244193542154:
        if message.content.startswith("!d bump"):
            await message.channel.send("そのコマンドは<t:1648767600:F>にサ終しました(笑)")
        elif message.content.startswith("/bump"):
            await message.channel.send(embed=discord.Embed(title="BUMPを実行出来てないよ!!", color=0x00bfff, timestamp=datetime.now()))
        elif client.user in message.mentions:
            await message.channel.send(f"{message.author.mention}呼んだ？\nわからないことがあったら【/chelp】を実行してね")
    else:
        if client.user in message.mentions:
            await message.channel.send(f"{message.author.mention}呼んだ？\nわからないことがあったら【/chelp】を実行してね")

# kugiri----------------------------------------------------------------

# @client.tree.command(name="testbump", description="【運営】テスト用Bumpコマンド")
# @discord.app_commands.checks.has_role("運営")
# async def testbump(interaction: discord.Interaction):
#    embeds = discord.Embed(
#        title="BumpTest",
#        color=0xff1948,
#        description="表示順をアップしたよ:thumbsup:"
#    )
#    await interaction.response.send_message(embed=embeds)

# kugiri----------------------------------------------------------------


@client.tree.command(name="cbnoticetime", description="【運営】再起動後の通知時間設定用")
# @discord.app_commands.checks.has_role("運営")
@discord.app_commands.describe(
    addminutes="入力分後に通知されます"
)
async def cbnoticetime(interaction: discord.Interaction, addminutes: int):
    role = interaction.guild.get_role(735130783760777270)  # 735130783760777270<-コマ研運営のロールID貼ること
    if role in interaction.user.roles:  # <-上記のロールを持っていたら
        bnJST_time = datetime.now()
        ScheduledTime = bnJST_time + timedelta(minutes=addminutes)
        fScheduledTime = ScheduledTime.strftime(" %Y/%m/%d %H:%M ")
        notice_channel = await client.fetch_channel(965098244193542154)  # 965098244193542154 # <-コマ研DISBORD用チャンネル
        bump_file = discord.File("bump.png", filename="bump.png")

        bump_embed = discord.Embed(
            title="BUMPの時間だよ(^O^)/",
            description="BUMPの時間になったよ♪ \n </bump:947088344167366698> って打ってね \n \n なお他のサーバーで30分以内にBumpしてる場合はBump出来ない可能性があります。 \n ",
            color=0x00ffff,
            timestamp=ScheduledTime
        )
        bump_embed.add_field(
            name="It's BUMP time (^O^)/",
            value="It's BUMP time♪ \n Please send </bump:947088344167366698> \n \n If you bumped within 30 minutes on another server, you may not be able to bump."
        )
        bump_embed.set_image(url="attachment://bump.png")

        await interaction.response.send_message(f"{addminutes}分後({fScheduledTime}頃)に通知されます")
        await asyncio.sleep(addminutes * 60)
        await notice_channel.send("BUMP TIME !!", file=bump_file, embed=bump_embed)

    else:  # <-上記のロールを持っていなかったら
        await interaction.response.send_message("JE1.16以降\n/title @s times 20 200 20 \n/title @s title {\"text\":\"実行できませんでした\",\"bold\":true,\"color\":\"red\"} \n/title @s subtitle {\"text\":\"あなたはこのコマンドを実行する権限を持っていません\",\"underlined\":true,\"color\":\"green\"}", ephemeral=True)

# kugiri----------------------------------------------------------------


@client.tree.command(name="cmennte", description="【運営】各種お知らせ用")
@discord.app_commands.describe(
    daimei="タイトル",
    setumei="説明",
    subdaimei="サブタイトル",
    subsetumei="サブ説明"
)
async def cmennte(interaction: discord.Interaction, daimei: str, setumei: str, subdaimei: str = "", subsetumei: str = ""):
    role = interaction.guild.get_role(735130783760777270)  # <-コマ研運営のロールID貼ること
    if role in interaction.user.roles:  # <-上記のロールを持っていたら

        mntJST_time = datetime.now()

        mennte_embed = discord.Embed(
            title=daimei,
            description=setumei,
            color=0xff580f,
            timestamp=mntJST_time
        )
        mennte_embed.add_field(
            name=subdaimei,
            value=subsetumei,
        )

        await interaction.response.send_message(embed=mennte_embed)

    else:  # <-上記のロールを持っていなかったら
        await interaction.response.send_message("JE1.16以降\n/title @s times 20 200 20 \n/title @s title {\"text\":\"実行できませんでした\",\"bold\":true,\"color\":\"red\"} \n/title @s subtitle {\"text\":\"あなたはこのコマンドを実行する権限を持っていません\",\"underlined\":true,\"color\":\"green\"}", ephemeral=True)

# kugiri----------------------------------------------------------------


@client.tree.command(name="cl", description="【運営】運営専用雑コマンド")
@discord.app_commands.describe(
    choice="選択肢",
)
@discord.app_commands.choices(
    choice=[
        discord.app_commands.Choice(name="高校おめ", value="cl1"),
        discord.app_commands.Choice(name="大学おめ", value="cl2"),
        # discord.app_commands.Choice(name="test1",value="test1"),
    ]
)
async def cl(interaction: discord.Interaction, choice: discord.app_commands.Choice[str]):
    role = interaction.guild.get_role(735130783760777270)  # <-コマ研運営のロールID貼ること
    if role in interaction.user.roles:  # <-上記のロールを持っていたら
        if choice.value == "cl1":
            await interaction.response.send_message(embed=discord.Embed(title="高校合格おめでとうございます!!", color=0x2b9788))
        elif choice.value == "cl2":
            await interaction.response.send_message(embed=discord.Embed(title="大学合格おめでとうございます!!", color=0x2b9788))

# kugiri----------------------------------------------------------------


@client.tree.command(name="cuuid", description="マイクラで使えるUUIDを2個生成します")
async def cuuid(interaction: discord.Interaction):

    uuJST_time = datetime.now()
    Uuuid4 = uuid.uuid4()
    fUuuid4 = str(Uuuid4).split("-")
    cUuuid4 = fUuuid4[0] + fUuuid4[1] + fUuuid4[2] + fUuuid4[3] + fUuuid4[4]
    UUuuid4 = uuid.uuid4()
    fUUuuid4 = str(UUuuid4).split("-")
    cUUuuid4 = fUUuuid4[0] + fUUuuid4[1] + fUUuuid4[2] + fUUuuid4[3] + fUUuuid4[4]

    uuid_embed = discord.Embed(
        title="UUID Generator",
        description="-----------------------------------------------------\n2個のUUIDを自動生成しました\nBEのAdd-on制作にお役立てください\n-----------------------------------------------------",
        color=0x58619a,
        timestamp=uuJST_time
    )
    uuid_embed.add_field(
        name="１個目",
        value=f"ハイフンあり\n```{Uuuid4}```\nハイフンなし\n```{cUuuid4}```\n ",
        inline=False
    )
    uuid_embed.add_field(
        name="-----------------------------------------------------",
        value=" ",
        inline=False
    )
    uuid_embed.add_field(
        name="2個目",
        value=f"ハイフンあり\n```{UUuuid4}```\nハイフンなし\n```{cUUuuid4}```\n ",
        inline=False
    )
    await interaction.response.send_message(embed=uuid_embed)

# kugiri----------------------------------------------------------------
    # !#【アプデで更新の可能性あり｜要確認】#!#


@client.tree.command(name="cpack-mcmeta", description="pack.mcmetaで使われるpack_formatの番号一覧です")
@discord.app_commands.describe(
    choice="選択してください",
)
@discord.app_commands.choices(
    choice=[
        discord.app_commands.Choice(name="Latest-Version", value="lv"),
        discord.app_commands.Choice(name="Search-pack_format", value="spf"),
        discord.app_commands.Choice(name="ALL-ResourcePack", value="areso"),
        discord.app_commands.Choice(name="ALL-DataPack", value="adata")
    ]
)
@discord.app_commands.describe(
    version="調べたいバージョンを半角英数字で記入してください(スナップショット非対応)",
)
async def cpackmcmeta(interaction: discord.Interaction, choice: discord.app_commands.Choice[str], version: str = ""):
    # !==========更新するときに確認すること==========
    lastupdate = "最終更新日 : 2024/03/21"
    lrv = "1.20.4"
    lrv_r = "22"
    lrv_d = "26"
    lsv = "24w12a"
    lsv_r = "30"
    lsv_d = "36"
    # !==========更新するときに確認すること==========

    pmJST_time = datetime.now()
    rpacknumber = "1\n2\n3\n4\n5\n6\n7\n8\n9\n10\n11\n12\n13\n14\n15\n16\n17\n18\n19\n20\n21\n22\n23\n24\n25\n26\n27\n28\n29\n30\n31\n32\n33\n34\n35\n36\n37\n38\n39\n40"
    rallversion = "13w24a-1.8.9\n15w31a-1.10.2\n16w32a-18w47a\n18w48a-19w46b\n1.15-pre1-1.16.2-pre3\n1.16.2-rc1-1.16.5\n20w45a-21w38a\n21w39a-1.18.2\n22w11a-1.19.2\n---\n22w42a-22w44a\n22w45a-23w07a\n1.19.4-pre1-23w13a\n23w14a-23w16a\n23w17a-1.20.1\n23w31a\n23w32a-1.20.2-pre1\n1.20.2-pre2-23w41a\n23w42a\n23w43a-23w44a\n23w45a-23w46a\n1.20.3-pre1-23w51b\n---\n24w03a-24w04a\n24w05a-24w05b\n24w06a-24w07a\n---\n24w09a-24w10a\n24w11a\n24w12a"
    rreleaseversion = "1.6.1-1.8.9\n1.9-1.10.2\n1.11-1.12.2\n1.13-1.14.4\n1.15-1.16.1\n1.16.2-1.16.5\n1.17-1.17.1\n1.18-1.18.2\n1.19-1.19.2\n---\n---\n1.19.3\n1.19.4\n---\n	1.20-1.20.1\n---\n---\n1.20.2\n---\n---\n---\n1.20.3-1.20.4\n---\n---\n---\n---\n---\n---\n---\n---"
    rpack_embed = discord.Embed(
        title="【Resorce Pack】\npack_format一覧",
        color=discord.Color.yellow(),
        timestamp=pmJST_time
    )
    rpack_embed.add_field(name="pack\nnumber", value=rpacknumber, inline=True)
    rpack_embed.add_field(name="ALL\nversion", value=rallversion, inline=True)
    rpack_embed.add_field(name="release\nversion", value=rreleaseversion, inline=True)
    rpack_embed.set_footer(text="出典 : https://minecraft.wiki/w/Pack_format")

    dpacknumber = "4\n5\n6\n7\n8\n9\n10\n11\n12\n13\n14\n15\n16\n17\n18\n19\n20\n21\n22\n23\n24\n25\n26\n27\n28\n29\n30\n31\n32\n33\n34\n35\n36\n37\n38\n39\n40"
    dallversion = "17w48a-19w46b\n1.15-pre1-1.16.2-pre3\n1.16.2-rc1-1.16.5\n20w46a-1.17.1\n21w37a-22w07a\n1.18.2-pre1-1.18.2\n22w11a-1.19.3\n23w03a-23w05a\n23w06a-1.19.4\n23w12a-23w14a\n23w16a-23w17a\n23w18a-1.20.1\n23w31a\n23w32a-23w35a\n1.20.2-pre1-1.20.2\n23w40a\n23w41a\n23w42a\n23w43a-23w43b\n23w44a\n23w45a\n23w46a\n1.20.3-pre1-1.20.4\n23w51a-23w51b\n24w03a\n24w04a\n24w05a-24w05b\n24w06a\n24w07a\n24w09a\n24w10a\n24w11a\n24w12a"
    dreleaseversion = "1.13-1.14.4\n1.15-1.16.1\n1.16.2-1.16.5\n1.17-1.17.1\n1.18-1.18.1\n1.18.2\n1.19-1.19.3\n---\n1.19.4\n---\n---\n1.20-1.20.1\n---\n---\n1.20.2\n---\n---\n---\n---\n---\n---\n---\n1.20.3-1.20.4\n---\n---\n---\n---\n---\n---\n---\n---\n---\n---"
    dpack_embed = discord.Embed(
        title="【Data Pack】\npack_format一覧",
        color=discord.Color.yellow(),
        timestamp=pmJST_time
    )
    dpack_embed.add_field(name="pack\nnumber", value=dpacknumber, inline=True)
    dpack_embed.add_field(name="ALL\nversion", value=dallversion, inline=True)
    dpack_embed.add_field(name="release\nversion", value=dreleaseversion, inline=True)
    dpack_embed.set_footer(text="出典 : https://minecraft.wiki/w/Pack_format")

    lv_embed = discord.Embed(
        title="Latest Version pack_format",
        color=discord.Color.yellow(),
        timestamp=pmJST_time
    )
    lv_embed.add_field(name=f"【{lrv}】Latest Release Version", value="", inline=False)
    lv_embed.add_field(name="Resource\nPack", value=f"{lrv_r}", inline=True)
    lv_embed.add_field(name="Data\nPack", value=f"{lrv_d}", inline=True)
    lv_embed.add_field(name=f"【{lsv}】Latest Snapshot Version", value="", inline=False)
    lv_embed.add_field(name="Resource\nPack", value=f"{lsv_r}", inline=True)
    lv_embed.add_field(name="Data\nPack", value=f"{lsv_d}", inline=True)

    # pfリソパ数字_デタパ数字 = Embed...... (n = none)
    pf1_n_embed = discord.Embed(
        title=f"【{version}】Search pack_format",
        color=discord.Color.yellow(),
        timestamp=pmJST_time
    )
    pf1_n_embed.add_field(name="Resource\nPack", value="1", inline=True)
    pf1_n_embed.add_field(name="Data\nPack", value="---", inline=True)
    pf1_n_embed.set_footer(text=lastupdate)
    pf2_n_embed = discord.Embed(
        title=f"【{version}】Search pack_format",
        color=discord.Color.yellow(),
        timestamp=pmJST_time
    )
    pf2_n_embed.add_field(name="Resource\nPack", value="2", inline=True)
    pf2_n_embed.add_field(name="Data\nPack", value="---", inline=True)
    pf2_n_embed.set_footer(text=lastupdate)

    pf3_n_embed = discord.Embed(
        title=f"【{version}】Search pack_format",
        color=discord.Color.yellow(),
        timestamp=pmJST_time
    )
    pf3_n_embed.add_field(name="Resource\nPack", value="3", inline=True)
    pf3_n_embed.add_field(name="Data\nPack", value="---", inline=True)
    pf3_n_embed.set_footer(text=lastupdate)

    pf4_4_embed = discord.Embed(
        title=f"【{version}】Search pack_format",
        color=discord.Color.yellow(),
        timestamp=pmJST_time
    )
    pf4_4_embed.add_field(name="Resource\nPack", value="4", inline=True)
    pf4_4_embed.add_field(name="Data\nPack", value="4", inline=True)
    pf4_4_embed.set_footer(text=lastupdate)

    pf5_5_embed = discord.Embed(
        title=f"【{version}】Search pack_format",
        color=discord.Color.yellow(),
        timestamp=pmJST_time
    )
    pf5_5_embed.add_field(name="Resource\nPack", value="5", inline=True)
    pf5_5_embed.add_field(name="Data\nPack", value="5", inline=True)
    pf5_5_embed.set_footer(text=lastupdate)

    pf6_6_embed = discord.Embed(
        title=f"【{version}】Search pack_format",
        color=discord.Color.yellow(),
        timestamp=pmJST_time
    )
    pf6_6_embed.add_field(name="Resource\nPack", value="6", inline=True)
    pf6_6_embed.add_field(name="Data\nPack", value="6", inline=True)
    pf6_6_embed.set_footer(text=lastupdate)

    pf7_7_embed = discord.Embed(
        title=f"【{version}】Search pack_format",
        color=discord.Color.yellow(),
        timestamp=pmJST_time
    )
    pf7_7_embed.add_field(name="Resource\nPack", value="7", inline=True)
    pf7_7_embed.add_field(name="Data\nPack", value="7", inline=True)
    pf7_7_embed.set_footer(text=lastupdate)

    pf8_8_embed = discord.Embed(
        title=f"【{version}】Search pack_format",
        color=discord.Color.yellow(),
        timestamp=pmJST_time
    )
    pf8_8_embed.add_field(name="Resource\nPack", value="8", inline=True)
    pf8_8_embed.add_field(name="Data\nPack", value="8", inline=True)
    pf8_8_embed.set_footer(text=lastupdate)

    pf8_9_embed = discord.Embed(
        title=f"【{version}】Search pack_format",
        color=discord.Color.yellow(),
        timestamp=pmJST_time
    )
    pf8_9_embed.add_field(name="Resource\nPack", value="8", inline=True)
    pf8_9_embed.add_field(name="Data\nPack", value="9", inline=True)
    pf8_9_embed.set_footer(text=lastupdate)

    pf9_10_embed = discord.Embed(
        title=f"【{version}】Search pack_format",
        color=discord.Color.yellow(),
        timestamp=pmJST_time
    )
    pf9_10_embed.add_field(name="Resource\nPack", value="9", inline=True)
    pf9_10_embed.add_field(name="Data\nPack", value="10", inline=True)
    pf9_10_embed.set_footer(text=lastupdate)

    pf12_10_embed = discord.Embed(
        title=f"【{version}】Search pack_format",
        color=discord.Color.yellow(),
        timestamp=pmJST_time
    )
    pf12_10_embed.add_field(name="Resource\nPack", value="12", inline=True)
    pf12_10_embed.add_field(name="Data\nPack", value="10", inline=True)
    pf12_10_embed.set_footer(text=lastupdate)

    pf13_12_embed = discord.Embed(
        title=f"【{version}】Search pack_format",
        color=discord.Color.yellow(),
        timestamp=pmJST_time
    )
    pf13_12_embed.add_field(name="Resource\nPack", value="13", inline=True)
    pf13_12_embed.add_field(name="Data\nPack", value="12", inline=True)
    pf13_12_embed.set_footer(text=lastupdate)

    pf15_15_embed = discord.Embed(
        title=f"【{version}】Search pack_format",
        color=discord.Color.yellow(),
        timestamp=pmJST_time
    )
    pf15_15_embed.add_field(name="Resource\nPack", value="15", inline=True)
    pf15_15_embed.add_field(name="Data\nPack", value="15", inline=True)
    pf15_15_embed.set_footer(text=lastupdate)

    pf18_18_embed = discord.Embed(
        title=f"【{version}】Search pack_format",
        color=discord.Color.yellow(),
        timestamp=pmJST_time
    )
    pf18_18_embed.add_field(name="Resource\nPack", value="18", inline=True)
    pf18_18_embed.add_field(name="Data\nPack", value="18", inline=True)
    pf18_18_embed.set_footer(text=lastupdate)

    pf22_26_embed = discord.Embed(
        title=f"【{version}】Search pack_format",
        color=discord.Color.yellow(),
        timestamp=pmJST_time
    )
    pf22_26_embed.add_field(name="Resource\nPack", value="22", inline=True)
    pf22_26_embed.add_field(name="Data\nPack", value="26", inline=True)
    pf22_26_embed.set_footer(text=lastupdate)

    # versionsリソパ数字_デタパ数字 = [対応バージョンたち] (n = none)
    versions1_n = ["1.6.1", "1.6.2", "1.6.3", "1.6.4", "1.7.0", "1.7.1", "1.7.2", "1.7.3", "1.7.4", "1.7.5", "1.7.6", "1.7.7", "1.7.8", "1.7.9", "1.7.10", "1.8.0", "1.8.1", "1.8.2", "1.8.3", "1.8.4", "1.8.5", "1.8.6", "1.8.7", "1.8.8", "1.8.9"]
    versions2_n = ["1.9.0", "1.9.1", "1.9.2", "1.9.3", "1.9.4", "1.10.0", "1.10.1", "1.10.2"]
    versions3_n = ["1.11.0", "1.11.1", "1.11.2", "1.12.0", "1.12.1", "1.12.2"]
    versions4_4 = ["1.13.0", "1.13.1", "1.13.2", "1.14.0", "1.14.1", "1.14.2", "1.14.3", "1.14.4"]
    versions5_5 = ["1.15.0", "1.15.1", "1.15.2", "1.16.0", "1.16.1"]
    versions6_6 = ["1.16.2", "1.16.3", "1.16.4", "1.16.5"]
    versions7_7 = ["1.17.0", "1.17.1"]
    versions8_8 = ["1.18.0", "1.18.1"]
    versions8_9 = ["1.18.2"]
    versions9_10 = ["1.19.0", "1.19.1", "1.19.2"]
    versions12_10 = ["1.19.3"]
    versions13_12 = ["1.19.4"]
    versions15_15 = ["1.20.0", "1.20.1"]
    versions18_18 = ["1.20.2"]
    versions22_26 = ["1.20.3", "1.20.4"]

    if choice.value == "areso":
        await interaction.response.send_message(embed=rpack_embed)
    elif choice.value == "adata":
        await interaction.response.send_message(embed=dpack_embed)
    elif choice.value == "lv":
        await interaction.response.send_message(embed=lv_embed)
    elif choice.value == "spf":
        if version in versions1_n:
            await interaction.response.send_message(embed=pf1_n_embed)
        elif version in versions2_n:
            await interaction.response.send_message(embed=pf2_n_embed)
        elif version in versions3_n:
            await interaction.response.send_message(embed=pf3_n_embed)
        elif version in versions4_4:
            await interaction.response.send_message(embed=pf4_4_embed)
        elif version in versions5_5:
            await interaction.response.send_message(embed=pf5_5_embed)
        elif version in versions6_6:
            await interaction.response.send_message(embed=pf6_6_embed)
        elif version in versions7_7:
            await interaction.response.send_message(embed=pf7_7_embed)
        elif version in versions8_8:
            await interaction.response.send_message(embed=pf8_8_embed)
        elif version in versions8_9:
            await interaction.response.send_message(embed=pf8_9_embed)
        elif version in versions9_10:
            await interaction.response.send_message(embed=pf9_10_embed)
        elif version in versions12_10:
            await interaction.response.send_message(embed=pf12_10_embed)
        elif version in versions13_12:
            await interaction.response.send_message(embed=pf13_12_embed)
        elif version in versions15_15:
            await interaction.response.send_message(embed=pf15_15_embed)
        elif version in versions18_18:
            await interaction.response.send_message(embed=pf18_18_embed)
        elif version in versions22_26:
            await interaction.response.send_message(embed=pf22_26_embed)
        else:
            await interaction.response.send_message("表記が違う、または、リリースバージョンではありません\nもう一度書き直して実行してください\n(スナップショットには対応していません)", ephemeral=True)

# kugiri----------------------------------------------------------------


@client.tree.command(name="cping", description="pingを計測します")
@discord.app_commands.describe(
    kaisuu="【初期値(未記入) : 1】実行回数を自然数で入力してください。",
    t_or_f="【初期値(未記入) : True】True : 3分おきに実行 ・ False : 直ぐ(１秒おき)に実行",
)
async def cping(interaction: discord.Interaction, kaisuu: Optional[int] = 1, t_or_f: Optional[bool] = True):

    pi1JST_time = datetime.now()
    text1 = f'{round(client.latency*1000)}ms'

    ping1_embed = discord.Embed(
        title="現在のping",
        description=text1,
        color=0x400080,
        timestamp=pi1JST_time
    )

    if kaisuu >= 1:
        await interaction.response.send_message(embed=ping1_embed)

        if kaisuu > 1:
            if t_or_f:  # true
                @tasks.loop(minutes=3, count=kaisuu)  # ←あとで３分に変える
                async def interval_cb():

                    pi2JST_time = datetime.now()
                    text2 = f'{round(client.latency*1000)}ms'

                    ping2_embed = discord.Embed(
                        title="現在のping",
                        description=text2,
                        color=0x400080,
                        timestamp=pi2JST_time
                    )

                    await interaction.user.send(embed=ping2_embed)

                interval_cb.start()

            elif t_or_f is False:  # false
                @tasks.loop(seconds=1, count=kaisuu)
                async def interval_cb():

                    pi3JST_time = datetime.now()
                    text3 = f'{round(client.latency*1000)}ms'

                    ping3_embed = discord.Embed(
                        title="現在のping",
                        description=text3,
                        color=0x400080,
                        timestamp=pi3JST_time
                    )
                    await interaction.user.send(embed=ping3_embed)

                interval_cb.start()
    else:
        await interaction.response.send_message("kaisuuには自然数を入れてね(^^♪\n自然数がわからない人はこのサーバーから追放するね(^^♪♪♪", ephemeral=True)

# kugiri----------------------------------------------------------------


@client.tree.command(name="chelp", description="このBotができること一覧")
async def chelp(interaction: discord.Interaction):

    chJST_time = datetime.now()

    chelp_embed = discord.Embed(
        title="コマンド一覧",
        description="/chelp : この説明文が出てきます\n/cping : サーバーとBotとのping値を測定できます\n/cuuid : 2個のUUIDを自動生成してくれます\n/cpack-mcmeta : ResourcePackとDataPackのpack_formatの番号一覧を表示します",
        color=0x2b9900,
        timestamp=chJST_time
    )

    await interaction.response.send_message(embed=chelp_embed)

# kugiri----------------------------------------------------------------


@client.tree.error
async def on_error(ctx, error):
    if isinstance(error, app_commands.MissingRole):
        await ctx.response.send_message("権限あらへんで(関西弁)", ephemeral=True)

# kugiri----------------------------------------------------------------

with open("CMTK.txt") as file:
    client.run(file.read())

# 画面上：表示⇒ターミナル、押すと実行するための画面出てくる
# 実行コマンド1：cd Desktop\DiscordBot_Command_Lab_Official_Bot\Command-Lab-Official-Bot
# 実行コマンド2：py .\CommandLab.py
# Botを止めるときは「Ctrl+C」を押す
