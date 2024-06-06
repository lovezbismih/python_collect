# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
import os
import asyncio

def test():
    """
    docstring
    """
    add_h = input("input HH:")
    add_m = input("input mm:")
    add_s = input("input ss:")
    i_msg = input("input msg:")

    if i_msg == "":
        i_msg = "game is over"

    if add_h == "":
        add_h = 0

    if add_m == "":
        add_m = 0

    if add_s == "":
        add_s = 0

    i_time = datetime.now()
    init_h = i_time.hour
    init_m = i_time.minute
    init_s = i_time.second
    print(f"{init_h}:{init_m}:{init_s}")

    delta = i_time + timedelta(hours=int(add_h), minutes=int(add_m), seconds=int(add_s))
    print(f"{delta.hour}:{delta.minute}:{delta.second}")
    asyncio.run(display_date(delta))
    os.system(f"msg * /time 3600 {i_msg}")

async def display_date(delta):
    """
    docstring
    """
    while True:
        run_time = datetime.now()
        print(f"{run_time.strftime('%X')}-{delta.hour}:{delta.minute}:{delta.second}")
        if run_time >= delta:
            break
        await asyncio.sleep(1)

if __name__ == "__main__":
    test()
