import asyncio
import time

async def prepare_meat(meat_type):
  print(f"Cooking meat: {meat_type}")
  await asyncio.sleep(3)
  print(f"Done cooking meat: {meat_type}")

async def add_extra(extra):
  print(f"Adding extra: {extra}")
  await asyncio.sleep(1)
  print(f"Done add extra: {extra}")

async def chef(order):
  print(f"Cocinando la carne del pedido: { order }")
  await prepare_meat(order[0])
  print(f"Añadiendo el extra del pedido: { order }")
  await add_extra(order[1])
  return

async def main():
  orders =[['burger', 'cheese'],
        ['chicken burger', 'pickles'],
        ['veggie burger', 'cheese']]

  #await asyncio.gather(*(chef(order) for order in orders))

  tasks = []
  for order in orders:
    task = asyncio.create_task(chef(order))
    tasks.append(task)
  await asyncio.gather(*tasks)

  #Crear tareas

start_time = time.time()
asyncio.run(main())
print(f"Total time = {time.time() - start_time}")