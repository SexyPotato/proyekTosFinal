from random import randint
import getpass
import string
import sqlite3

def token_generator():
  alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
  num = "123456789"
  token = ""
  for n in range(6):
    switch = randint(0,2)
    if switch == 0:
      token += alpha[randint(0, len(alpha))]
    else:
      token += num[randint(0, len(num)-1)]
  return token

def play(username):
  class Character:
    def __init__(self):
      self.name = ""
      self.health = 1
      self.health_max = 1
    def do_damage(self, enemy):
      damage = min(
          max(randint(0, self.health) - randint(0, enemy.health), 0),
          enemy.health)
      enemy.health = enemy.health - damage
      if damage == 0: print "%s evades %s's attack." % (enemy.name, self.name)
      else: print "%s hurts %s!" % (self.name, enemy.name)
      return enemy.health <= 0

  class Enemy(Character):
    def __init__(self, player):
      Character.__init__(self)
      self.name = 'a goblin'
      self.health = randint(1, player.health)

  class Player(Character):
    def __init__(self):
      Character.__init__(self)
      self.state = 'normal'
      self.health = 10
      self.health_max = 10
    def quit(self):
      print "%s can't find the way back home, and dies of starvation.\nR.I.P." % self.name
      self.health = 0
    def help(self): print Commands.keys()
    def status(self): print "%s's health: %d/%d" % (self.name, self.health, self.health_max)
    def tired(self):
      print "%s feels tired." % self.name
      self.health = max(1, self.health - 1)
    def rest(self):
      if self.state != 'normal': print "%s can't rest now!" % self.name; self.enemy_attacks()
      else:
        print "%s rests." % self.name
        if randint(0, 1):
          self.enemy = Enemy(self)
          print "%s is rudely awakened by %s!" % (self.name, self.enemy.name)
          self.state = 'fight'
          self.enemy_attacks()
        else:
          if self.health < self.health_max:
            self.health = self.health + 1
          else: print "%s slept too much." % self.name; self.health = self.health - 1
    def explore(self):
      if self.state != 'normal':
        print "%s is too busy right now!" % self.name
        self.enemy_attacks()
      else:
        print "%s explores a twisty passage." % self.name
        if randint(0, 1):
          self.enemy = Enemy(self)
          print "%s encounters %s!" % (self.name, self.enemy.name)
          self.state = 'fight'
        else:
          if randint(0, 1): self.tired()
    def flee(self):
      if self.state != 'fight': print "%s runs in circles for a while." % self.name; self.tired()
      else:
        if randint(1, self.health + 5) > randint(1, self.enemy.health):
          print "%s flees from %s." % (self.name, self.enemy.name)
          self.enemy = None
          self.state = 'normal'
        else: print "%s couldn't escape from %s!" % (self.name, self.enemy.name); self.enemy_attacks()
    def attack(self):
      if self.state != 'fight': print "%s swats the air, without notable results." % self.name; self.tired()
      else:
        if self.do_damage(self.enemy):
          print "%s executes %s!" % (self.name, self.enemy.name)
          self.enemy = None
          self.state = 'normal'
          if randint(0, self.health) < 10:
            self.health = self.health + 1
            self.health_max = self.health_max + 1
            print "%s feels stronger!" % self.name
        else: self.enemy_attacks()
    def enemy_attacks(self):
      if self.enemy.do_damage(self): print "%s was slaughtered by %s!!!\nR.I.P." %(self.name, self.enemy.name)
  Commands = {
    'quit': Player.quit,
    'help': Player.help,
    'status': Player.status,
    'rest': Player.rest,
    'explore': Player.explore,
    'flee': Player.flee,
    'attack': Player.attack,
  }
  p = Player()
  p.name = username
  print "(type help to get a list of actions)\n"
  print "%s enters a dark cave, searching for adventure." % p.name

  while(p.health > 0):
    line = raw_input("> ")
    if len(line) > 0:
      commandFound = False
      for c in Commands.keys():
        if line[0] == c[0]:
          Commands[c](p)
          commandFound = True
          break
      if not commandFound:
        print "%s doesn't understand the suggestion." % p.name
  return 0

def login():
  print "Please login to play game"
  username = raw_input("Username: ")
  password = getpass.getpass("password: ")
  token = raw_input("Authentication Code: ")
  with sqlite3.connect("database.db") as data:
    inp = data.cursor()
    inp.execute("SELECT COUNT(*) FROM users WHERE username = ? AND  password = ? AND token = ?" ,(username, password, token))
    rows = inp.fetchall();
    data.commit()
  data.close()
  return play(username)

def signup():
  print "SIGN UP to play game"
  username = raw_input("Username: ")
  password = getpass.getpass("password: ")
  token = token_generator()
  print "Your Authentication code -> %s" % (token)
  print "Please save it to login to your account!"
  with sqlite3.connect("database.db") as wtf:
    inp = wtf.cursor()
    inp.execute("INSERT INTO users (username, password, token) VALUES (?, ?, ?)",(username, password, token))
    wtf.commit()
    print "You are now registered!!"
  wtf.close()
  return login()

#main program

print "Welcome!!"
while (True):
  opt = raw_input("L for login S for signup X for exit: ")
  opt = opt.upper()
  if opt=='S':
    signup()
  elif opt=='L':
    login()
  elif opt=='X':
    break
  else:
    print "please read again and input the Goddamn option letters only!!"