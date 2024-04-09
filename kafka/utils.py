def acked(err, msg):
    if err is not None:
        print(f"Failed to deliver message: {msg.value()}: {err.str()}")
    else:
        print(f"Message produced: {msg.value()}")
