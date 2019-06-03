import threading
import queue
import sys, getopt


def get_option(argv):
    global pre_number, read_file, save_file, thread_num

    opts, args = getopt.getopt(argv, "hp:i:o:t:", ["help", "phone=", "input=", "output=", "thread="])
    for opt, arg in opts:
        if opt in ["-h", "--help"]:
            print("\n\t手机尾号遍历小工具V1.0\n")
            print("\t-p\t前数位固定数字，例：-p 1300610 或 --phone=1300610")
            print("\t-i\t输入号段文件，例：-i read.txt 或 --input=read.txt")
            print("\t-o\t输出文件，例：-o wuhan.txt 或 --output=wuhan.txt")
            print("\t-t\t写入线程，默认10线程，例：-t 12 或 --thread=12\n")
            sys.exit()
        elif opt in ["-p", "--input"]:
            pre_number = arg
        elif opt in ["-i", "--input"]:
            read_file = arg
        elif opt in ["-o", "--output"]:
            save_file = arg
        elif opt in ["-t", "--thread"]:
            thread_num = int(arg)

def read_number(pre_number):

    print("写入%s号段..." % pre_number)

    q = queue.Queue()
    tail_length = 11 - len(pre_number)
    tail_count = 10 ** tail_length  # 尾号数量，7未则10000

    for tail in range(tail_count):
        q.put(tail)

    for i in range(thread_num):
        t = threading.Thread(target=save_phone, args=(q, pre_number, tail_length, ))
        t.start()

def save_phone(q, pre_number, tail_length):
    while not q.empty():
        tail = str(q.get())

        lock.acquire()
        tail_number = pre_number + tail.zfill(tail_length)
        with open(file=save_file, mode="a") as f:
            f.writelines(tail_number + "\n")
        lock.release()


if __name__ == '__main__':

    pre_number = ''
    read_file = ''
    save_file = ''
    thread_num = 10

    get_option(sys.argv[1:])
    lock = threading.Lock()

    if read_file != '':
        f = open(file=read_file, mode="r")
        numbers = f.readlines()
        for i in range(len(numbers)):
            number = numbers[i].strip()

            t = threading.Thread(target=read_number, args=(number, ))
            t.start()
            t.join()
    else:
        read_number(pre_number)

