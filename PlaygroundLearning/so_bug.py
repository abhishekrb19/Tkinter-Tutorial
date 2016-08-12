from multiprocessing import Process, Queue

def f(q):
    #q.put([42, None, 'hello'])
    print "nopo"


if __name__ == '__main__':
    q = Queue()
    p = Process(target=f, args=(q,))
    p.start()
    try:
        # print q.get(block =False)    # prints "[42, None, 'hello']"
        print q.get(block=False)
    except:
        print "empty q"
    p.join()