
import multiprocessing
import time
import codecs

def get_timestamp():
    """ Return string of current time """
    return time.strftime("%H:%M:%S", time.localtime())

def process_a_func(queue: multiprocessing.Queue, conn_a_to_b):
    """ Implementation of process A 

    Args:
        queue (multiprocessing.Queue): Queue from Main process to A process
        conn_a_to_b (PipeConnection): Pipe connection from process A to process B
    """
    while True:
        message: str = queue.get()
        message = message.lower()
        conn_a_to_b.send(message)
        time.sleep(5)

def process_b_func(conn_b_to_a, conn_b_to_main):
    """ Implementation of process B

    Args:
        conn_b_to_a (PipeConnection): Pipe connection from process B to process A
        conn_b_to_main (PipeConnection): Pipe connection from process B to process Main
    """

    while True:
        message = conn_b_to_a.recv()
        encoded_message = codecs.encode(message, "rot-13")
        conn_b_to_main.send(encoded_message)


if __name__ == "__main__":

    queue_main_to_a = multiprocessing.Queue()

    parent_conn_main_to_b, child_conn_b_to_main = multiprocessing.Pipe()
    parent_conn_b_to_a, child_conn_a_to_b = multiprocessing.Pipe()

    process_a = multiprocessing.Process(
        target=process_a_func, args=(queue_main_to_a, child_conn_a_to_b)
    )
    process_a.start()

    process_b = multiprocessing.Process(
        target=process_b_func, args=(parent_conn_b_to_a, child_conn_b_to_main)
    )
    process_b.start()

    try:
        while True:
            main_message = input("Enter a message: ")
            print(
                f"Message '{main_message}' was entered at {get_timestamp()}"
            )

            queue_main_to_a.put(main_message)
            received_message = parent_conn_main_to_b.recv()
            print(
                f"Encoded message: '{received_message}' received at {get_timestamp()}"
            )

    except KeyboardInterrupt:
        process_a.terminate()
        process_b.terminate()
        print("Applications stopped")
