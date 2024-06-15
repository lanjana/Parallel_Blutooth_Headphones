import pyaudio
import wave


def list_audio_devices():
    p = pyaudio.PyAudio()
    inp_device = "VB-Audio"
    out_device_1 = "Crusher ANC"
    out_device_2 = "AirPods"
    out_device_3 = "OneOdio"

    out_devices = []
    inp_device_ind = 0

    for i in range(p.get_device_count()):
        info = p.get_device_info_by_index(i)

        if info["maxOutputChannels"] > 0:
            if out_device_1 in info["name"]:
                out_devices.append(i)
                out_device_1 = "######"
            if out_device_2 in info["name"]:
                out_devices.append(i)
                out_device_2 = "######"
            if out_device_3 in info["name"]:
                out_devices.append(i)
                out_device_3 = "######"

            print(
                f"Device {i}: {info['name']} ({'Input' if info['maxInputChannels'] > 0 else 'Output'})"
            )

        if inp_device_ind == 0 and info["maxInputChannels"] > 0:
            if inp_device in info["name"]:
                inp_device_ind = i

    p.terminate()

    print(out_devices)
    return out_devices, inp_device_ind


def play_audio_on_multiple_devices(
    out_devices,
    inp_device_ind,
    chunk_size=1024,
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
        input_device_index=inp_device_ind,
        frames_per_buffer=chunk_size,
    )

    out_streams = []
    for i in out_devices:
        try:
            out_streams.append(
                p.open(
                    format=format,
                    channels=channels,
                    rate=rate,
                    output=True,
                    output_device_index=i,
                )
            )
        except Exception as e:
            print(e)
            continue

    try:
        while True:
            data = input_stream.read(chunk_size)
            for stream in out_streams:
                stream.write(data)

    except KeyboardInterrupt:
        print("Streaming stopped.")

    input_stream.stop_stream()
    input_stream.close()

    for stream in out_streams:
        stream.stop_stream()
        stream.close()

    p.terminate()


out_devices, inp_device_ind = list_audio_devices()
play_audio_on_multiple_devices(out_devices, inp_device_ind)
