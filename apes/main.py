import os
from os import path

import logging
logger = logging.getLogger(__name__)


class dataio:
    """
    Base class for data IO.
    The rootpath can be modified by method rootset and rootappend.
    """

    def __init__(self):
        proj = 'eeq'
        file_path = os.path.abspath(os.curdir)
        pos = file_path.find(proj) + len(proj)
        proj_path = file_path[:pos]
        self.rootpath = proj_path

    def rootset(self, root):
        self.rootpath = root

    def rootappend(self, root):
        self.rootpath = os.path.join(self.rootpath, root)

    def save(self, df, name, type='csv',
             file_path='', relative=False):
        """
        Save pandas.Dataframe to CSV file.
        Parameters
        ----------
        df: pandas.DataFrame
            Dataframe to be saved.
        type: str
            File format
        name: str
            Saved file name, no suffix is requried.
        file_path: str
            Saved path, if no path is given, the file will be saved in the rootpath.
        relative_path: bool
            If True, relative_path will be appended to rootpath as the full path.
        """
        # check relative path
        fullpath = os.path.join(self.rootpath, file_path)
        if not relative:
            fullpath = file_path

        # check end character
        if not fullpath.endswith('/'):
            fullpath += '/'

        # check file format
        # TODO: Add type_dict here to suppor more format
        # if input file name has format postfix, remove it
        if not name.endswith('.csv'):
            name += '.' + type

        full = os.path.join(fullpath, name)
        if path.exists(full):
            msg = f'Overwritten: {name} already exists in:\n{fullpath}'
        else:
            msg = f'Successful: {name} in:\nf{fullpath}'
        df.to_csv(full, index=False)
        logger.warning(msg)
        return True

    def find(self, name, type='csv', file_path=''):
        """
        Find file directory.
        Parameters
        ----------
        name: str
            File name, no suffix is requried.
        type: str
            File format
        file_path: str
            Path to search, if no path is given, the file will be searched in the rootpath.
        """
        # -- check file path
        if not file_path:
            file_path = self.rootpath

        # -- check file format
        # TODO: Add type_dict here to suppor more format

        # if input file name has format postfix, remove it
        if not name.endswith(type):
            name += '.' + type

        all_dir = []
        # Wlaking top-down from the root
        for root, dir, files in os.walk(file_path):
            if name in files:
                all_dir.append(os.path.join(root, name))

        if len(all_dir) > 1:
            msg = f'{name} exists in multiple directories, first one will be used.'
            result = all_dir[0]
        elif len(all_dir) == 1:
            msg = f'{name} exists as\n{all_dir[0]}'
            result = all_dir[0]
        else:
            msg = f'{name} is not found!'
            result = False
        logger.warning(msg)
        return result
