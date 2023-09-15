import uos


def get_version() -> str:
    if 'version' in uos.listdir():
        with open('version', 'r') as current_version_file:
            return current_version_file.readline().strip()
    return '0.0.1'
