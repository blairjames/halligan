#!/usr/bin/env python3

from asyncio import get_event_loop
from argparse import ArgumentParser
from aiohttp import ClientSession
from typing import Generator
from os import system
from time import perf_counter as pc


class Halligan:

    def __init__(self):
        self.dir_list = ""
        self.url = ""
        self.executor = get_event_loop().run_in_executor
        self.i = 1
        self.found = []
        self.times = []


    def exceptor(self, method_name: str, exception: Exception):
        try:
            print("Error! in " + method_name + ": " + str(exception))
            exit(1)
        except Exception as e:
            print("Error! in exceptor: " + str(e))


    def get_args(self):
        try:
            args = ArgumentParser()
            add = args.add_argument
            add("url", help="Base URL to which candidate directories are appended.")
            add("directory_list", help="list of candidate directories to be attempted forcefully.")
            inputs = args.parse_args()
            if self.validator(inputs.url) and self.validator(inputs.directory_list):
                self.dir_list = inputs.directory_list
                self.url = ("https://" + inputs.url)
            else:
                raise Exception
        except Exception as e:
            self.exceptor("get_args", e)
            exit(1)


    def validator(self, user_input: str):
        try:
            user_input = str(user_input)
            black_list = ["!","@","#","$","%","^","&","*","(",")","=","+",
                          "[","]","{","}","|",";","\"","\'",",",">","<","?"]
            if user_input:
                if len(user_input) < 39:
                    for b in black_list:
                        if b in user_input:
                            raise Exception
                        else:
                            continue
                    return True
                else:
                    raise Exception
            else:
                print("validator received no input.")
                raise Exception
        except Exception as e:
            print("Validation Error!: " + str(e))
            exit(1)


    def clear_screen(self) -> bool:
        try:
            system("clear")
            return True
        except Exception as e:
            print("Error! in clearscreen: " + str(e))


    def bruce(self):
        print("\n----------------------------------------------------------------------------------")
        print("                                  HALLIGAN    ")
        print("                     Forcefull directory enumeration tool\n")
        print("*A Halligan bar is a forcible entry tool used by firefighters and law enforcement.")
        print("----------------------------------------------------------------------------------\n")


    def read_file(self) -> Generator:
        try:
            with open(self.dir_list, "r") as file:
                return (f for f in file.readlines())
        except Exception as e:
            self.exceptor("Error in read_file: ", e)


    async def process_response(self, response, url, apd):
        try:
            print(str(self.i) + " - " + url)
            if response == 200:
                print("\nPath Discovered: " + url + "\n")
                apd(url)
            self.i += 1
        except Exception as e:
            self.exceptor("process_response", e)


    async def send_http_request(self, url: str, session, apd, timeapd):
        try:
            t1 = pc()
            async with session.get(url) as res:
                await self.process_response(res.status, url, apd)
            t2 = pc()
            timeapd(t2 - t1)
        except Exception as e:
            self.exceptor("send_http_request", e)


    def pre_run(self):
        try:
            self.clear_screen()
            self.bruce()
            self.get_args()
        except Exception as e:
            self.exceptor("pre_run", e)


    async def controller(self):
        try:
            self.pre_run()
            base = self.url
            urls = [(base + d).rstrip("\n") for d in self.read_file()]
            async with ClientSession() as session:
                apd = self.found.append
                timeapd = self.times.append
                [await self.send_http_request(u, session, apd, timeapd) for u in urls]
            if len(self.found) > 0:
                print("\nLegitimate Paths Discovered")
                print("----------------------------")
                [print(x) for x in self.found]
                print("\n")
            else:
                print("No Legitimate Paths Discovered..")
            avg = sum(self.times) / len(self.times)
            print("Average Request Time: " + str(avg))
        except Exception as e:
            self.exceptor("controller", e)


def main():
    loop = get_event_loop()
    loop.run_until_complete(loop.create_task(Halligan().controller()))


if __name__ == '__main__':
    main()
