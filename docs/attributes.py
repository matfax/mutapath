import re

from sphinx.application import Sphinx
from sphinx.errors import ExtensionError
from sphinx.ext import autodoc
from sphinx.util import logging, import_object, inspect

import mutapath

LOG = logging.getLogger(__name__)

_DOC_REF_MATCHER = re.compile(r'[ "]*[.]{2} seealso:: :[funcatr]+:`([a-zA-Z.]+)`[ "]*$')


def _import_wrapped_members(cls, member_name, member, cls_name=""):
    LOG.debug(f"[attributes] inspecting {cls_name}.{member_name}")
    if not member_name.startswith("_"):
        see_other_matched = _DOC_REF_MATCHER.match(str(member.__doc__))
        if see_other_matched is not None:
            other_ref = see_other_matched.group(1)
            LOG.info(
                f"[attributes] importing referenced doc for member {cls_name}.{member_name} from {other_ref}"
            )
            try:
                other_obj = import_object(other_ref)
                member.__doc__ = other_obj.__doc__
                setattr(cls, member_name, member)
            except ModuleNotFoundError:
                LOG.warning(f"[attributes] could not import {other_ref}")
            except ExtensionError:
                LOG.warning(f"[attributes] could not import {other_ref}")
            except AttributeError:
                LOG.warning(f"[attributes] could not import {other_ref}")


def setup(app: Sphinx):
    LOG.info("[attributes] starting attributes extension")
    app.add_autodocumenter(AppDocumenter, override=True)

    for name, member in inspect.getmembers(mutapath.Path):
        _import_wrapped_members(mutapath.Path, name, member, "mutapath.Path")
    for name, member in inspect.getmembers(mutapath.MutaPath):
        _import_wrapped_members(mutapath.MutaPath, name, member, "mutapath.MutaPath")


class AppDocumenter(autodoc.ModuleDocumenter):
    def __init__(self, *args) -> None:
        super().__init__(*args)
        if isinstance(self.object, mutapath.Path):
            for member in dir(mutapath.Path):
                if member not in self.options.get("members") and not member.startswith(
                    "_"
                ):
                    LOG.info(f"[attributes] adding wrapped member {member}")
                    self.options["members"].append(member)
