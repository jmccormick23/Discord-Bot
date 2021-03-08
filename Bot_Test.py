import os
import discord
import sqlite3

conn = sqlite3.connect('test.db')
conn.isolation_level = None
client = discord.Client()

#CREATED DATABASE
#conn.execute('''CREATE TABLE MEMBERS
      #(ID              INT      NOT NULL,
      #NAME             TEXT     NOT NULL,
      #LEVEL            INT      NOT NULL,
      #CP               INT,
      #CLASS            CHAR(25))''')
#print ("Table created successfully")

#INSERT USER
#conn.execute("INSERT INTO MEMBERS (ID,NAME,LEVEL,CP,CLASS) \
      #VALUES (229039794787713025, 'Solumn', 125, 5525391, 'Mage')");

#BOOL TO DETERMINE IF A USER ENTERED A VALUE FOR UPDATE
def check(message):
  try:
    int(message.content)
    return True
  except ValueError:
    return False

#DETERMINE IF THE USER HAS INFORMATION STORED IN THE DATABASE OR NOT
#def valid(message):
   #valid = conn.execute("SELECT EXISTS(SELECT * from MEMBERS WHERE id=?)", (message.author.id,))
   #if valid:
    #   bool user = True
  # else:
     #  bool user = False

@client.event
async def on_ready():
    guild_count = 0
  
    for guild in client.guilds:
        print(f"- {guild.id} (name: {guild.name})")

        guild_count = guild_count + 1

    print("Data Bot is in " + str(guild_count) + " servers.")

@client.event
async def on_message(message):
    if message.content.startswith('!show'):
        #DETERMINE IF USER HAS A VALID ENTRY THEN SELECTS USER
        valid = conn.execute("SELECT EXISTS(SELECT * from MEMBERS WHERE id=?)", (message.author.id,))
        valid1 = valid.fetchone()
        validtest = (1,)
        if valid1 == validtest:
            cursor = conn.execute("SELECT * from MEMBERS WHERE id=?", (message.author.id,))
            for row in cursor:
                print(row)
                break

            response = discord.Embed(title=row[1],color=0x3498db)
            response.add_field(name="Level", value=row[2], inline=False)
            response.add_field(name="CP", value=row[3], inline=False)
            response.add_field(name="Class", value=row[4], inline=False)

            print(valid)
            await message.channel.send(embed=response)
        else:
            await message.channel.send("You have no recorded data, please contact a moderator to assist you.")

    if message.content.startswith('!updatecp'):
        valid = conn.execute("SELECT EXISTS(SELECT * from MEMBERS WHERE id=?)", (message.author.id,))
        valid1 = valid.fetchone()
        validtest = (1,)
        if valid1 == validtest:
            await message.channel.send('Enter your CP')
            cp = await client.wait_for('message', timeout = 60, check=check)
            attempt = int(cp.content)
            cursor = conn.execute("UPDATE MEMBERS SET cp=? WHERE id=?", (int(attempt), message.author.id))
            await message.channel.send("CP Updated Successfully")
        else:
            await message.channel.send("You have no recorded data, please contact a moderator to assist you.")

    if message.content.startswith('!updatelevel'):
        valid = conn.execute("SELECT EXISTS(SELECT * from MEMBERS WHERE id=?)", (message.author.id,))
        valid1 = valid.fetchone()
        validtest = (1,)
        if valid1 == validtest:
            await message.channel.send("Enter your Level")
            lvl = await client.wait_for('message',timeout = 60, check=check)
            attempt = int(lvl.content)
            cursor = conn.execute("UPDATE MEMBERS SET LEVEL=? WHERE id=?", (attempt, message.author.id)) 
            await message.channel.send("Level Updated Successfully")
        else:
            await message.channel.send("You have no recorded data, please contact a moderator to assist you.")


    if message.content.startswith('!help'):

      response = discord.Embed(title='Bot Commands',color=0x3498db)
      response.add_field(name="!updatecp", value='Allows you to adjust your CP', inline=False)
      response.add_field(name="!updatelevel", value='Allows you to adjust your level', inline=False)
      response.add_field(name="!show", value='Shows you your character data', inline=False)
      response.add_field(name="!delete", value='Deletes your character data (Please be careful)', inline=False)

      await message.channel.send(embed=response)

    if message.content.startswith('!delete'):
      await message.channel.send("Are you sure you want to delete all of your character data?(yes/no)")
      delete = await client.wait_for('message',timeout = 60)
      if delete.content.startswith('y' or 'Y'):
        print('this got here')
        cursor = conn.execute("DELETE from MEMBERS WHERE id=?", (message.author.id,))


from dotenv import load_dotenv
load_dotenv()

client.run(os.getenv('TOKEN'))
