**DegeneSix**
KatharSys die pool roller bot.
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
