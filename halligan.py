#!/usr/bin/env python3

from asyncio import get_event_loop
from argparse import ArgumentParser
from os import system, getcwd
from concurrent.futures import ProcessPoolExecutor
from requests import session


class Halligan:

    def __init__(self):
        self.dir_list = ""
        self.url = ""

    def exceptor(self, method_name: str, exception: Exception):
        try:
            print("Error! in " + method_name + ": " + str(exception))
            pass
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
                if len(user_input) < 100:
                    for b in black_list:
                        if b in user_input:
                            print("Input contains inappropriate characters.")
                            raise Exception
                        else:
                            continue
                    return True
                else:
                    print("Input is too large.")
                    raise Exception
            else:
                print("validator received no input.")
                raise Exception
        except Exception as e:
            print("Validation Error!" + str(e))
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


    def read_file(self):
        try:
            with open(self.dir_list, "r") as file:
                return [f for f in file.readlines()]
        except Exception as e:
            self.exceptor("Error in read_file: ", e)


    async def writer(self, lines):
        try:
            path = getcwd() + "/halligan_temp.log"
            with open(path, "a") as file:
                file.writelines(lines)
        except Exception as e:
            self.exceptor("writer", e)


    async def process_response(self, response, url:str):
        try:
            print(url)
            if response == 200:
                print("\nPath Discovered: " + url + "\n")
                await self.writer("Path Discovered: " + url + "\n")
        except Exception as e:
            self.exceptor("process_response", e)


    def send_http_request(self, url):
        try:
            loop = get_event_loop()
            with session().get(url) as res:
                task = loop.create_task(self.process_response(res.status_code, url))
                loop.run_until_complete(task)
        except Exception as e:
            self.exceptor("send_http_request", e)


    def pre_run(self):
        try:
            self.clear_screen()
            self.bruce()
            self.get_args()
            with open(getcwd() + "/halligan_temp.log", "w") as file:
                file.close()
        except Exception as e:
            self.exceptor("pre_run", e)


    def get_found(self):
        with open(getcwd() + "/halligan_temp.log", "r") as file:
            lines = file.readlines()
            return lines


    def controller(self):
        try:
            self.pre_run()
            base = self.url
            urls = [d for d in self.read_file()]
            clean_urls = []
            apd = clean_urls.append
            for u in urls:
                if u.startswith("/"):
                    apd(u)
                else:
                    apd("/" + u)
            clean_urls = [d.rstrip("\n") for d in clean_urls]
            urls = [base + d for d in clean_urls]
            procs = 512
            with ProcessPoolExecutor(procs) as pool:
                pool.map(self.send_http_request, urls)
            found = self.get_found()
            if found:
                print("\nLegitimate Paths Discovered")
                print("----------------------------")
                [print(x) for x in found]
            else:
                print("\nNo Legitimate Paths Discovered..")
        except Exception as e:
            self.exceptor("controller", e)


def main():
    Halligan().controller()

if __name__ == '__main__':
    main()
