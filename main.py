import requests, threading, json, time, os, sys, random
from colorama import init, Fore

class Generator:
  def __init__(self, tokens, username, delay):
    self.lock = threading.Lock()
    self.tokens = tokens
    self.delay = delay
    self.enumerator = range(10000)
    
  def __iter__(self):
    return self.enumerator.__iter__()
  
  def next(self):
    try:
      self.lock.acquire()
      return next(self.enumerator)
    finally:
      self.lock.release()
    
found = False
username = None

def worker(generator):
  global found, username
  
  for discriminator in generator:
    if found:
      break
      
    if discriminator % 10 == 0 and discriminator > 0: # Print status every 10th attempt
      print(f'Current attempt: {discriminator}')
    
    data = {
      'username': generator.username,
      'discriminator': str(discriminator)
    }
    
    headers = {
      'authorization': random.choice(generator.tokens),
      'content-type': 'application/json'
    }
    
    data = {'username': username, 'discriminator': str(discriminator)}
    r = requests.post('https://discord.com/api/v9/users/@me/relationships', data=json.dumps(data), headers=headers)
    if r.status_code == 204:
      print(f'Found user: {username}#{discriminator}')
      found = False
      
    time.sleep(generator.delay)

def main():
  amount = input('Thread amount: ')
  if not amount.isnumeric():
    print('Thread amount is not a integer.')
    sys.exit(1)
  
  delay = input('Delay per thread (ms): ')
  if not amount.isnumeric():
    print(f'Delay is not a integer.')
    sys.exit(1)

  token_path = input('Token list: ')
  if not os.path.exists(token_path):
    print('Token file does not exist.')
    sys.exit(1)
  
  username = input('Username: ')
  
  with open(token_path, 'r') as f:
    
    tokens = f.read().split('\n')
    generator = Generator(tokens, username, delay)
  
    threads = []
    for tid in range(int(amount)):
        thread = threading.Thread(target=worker, args=(generator))
        thread.start()
        threads.append(thread)
      
    for thread in threads:
      thread.join()

if __name__ == '__main__':
  main()
