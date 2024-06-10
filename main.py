import pyaudio
import wave


def list_audio_devices():
    p = pyaudio.PyAudio()
    for i in range(p.get_device_count()):
        info = p.get_device_info_by_index(i)
        if info["maxOutputChannels"] > 0:
            if True or "Crusher" in info["name"] or "AirPods" in info["name"]:
                print(
                    f"Device {i}: {info['name']} ({'Input' if info['maxInputChannels'] > 0 else 'Output'})"
                )
    p.terminate()


def play_audio_on_multiple_devices(
    chunk_size=1024,
    output_device1_index=10,
    output_device2_index=12,
    input_device_index=4,
    channels=2,
    rate=48000,
    format=pyaudio.paInt32,
):
    p = pyaudio.PyAudio()

    input_stream = p.open(
        format=format,
        channels=channels,
        rate=rate,
        input=True,
        input_device_index=input_device_index,
        frames_per_buffer=chunk_size,
    )

    output_stream2 = p.open(
        format=format,
        channels=channels,
        rate=rate,
        output=True,
        output_device_index=output_device2_index,
    )

    output_stream1 = p.open(
        format=format,
        channels=channels,
        rate=rate,
        output=True,
        output_device_index=output_device1_index,
    )

    try:
        while True:
            data = input_stream.read(chunk_size)
            output_stream2.write(data)
            output_stream1.write(data)

    except KeyboardInterrupt:
        print("Streaming stopped.")

    input_stream.stop_stream()
    input_stream.close()
    output_stream1.stop_stream()
    output_stream1.close()
    output_stream2.stop_stream()
    output_stream2.close()

    p.terminate()


list_audio_devices()
play_audio_on_multiple_devices()
