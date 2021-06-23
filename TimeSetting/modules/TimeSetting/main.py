# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for
# full license information.

import time
import os
import sys
import asyncio
from six.moves import input

import logging

async def main():
    try:
        if not sys.version >= "3.5.3":
            raise Exception( "The sample requires python 3.5.3+. Current version of Python: %s" % sys.version )
        print ( "IoT Hub Client for Python" )

        # 로그 설정
        root_logging = logging.getLogger()
        # 로그 레벌 셋팅 : CRITICAL(50), ERROR(40), WARNING(3), INFO(20), DEBUG(10), NOTSET(0)
        root_logging.setLevel(logging.INFO)
        # 로그 포맷 설정
        formatter = logging.Formatter('[%(asctime)s] - %(name)s - %(levelname)s - %(message)s')
        
        # 스트림 로그
        stream_hander = logging.StreamHandler()
        stream_hander.setFormatter(formatter)
        root_logging.addHandler(stream_hander)

        # define behavior for receiving an input message on input1
        async def input1_listener():
            while True:
                logging.info("Time!")
                time.sleep(1)

        # define behavior for halting the application
        def stdin_listener():
            while True:
                try:
                    selection = input("Press Q to quit\n")
                    if selection == "Q" or selection == "q":
                        print("Quitting...")
                        break
                except:
                    time.sleep(10)

        # Schedule task for C2D Listener
        listeners = asyncio.gather(input1_listener())

        print ( "The sample is now waiting for messages. ")

        # Run the stdin listener in the event loop
        loop = asyncio.get_event_loop()
        user_finished = loop.run_in_executor(None, stdin_listener)

        # Wait for user to indicate they are done listening for messages
        await user_finished

        # Cancel listening
        listeners.cancel()

    except Exception as e:
        print ( "Unexpected error %s " % e )
        raise

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
