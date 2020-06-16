**DegeneSix**
KatharSys die pool roller bot.

## Dice Rolling
Can be invoked with only the action number
```
!roll 8

@Pabruva rolls: 
 3, 1, 6, 5, 6, 2, 6, 5 
 5 successes, 3 triggers
```
or the action number and the difficulty, separated by a space:
```
!roll 9 3

@Pabruva needs 3 successes and rolls: 
 6, 5, 1, 3, 4, 4, 2, 6, 5 
 6 successes, 2 triggers 
 Success!
```
Counts successes, triggers and checks for botches:
```
!roll 3

@Pabruva rolls: 
 1, 1, 2 
 0 successes, 0 triggers 
 It's a botch!
```
Limits pool to 12 and adds any extra as auto-successes:
```
!roll 24

@Pabruva rolls: 
 6, 5, 5, 1, 6, 6, 3, 3, 1, 6, 4, 6 
 20 successes, 5 triggers
```

## Initiative
DegeneSix can also manage your initiative.
1. Use `start-initiative [label]` to register a game (where the label is optional). This will delete the active initiative in that text channel.
2. Use `!initiative [name] [dice] [ego]` to join (name and ego are optional). Each player can only have one character without a name, and cannot have any characters with duplicate names. This is to prevent confusion.
3. Use `!next` to start the initiative. At the beginning of each round, an overview of the order will be printed, and the first player's turn will begin. 
4. Use `!next` again to move to the next player's turn

The Degenesix initiative feature also has a verbosity feature. Use `!verbose [on/off]` to receive fewer messages.

Example:
```
DM: !start-initiative "My Game"
BOT: Initiative "My Game" started!
     Use !initiative [name] [dice] [ego] (name and ego are optional) to join
     Type !next to start!
@David: !initiative 5
BOT: Player @David was added to the initiative with 5 dice
@Pabruva: !initiative Falberg 6 2
BOT: Player Falberg was added to the initiative with 6 dice and 2 ego
@David: !next
BOT: Starting round 1 of initiative "My Game"...
     Initiative order:
         4:    Falberg
         2:    @David
BOT: 4 successes
     @Pabruva, it is Falberg's turn. You have 2 extra dice for your first action (from ego)
@Pabruva: !next
BOT: 2 successes
     @David, it is your turn. You have 1 extra dice (from triggers)
```
