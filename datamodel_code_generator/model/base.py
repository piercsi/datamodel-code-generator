from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional, List

from mako.template import Template

TEMPLATE_DIR: Path = Path(__file__).parents[0] / 'template'


class DataModelField:
    def __init__(self, name: str, type_hint: Optional[str] = None, default: Optional[str] = None,
                 required: bool = False):
        self.name: str = name
        self.type_hint: Optional[str] = type_hint
        self.required: bool = required
        self.default: Optional[str] = default


class TemplateBase(ABC):
    def __init__(self, template_file_name):
        self.template_file_name: str = template_file_name
        self._template: Optional[Template] = None

    @property
    def template(self) -> Template:
        if self._template:
            return self._template
        self._template = Template(filename=str(TEMPLATE_DIR / self.template_file_name))
        return self._template

    @abstractmethod
    def render(self) -> str:
        pass

    def _render(self, *args, **kwargs):
        return self.template.render(*args, **kwargs)

    def __str__(self) -> str:
        return self.render()


class DataModel(TemplateBase, ABC):
    TEMPLATE_FILE_NAME: str = ''

    def __init__(self, name: str, fields: List[DataModelField],
                 decorators: Optional[List[str]] = None, base_class: Optional[str] = None):

        if not self.TEMPLATE_FILE_NAME:
            raise Exception(f'TEMPLATE_FILE_NAME Not Set')

        self.name: str = name
        self.fields: List[DataModelField] = fields or DataModelField(name='pass')
        self.decorators: List[str] = decorators or []
        self.base_class: Optional[str] = base_class
        self._template: Optional[Template] = None

        super().__init__(template_file_name=self.TEMPLATE_FILE_NAME)

    def render(self) -> str:
        response = self._render(
            class_name=self.name,
            fields=self.fields,
            decorators=self.decorators,
            base_class=self.base_class
        )
        return response
