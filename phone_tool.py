import threading
import queue
import sys, getopt


def get_option(argv):
    global pre_number, save_file, thread_num

    opts, args = getopt.getopt(argv, "hi:o:t:", ["help", "input=", "output=", "thread="])
    for opt, arg in opts:
        if opt in ["-h", "--help"]:
            print("\n\t手机尾号遍历小工具V1.0\n")
            print("\t-i\t前数位固定数字，例：-i 1300610 或 --input=1300610")
            print("\t-o\t输出文件，例：-o wuhan.txt 或 --output=wuhan.txt")
            print("\t-t\t写入线程，默认10线程，例：-t 12 或 --thread=12\n")
            sys.exit()
        elif opt in ["-i", "--input"]:
            pre_number = arg
        elif opt in ["-o", "--output"]:
            save_file = arg
        elif opt in ["-t", "--thread"]:
            thread_num = int(arg)

def save_phone():
    while not q.empty():
        tail = str(q.get())

        tail_number = pre_number + tail.zfill(tail_length)
        with open(file=save_file, mode="a") as f:
            f.writelines(tail_number + "\n")


if __name__ == '__main__':

    pre_number = ''
    save_file = ''
    thread_num = 10

    get_option(sys.argv[1:])

    tail_length = 11 - len(pre_number)
    tail_count = 10**tail_length    # 尾号数量，7未则10000

    q = queue.Queue()
    for tail in range(tail_count):
        q.put(tail)

    for i in range(thread_num):
        t = threading.Thread(target=save_phone, )
        t.start()
