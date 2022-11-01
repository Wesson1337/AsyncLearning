import asyncio
import threading
import time

# start = time.time()
# threads = []
# for i in range(10):
#     thread = threading.Thread(target=time.sleep, args=(3,))
#     thread.start()
#     threads.append(thread)
#
# for thread in threads:
#     thread.join()
#
#
# print(threads)
# print(time.time() - start)


async def sleep(sec):
    await asyncio.sleep(sec)
    print('done')


async def main():
    tasks = []

    for i in range(10):
        task = asyncio.create_task(sleep(5))
        tasks.append(task)

    for task in tasks:
        await task


if __name__ == '__main__':
    start = time.time()
    asyncio.run(main())
    print(time.time() - start)
