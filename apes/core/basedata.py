"""APES data class"""

import sys
import os
import glob
from datetime import datetime
from collections import OrderedDict
import magic
import pprint

from apes.utils.path import data_root, get_data

import pandas as pd

import logging
logger = logging.getLogger(__name__)

time_list = [f'{i}' for i in range(1955, 2050)]
all_tags = OrderedDict([
    ('power', ['load', 'generation', 'LMP']),
    ('energy', ['gas']),
    ('economy', ['gdp']),
    ('demography', ['population', 'income']),
    ('geography', ['state', 'county', 'city', 'MSA']),
    ('time', time_list),
    ('ungrouped', []),
])
flatten_all_tag = [val for values in all_tags.values() for val in values]


unit_dict = OrderedDict([
    ('Bytes', 1),
    ('KB', 1024),
    ('MB', 1024 ** 2),
    ('GB', 1024 ** 3),
])


def file_size_normalize(size):
    """
    Normalize file size with units in MB

    Parameters
    ----------
    size: str
        File size with units split by one space, e.g. "28.96 MB"
    """
    size_val, size_unit = size.split(' ')
    size_val = float(size_val)
    size_out = size_val * unit_dict[size_unit] / unit_dict['MB']
    return size_out


def file_size_format(size, force_unit=None) -> str:
    """
    Convert file size in Bytes to human readable format

    Parameters
    ----------
    size : float
        File size in Bytes
    force_unit : str, optional
        Force unit to be used, ['Bytes', 'KB', 'MB', 'GB'],

    Returns
    -------
    str
        File size with unit split by space,
        e.g. '1.2 MB'
    """
    out = '-1 Bytes'
    find_flag = False
    if force_unit:
        size_c = size / unit_dict[force_unit]
        out = f'{size_c:.2f} {force_unit}'
    else:
        for unit in unit_dict.keys():
            size_c = size / unit_dict[unit]
            out = f'{size_c:.2f} {unit}'
            if (size_c < 1024):
                find_flag = True
                break
            elif (size_c >= 1024):
                continue
        if not find_flag:
            logger.warning(f'File size is too large: {out}')
    return out


class DictAttr():

    def __init__(self, attr):
        """
        Base class for attribtue that are in OrderedDict

        Parameters
        ----------
        attr: OrderedDict
            Data attribute dictionary
        """
        for key, val in attr.items():
            setattr(self, key, val)
        self._dict = self.as_dict()

    def as_dict(self):
        """
        Return the config fields and values in an ``OrderedDict``.
        """
        out = []
        for key, val in self.__dict__.items():
            if not key.startswith('_'):
                out.append((key, val))
        return (OrderedDict(out))

    def __repr__(self):
        return pprint.pformat(self._dict)


