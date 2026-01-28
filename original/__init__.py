import bpy # type: ignore

from . import von_common
from . import von_ui
from . import von_ui_operators

bl_info = {
    "name": "Vona's Blender Source Tools",
    "author": "Vona",
    "version": (0, 0, 2),
    "blender": (4, 2, 10),
    "location": "Where the user can find it",
    "description": "Gold Version of Vona's addon that expands the blender source tools toolset to improve pipeline workflow.",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": ""}


def register():
    von_common.von_common_register()
    von_ui_operators.von_operator_register()
    von_ui.von_ui_register()

def unregister():
    von_ui.von_ui_unregister()
    von_ui_operators.von_operator_unregister()
    von_common.von_common_unregister()