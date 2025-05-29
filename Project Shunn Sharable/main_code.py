from multiprocessing import Process, freeze_support, set_start_method
import om
import webSpeech_backend
import time

def start_assistant():
    om.taskexection()

def start_flask():
    webSpeech_backend.run_flask()

if __name__ == '__main__':
    freeze_support()
    set_start_method('spawn', force=True)

    print("Starting assistant and speech server...")

    p1 = Process(target=start_assistant)
    p2 = Process(target=start_flask)

    p1.start()
    time.sleep(2)
    p2.start()

    try:
        p1.join()
        p2.join()
    except KeyboardInterrupt:
        print("Shutting down...")
        p1.terminate()
        p2.terminate()
