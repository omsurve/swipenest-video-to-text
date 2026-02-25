def format_timestamp(seconds):
    millisec = int(seconds * 1000)

    hours = millisec // 3600000
    minutes = (millisec % 3600000) // 60000
    seconds = (millisec % 60000) // 1000
    milliseconds = millisec % 1000

    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"


def generate_srt(chunks, output_path):

    with open(output_path, "w", encoding="utf-8") as f:

        for index, chunk in enumerate(chunks, start=1):

            start, end = chunk["timestamp"]

            if start is None or end is None:
                continue

            start_time = format_timestamp(start)
            end_time = format_timestamp(end)

            text = chunk["text"].strip()

            f.write(f"{index}\n")
            f.write(f"{start_time} --> {end_time}\n")
            f.write(f"{text}\n\n")

    print("✅ SRT file generated!")
