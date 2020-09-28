# EU-Economy-Bot
This is an economy bot for the EU discord server, but its
features are so flexible as to be applicable to any economy or roleplay discord server.





# Inspiration

I wanted a Purely Economic bot for my EU simulator server. I tried to use premade bots, such as tip.cc or unbelieveabot, but they did not suit my criterion. For each I found that many bots rely too much on gambling and games, which I did not want in the EU server. Thus I decided to build a new bot that purely focuses on economics without any games.
This bot focuses on flexability and freedom, allowing
members and admins to bring the most customizability to any discord server.

# Commands list

- $prune - delete all wallets that no longer exist
- $ping - The ping command. Tests server lag
- $print - add an amount of money to an account
- $graph - graph the money over time of an account
- $set-wallet-settings - change settings of a wallet
- $oldhelp - gives a list of old commands from old version
- $set-money - set the amount of money
- $info - gives info on a secpfic command
- $set-money-each - set the amount of money of each person who satisfies a condition
- $links - Show relevant links to this bot
- $add-smart-contract - add a new smart contract
- $all-commands - gives a list of all implemented commands
- $clear-contracts - delete all your smart contracts
- $insert-trade - put a new trade on the market
- $whois - see who satisifies a given condition
- $accept-trade - put a new trade on the market
- $view-market - see all trades on the market right now
- $work - gain an amount of money
- $delete-all-trades - delete all trades currently on the market
- $work-conditional - allow admins to set different work amounts for different roles
- $inspect-trade - get info on a trade
- $quiz - take a quiz for a cash prize
- $see-work-levels - look at all work levels
- $set-config - allow admins to change the server settings
- $balance - get the balance in an account
- $send - send an ammount of money
- $delete work level - delete a work level by name
- $view-config - see what the current server config is
- $send-each - send each person an ammount of money



# Wallets explained

Wallets are where money is stored. Each person has a personal wallet
and each roles has a communal wallet. Anyone with the role can access the role wallet.
People with the role "taxation" can access any wallet below them in the role heirarchy.

# Smart Contracts

What makes this bot unique from other economy bots is the ability for users to create their own smart-contracts based on events on the server.

Currently the only event supported is messaging. So a user can send money to another user based on content found in a message. Here is an example:

(run the command below in a channel)
$add-smart-contract message

Then add this code:

    if message.content == "I want some money!":
        send("@eulerthedestroyer", message.author.mention, "1")
        output = "I just sent you 1 through a smart contract"

This smart contract will send $1 from @eulerthedestroyer to the person who sent the message that matches the text "I want some money!". Each person can only have 3 smart contracts, and if a smart contract encounters an error, then it is automatically annulled.


# Alternate currencies/items

If your server wants multiple currencies or items to be supported, then we have you covered. Add a - and the name of the currency
afterwards, as an example, $set-balance @euler 1-peso will set the peso balance of me to 1.


# Conditions
Commands such as send-each use conditions to allow you to send to each person who satisfies a condition. 
The currently availiable keywords for conditions are `not, and, or, everyone, online, offline, bot`.
You can see which people satisfy a condition with whois.


# Invite link

You can invite this bot to any server with the link https://discord.com/api/oauth2/authorize?client_id=716434826151854111&permissions=268503104&scope=bot
