import multiprocessing
import threading
import time
import codecs


def get_timestamp():
    """Return string of current time"""
    return time.strftime("%H:%M:%S", time.localtime())


def process_a_func(queue: multiprocessing.Queue, conn_a_to_b):
    """Implementation of process A

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
    """Implementation of process B

    Args:
        conn_b_to_a (PipeConnection): Pipe connection from process B to process A
        conn_b_to_main (PipeConnection): Pipe connection from process B to process Main
    """

    while True:
        message = conn_b_to_a.recv()
        encoded_message = codecs.encode(message, "rot-13")
        conn_b_to_main.send(encoded_message)


def stdout_thread_method(parent_conn_main_to_b, user_exit_event: threading.Event):
    """ Body of Tread for printing received frm B messages"""
    try:
        while not user_exit_event.is_set():
            if parent_conn_main_to_b.poll():
                received_message = parent_conn_main_to_b.recv()
                print(
                    f"\rEncoded message: '{received_message}' received at {get_timestamp()}"
                    + "\nEnter a message: ",
                    end=""
                )
    except KeyboardInterrupt:
        return


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

    user_exit = threading.Event()
    stdout_thread = threading.Thread(
        target=stdout_thread_method, args=(parent_conn_main_to_b, user_exit)
    )
    stdout_thread.start()

    try:
        while True:
            main_message = input("Enter a message: ")
            print(f"Message '{main_message}' was entered at {get_timestamp()}")
            queue_main_to_a.put(main_message)

    except KeyboardInterrupt:
        user_exit.set()
        process_a.terminate()
        process_b.terminate()
        print("Applications stopped")
