import discord
import argparse
import os
import aiohttp
import aiofiles
import time


parser = argparse.ArgumentParser(description='Archy the archiving bot')
parser.add_argument('--token',
        '-t',
        help='Enter app token: ',
        type=str,
        required = True
)
parser.add_argument('--dir',
        '-d',
        help='Enter archive location: ',
        type=str,
        required = True
)

args = parser.parse_args()

archive_dir = args.dir
attachement_dir = os.path.join(archive_dir, "attachements")
directory_list = [archive_dir, attachement_dir]

def check_add_directory(directory):
    if not os.path.isdir(directory):
        os.mkdir(directory)

if __name__ == '__main__':
    client = discord.Client()
    for d in [archive_dir, attachement_dir]:
        check_add_directory(d)

    @client.event
    async def on_message(message):
        for a in message.attachments:
            async with aiohttp.ClientSession() as s:
                async with s.get(a.url) as r:
                    if r.status == 200:
                        f = await aiofiles.open(os.path.join(attachement_dir, a.filename), mode='wb')
                        await f.write(await r.read())
                        await f.close()
    
        filename = os.path.join(archive_dir, str(message.channel.id))
        t = str(time.time())
        wf = await aiofiles.open(filename, mode='a')
        await wf.write(f"{t},{message.channel.id},{message.author},{message.content}\n")
        await wf.close()

       


    client.run(args.token)
