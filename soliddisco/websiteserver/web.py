from werkzeug.routing import BaseConverter
from flask import Flask
from pathlib import Path


class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super().__init__(url_map)
        self.regex = items[0]


weby = Flask(__name__)
weby.url_map.converters['regex'] = RegexConverter

DATA_DIR = ''

_INDEX_HTML = '''
<html>
    <head>
        <title>Brain Computer Interface</title>
    </head>
    <body>
        <ul>
            {users}
        </ul>
    </body>
</html>
'''

_USER_LINE_HTML = '''
<li><a href="/users/{user_id}">user {user_id}</a></li>
'''

_USER_HTML = '''
<html>
    <head>
        <title>Brain Computer Interface: User {user}</title>
    </head>
    <body>
        <table>
            {thoughts}
        </table>
    </body>
</html>
'''

_USER_THOUGHTS_HTML = '''
<tr>
    <td>{time}</td>
    <td>{thoughts}</td>
</tr>
'''


def run_webserver(address, data_dir):
    global DATA_DIR
    DATA_DIR = str(data_dir)
    host, port = address
    weby.run(host, port, debug=True)


@weby.route('/')
def index():
    global DATA_DIR
    users_html = []
    for user_dir in sorted(list(Path(DATA_DIR).iterdir()), reverse=True):
        users_html.append(_USER_LINE_HTML.format(user_id=user_dir.name))
    index_html = _INDEX_HTML.format(users='\n'.join(users_html))
    return index_html, 200


@weby.route('/users/<regex("[0-9]+"):user_id>')
def user(user_id):
    global DATA_DIR
    users = set(str(p.name) for p in Path(DATA_DIR).iterdir() if p.is_dir())
    if user_id not in users:
        return "Not Foundddd", 404

    display = {}
    user_dir = Path(f"{DATA_DIR}/{user_id}")
    user_files = set()
    for f in user_dir.iterdir():
        if f.is_file():
            user_files.add(f.name.split('.')[0])

    for user_thought in user_files:
        user_thought_path = user_dir / f"{user_thought}.txt"
        day, hour = user_thought.split('_')
        time = ' '.join([day, hour.replace('-', ':')])
        text = ""
        with user_thought_path.open(mode="r") as f:
            text = f.read()
            f.close()
        display[time] = text
    show = []
    for time, thought in sorted(display.items(), reverse=True):
        show.append(_USER_THOUGHTS_HTML.format(time=time, thoughts=thought))
    show_html = _USER_HTML.format(user=user_id, thoughts='\n'.join(show))
    return show_html, 200


# def main(argv):
#     if len(argv) != 3:
#         print(f'USAGE: {argv[0]} <address> <data dir>')
#         return 1
#     try:
#         ip, port = argv[1].split(':')
#         run_webserver((ip, int(port)), argv[2])
#         return 0
#     except Exception as error:
#         print(f'ERROR: {error}')
#         return 1


# if __name__ == '__main__':
#     import sys
#     sys.exit(main(sys.argv))
