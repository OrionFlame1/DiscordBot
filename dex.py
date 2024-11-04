import requests
from bs4 import BeautifulSoup
from discord.ext import commands
import os
from dotenv import load_dotenv
import helper as h

load_dotenv()
headers = {'User-Agent': os.getenv("User-Agent")}


@commands.command()
async def dex(ctx, *arg):
    print("dexing\n")
    if len(arg) == 0:  # no arguments in tuple
        print(f"{h.timestamp()} Args not provided")
        await ctx.send(
            "```No argument\nUsage: /dex word(or words separated by space)\nUsed for searching on dexonline.ro```")
        return
    print(f"{h.timestamp()} Searching for words {arg}")

    for word in arg:
        async with ctx.typing():
            url = "https://www.dexonline.ro/definitie/" + word
            page = requests.get(url)
            soup = BeautifulSoup(page.content, "html.parser")  # parse found page

            if not soup.find(class_="def"):  # check if there are no found words
                await ctx.send(f"```Cuvântul {word} nu a fost găsit.```")  # word not found
                if soup.find(
                        class_="list-inline list-inline-bullet list-inline-bullet-sm"):  # check if there are suggests
                    suggests = soup.find(class_="list-inline list-inline-bullet list-inline-bullet-sm").text
                    await ctx.send(f"```Încercați alte sugestii: {suggests}```")  # print suggests
                    print(f"{h.timestamp()} Found suggestions")
                    continue
                print(f"{h.timestamp()} Not found")
                continue
            el = soup.find(class_="def").text  # find the first found word
            if len(el) > 2000:  # cut for discord 2k chars format
                el = el[:1993]
                el = el[:el.rfind('.') + 1]
            await ctx.send("\n" + "```" + el + "```")  # send word
            # await say(ctx)
            print(f"{h.timestamp()} Word found\n" + el)

# headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
#     }

# @commands.command()
# async def headers(ctx):
#     print(type(headers))


@commands.command()
async def dicti(ctx, *arg):
    if len(arg) == 0:  # no arguments in tuple
        print(f"{h.timestamp()} Args not provided")
        await ctx.send("```No argument\nUsage: /dict word(or words separated by space)```")
        return
    arg = "-".join(arg)
    if arg.find("-"):
        expression = True
    else:
        expression = False
    print(f"{h.timestamp()} Searching for word/expression {arg}")
    async with ctx.typing():
        url_search = "https://dictionary.cambridge.org/dictionary/english/" + arg
        print("Searching in " + url_search)
        page_search = requests.get(url_search, headers=headers)
        soup_search = BeautifulSoup(page_search.content, "html.parser")  # parse found page
        res = soup_search.find("h1", class_="ti fs fs12 lmb-0 hw superentry")
        if res is None:
            print("Not found")
            return
        if expression:
            definition = soup_search.find("div", class_="def ddef_d db").text
            example = soup_search.find("div", class_="examp dexamp").text
            print(definition + '\n•' + example)
            await ctx.send(f"```{definition}\n•{example}```")
        else:
            wordtype = soup_search.find("h3", class_="dsense_h").text
            definition = soup_search.find("div", class_="ddef_h").text
            print(wordtype + '\n•' + definition)


async def setup(bot):
    bot.add_command(dex)
    bot.add_command(dicti)
    # bot.add_command(headers)
