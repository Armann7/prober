import logging
import random
from abc import ABCMeta
from abc import abstractmethod
from collections.abc import Mapping
from pathlib import Path
from typing import Any
from typing import Literal

AlertLevel = Literal['info', 'low', 'medium', 'high']


class BaseScanResult(metaclass=ABCMeta):

    def __init__(self, scanner: str, url: str):
        self._scanner = scanner
        self._url = url

    def __repr__(self) -> str:
        return f'{self._scanner}: {self._url}'
    
    @abstractmethod
    def write_report(self, folder: Path):
        pass


class ScanResult(BaseScanResult, metaclass=ABCMeta):

    def __init__(self, scanner: str, url: str, raw: Mapping[str, Any], *levels: AlertLevel):
        super().__init__(scanner, url)        
        self._raw = raw
        self._levels = set(levels)


class ScanError(BaseScanResult):

    def __init__(self, scanner: str, url: str, message: str, output: str):
        super().__init__(scanner, url)        
        self._message = message
        self._output = output

    def __repr__(self) -> str:
        return f'{self._scanner}: {self._url} ({self._message})'
    
    def write_report(self, folder: Path):
        file: Path = folder / make_report_filename(f'{self._scanner}-error', self._url)
        file.write_text(self._output)


def make_report_filename(prefix: str, url: str) -> Path:
    unwanted_symbols = ':/\\*?+'
    translation_table = str.maketrans(unwanted_symbols, '_' * len(unwanted_symbols))
    url = url.lstrip('https://').lstrip('http://').rstrip('/')
    sanitized_url = url.translate(translation_table)
    if len(sanitized_url) > 200:
        sanitized_url = sanitized_url[:200] + f'_{random.randrange(1, 99999):05d}'  # nosec B331
    return Path(f'{prefix}-{sanitized_url}.json')


_logger = logging.getLogger(__name__)
