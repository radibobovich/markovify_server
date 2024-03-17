import asyncio
import json
import websockets
import markovify

text_model = None

max_dataset_length = 10000

file_name = 'lr.txt'


def load_model():
    with open(file_name, encoding='utf-8') as f:
        text = f.read()
    global text_model
    text_model = markovify.Text(text, state_size=2)


async def echo(websocket):
    while True:
        message = await websocket.recv()
        data = json.loads(message)
        if data['command'] == 'save':
            save_to_dataset(data['text'])
            load_model()
            print('Saved to dataset')
        # model is Generation
        elif data['command'] == 'generate':
            global text_model
            sentence = text_model.make_sentence(tries=20)
            if sentence is None:
                print('Failed to generate sentence')
                continue
            response = json.dumps({'command': 'generate', 'text': sentence})
            await websocket.send(response)


# if dataset length > 1000, remove from start as many lines as added
def save_to_dataset(text):
    text_lines_count = len(text.split('\n'))
    with open(file_name, "a", encoding='utf-8') as f:
        f.write(text + '\n')
    with open(file_name, "r", encoding='utf-8') as f:
        lines = f.readlines()
        print(f'Dataset length: {len(lines)}')
    if len(lines) > max_dataset_length:
        print(f'''Dataset is too big,
               removing {text_lines_count} lines from start''')
        with open(file_name, "w", encoding='utf-8') as f:
            f.writelines(lines[text_lines_count:])


async def main():
    global text_model
    load_model()
    # print(text_model.
    #       make_sentence_with_start(beginning='А', strict=False))
    server = await websockets.serve(
        echo, "127.0.0.1", 8765, ping_interval=0, ping_timeout=None)
    print(text_model.make_sentence(tries=10))
    host = server.sockets[0].getsockname()[0]
    port = server.sockets[0].getsockname()[1]
    # Выводим информацию о запущенном сервере
    print(f"Сервер запущен по адресу ws://{host}:{port}")

    await asyncio.Future()

# Запускаем цикл событий asyncio
asyncio.run(main())