class BaseData():
    """
    Base class for all data class.
    """

    def __init__(self, file_name,
                 name=None,
                 info=None, tag=[],
                 url=None, doi=None,
                 lic=None, publisher=None,):
        """
        Parameters
        ----------
        file_name : str
            File name
        name : str, optional
            Name of the dataset
        info : str
            meta data of the dataset
        tag : list of str, optional
            Tag of the dataset
        """
        # --- directory description ---
        self.name = name

        # --- split ---
        try:
            magic.from_file(get_data(file_name), mime=True)
            is_split = False
        except IsADirectoryError:
            is_split = True
        self.is_split = is_split

        # --- data tags ---
        tags = self._set_tag_dict(input_tag=tag, all_tags=all_tags)
        self.tag = DictAttr(tags)
        # --- data attributes ---
        attr = self._set_attr_dict(file_name=file_name,
                                   name=name, info=info,
                                   url=url, doi=doi, lic=lic,
                                   publisher=publisher)
        self.attr = DictAttr(attr)
        self._fpath = get_data(file_name)

        # --- file size check ---
        size_mb = file_size_normalize(self.attr.size)
        thl_warn_mb = 50
        thl_error_mb = 100
        if size_mb > thl_warn_mb:
            info = f'File size is larger than {thl_warn_mb} MB'
            logger.info(info)
        elif size_mb > thl_error_mb:
            info = f'File size is larger than {thl_error_mb} MB'
            logger.warning(
                f'File size {size_mb} larger than: {thl_error_mb} MB')

    def __repr__(self):
        # TODO: include publisher, license, url, doi
        info = f'Class: {self.__class__.__name__}' + '\n' + \
            f'Data name: {self.name}' + '\n' + \
            f'Data type: {self.attr.type}' + '\n' + \
            f'Data size: {self.attr.size}' + '\n' + \
            f'Is split: {self.is_split}' + '\n' + \
            f'Created at: {self.attr.created_time}' + '\n' + \
            f'Last modified at: {self.attr.modified_time}' + '\n' + \
            f'Last accessed at: {self.attr.accessed_time}' + '\n' + \
            f'Is split: {self.is_split}' + '\n'
        if self.is_split:
            info2 = f'Stored in: {self._fpath}'
        else:
            info2 = f'Stored as: {self._fpath}'
        return info + info2

    def _set_tag_dict(self, input_tag, all_tags) -> OrderedDict:
        """Set the tags into dictionary"""
        tags = all_tags.copy().fromkeys(all_tags.keys(), [])
        for cat in tags.keys():
            values = []
            for single_tag in input_tag:
                if single_tag in all_tags[cat]:
                    values.append(single_tag)
                    continue
                else:
                    continue
            if len(values) > 0:
                tags[cat] = values
            else:
                pass
        ungrouped_list = []
        for single_tag in input_tag:
            if not single_tag in flatten_all_tag:
                ungrouped_list.append(single_tag)
        if len(ungrouped_list) > 0:
            tags['ungrouped'] = ungrouped_list
            msg = f'Ungrouped tags: {ungrouped_list}'
            logger.info(msg + ', consider updating the tag list')
        return tags

    def _set_attr_dict(self, file_name,
                       name, info,
                       url, doi, lic,
                       publisher) -> OrderedDict:
        """
        Set the attributes of the data
        """
        t_format = '%Y-%m-%d, %H:%M:%S'
        fpath = get_data(file_name)

        # --- type ---
        type = None
        try:
            type = magic.from_file(fpath, mime=True).split('/')[-1]
        except IsADirectoryError:
            sub_files = os.listdir(fpath)
            sub_formats = [magic.from_file(
                fpath + '/' + sub_file, mime=True).split('/')[-1] for sub_file in sub_files]
            type = 'Multiple files, ' + f'{list(set(sub_formats))}'

        # --- size ---
        size_formatted = ''
        if self.is_split:
            size_count = 0
            for subpath, dirs, files in os.walk(fpath):
                for f in files:
                    fp = os.path.join(subpath, f)
                    size_count += os.path.getsize(fp)
            size_formatted = file_size_format(size_count, force_unit=None)
        else:
            size_formatted = file_size_format(
                os.path.getsize(fpath), force_unit=None)

        # --- time ---
        dct = os.path.getctime(fpath)
        dmt = os.path.getmtime(fpath)
        dat = os.path.getatime(fpath)

        # TODO: the timestamps seems to be wrong?
        attr = OrderedDict([
            ('name', name),
            ('info', info),
            ('file_name', file_name.split('/')[-1]),
            ('size', size_formatted),
            ('type', type),
            ('created_time', datetime.fromtimestamp(dct).strftime(t_format)),
            ('modified_time', datetime.fromtimestamp(dmt).strftime(t_format)),
            ('accessed_time', datetime.fromtimestamp(dat).strftime(t_format)),
            ('url', url),
            ('doi', doi),
            ('lic', lic),
            ('publisher', publisher),
        ])
        return attr

    def save(self, filename):
        """Save data to file"""
        # if the file size is larger than XX MB
        # seperate it into multiple files
        # TODO: find popular file size limit
        pass


class SourceData(BaseData):
    """
    Class for source data.
    """

    def __init__(self, file_name,
                 name=None,
                 info=None, tag=None,
                 url=None, doi=None,
                 lic=None, publisher=None,):
        """
        Parameters
        ----------
        file_name : str
            File name
        data_name : str, optional
            Name of the dataset
        info : str
            meta data of the dataset
        tag : list of str, optional
            Tag of the dataset
        url : str, optional
            Source URL of the dataset if available
        doi : str, optional
            DOI of the dataset if available
        lic : str, optional
            License of the dataset if applicable
        """
        super().__init__(file_name=file_name,
                         name=name,
                         info=info, tag=tag,
                         url=url, doi=doi, lic=lic,
                         publisher=publisher,)
        self.dir = data_root() + '/' + file_name


class CSVSourceData(SourceData):
    """Class for source data in CSV format"""
    # NOTE: should we consider Dask rather than Pandas?

    def __init__(self, file_name,
                 name=None,
                 info=None, tag=None,
                 url=None, doi=None,
                 lic=None, publisher=None,):
        super().__init__(file_name=file_name,
                         name=name,
                         info=info, tag=tag,
                         url=url, doi=doi, lic=lic,
                         publisher=publisher,)

    def as_df(self, **kwargs) -> pd.DataFrame:
        """Load data into pandas dataframe using pd.read_csv()"""
        if self.is_split:
            all_files = glob.glob(self.dir + '/*.csv')
            li = []
            for filename in all_files:
                frame = pd.read_csv(
                    filename, index_col=None, header=0,  **kwargs)
                li.append(frame)
            df = pd.concat(li, axis=0, ignore_index=True)
        else:
            df = pd.read_csv(self.dir, **kwargs)
        return df

    def head(self,  **kwargs) -> pd.DataFrame:
        """Preview the CSV data as pandas dataframe"""
        return self.as_df(**kwargs).head()


class MapData(BaseData):
    """Class for map data"""
    pass


# TODO: document the stored data


# TODO: ArcGIS API?
