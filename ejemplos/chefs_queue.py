import asyncio
import time

async def prepare_meat(meat):
  print(f"cocinando carne: {meat}")
  await asyncio.sleep(3)
  print(f"terminando de cocinar carne: {meat}")

async def add_extra(extra):
  print(f"añadiendo extra: {extra}")
  await asyncio.sleep(1)
  print(f"terminando de añadir el extra: {extra}")

async def chef(id, queue):
  while True:
    order = await queue.get()
    print(f"Chef {id} cocinando el pedido {order}")
    await prepare_meat(order[0])
    await add_extra(order[1])
    print(f"Chef {id} finalizando pedido {order}")
    queue.task_done()
  return

async def client(id, queue):
  orders =[[f'burger{id}', f'cheese{id}'],
          [f'chicken burger{id}', f'pickles{id}'],
          [f'veggie burger{id}', f'cheese{id}']]

  for order in orders:
    await queue.put(order)

async def main():

  queue = asyncio.Queue()

  num_clients = 20
  num_chefs = 3

  clients = []
  for id in range(num_clients):
    task = asyncio.create_task(client(id, queue))
    clients.append(task)

  chefs = []
  for id in range(num_chefs):
    task = asyncio.create_task(chef(id, queue))
    chefs.append(task)

  await asyncio.gather(*clients) 
  await queue.join()
  

start_time = time.time()
asyncio.run(main())
print(time.time()-start_time)