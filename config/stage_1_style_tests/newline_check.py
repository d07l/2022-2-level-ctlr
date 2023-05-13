"""
Checks newline at the end
"""
import sys

from config.test_params import PROJECT_ROOT


def get_paths() -> list:
    """
    Returns list of paths to non-python files
    """
    paths_to_exclude = [
        'venv',
        '.git',
        '.idea'
    ]
    list_with_paths = []
    for file in PROJECT_ROOT.iterdir():
        if file.name not in paths_to_exclude and file.is_dir():
            list_with_paths.extend(sorted(file.rglob('*')))
        else:
            list_with_paths.append(file)
    return list_with_paths


def check_paths(list_with_paths: list):
    """
    Checks if the path is correct
    """
    paths_to_exclude = [
        '1_raw.txt',
        '__init__.cpython-310.pyc',
        'test_params.cpython-310.pyc'
    ]
    paths = []
    for path in list_with_paths:
        if path.stat().st_size != 0 and path.is_file() and \
                path.name not in paths_to_exclude and \
                path.suffix != '.png':
            paths.append(path)
    return paths


def has_newline(paths: list) -> bool:
    """
    Checks for a newline at the end
    """
    for path in paths:
        with open(path, encoding='utf-8') as file:
            lines = file.readlines()
        if lines[-1][-1] != '\n':
            print(f'No newline at the end of the {path} file')
            return False
    print('All files conform to the template.')
    return True


def main():
    """
    Entrypoint for module
    """
    list_with_paths = get_paths()
    paths = check_paths(list_with_paths)
    sys.exit(not has_newline(paths))


if __name__ == '__main__':
    main()
