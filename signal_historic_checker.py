from multiprocessing import Process, Queue

import data_loader
import diff_checker
from diff_checker import logger, values,commiter,commits

sender = []


def main():
    if __name__ != '__main__':
        return
    logger.debug('starting the work -- ')
    if diff_checker.typeof == "historical":
        process_create_start()
    elif diff_checker.typeof == "live":
        diff_checker.main(None)
    else:
        print("You haven't entered the appropriate type")

# TODO Rename this here and in `main`


def process_create_start():
    download_data, files = data_loader.main_data_load()
    division = download_data.data_distribution(values['estimate'])
    process_of_diff_checker = []
    process_of_data_sender = []
    tmp1 = 0
    for process in division:
        sender.append(Queue())
        process_of_diff_checker.append(
            Process(target=diff_checker.main, args=(sender[tmp1],)))
        process_of_data_sender.append(
            Process(target=download_data.send_data, args=(process, sender[tmp1],)))
        process_of_diff_checker[tmp1].start()
        process_of_data_sender[tmp1].start()
        tmp1 += 1
    commiter_process = Process(target=commiter, args=())
    commiter_process.start()
    for i in range(tmp1):
        process_of_data_sender[i].join()
        process_of_diff_checker[i].join()


main()
