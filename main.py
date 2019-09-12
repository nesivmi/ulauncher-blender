import os
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.OpenAction import OpenAction
from ulauncher.api.shared.action.RunScriptAction import RunScriptAction

rfile_name = "recent-files.txt"


class BlenderExtension(Extension):
    def __init__(self):
        super(BlenderExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        query = event.get_argument() or str()

        bl_config = os.path.join(os.environ["HOME"], ".config", "blender")
        
        recent_files = []
        
        blapp = extension.preferences["start"]
        if os.path.exists(blapp) and len(query) < 1:
            recent_files.append([blapp, "Blender", "Start New File"])
        
        for i in os.listdir(bl_config):
            fn = os.path.join(bl_config, i, "config", rfile_name)
            if not os.path.exists(fn): continue
            with open(fn) as f:
                for j in f.readlines():
                    j = j.strip()
                    if len(query) > 0:
                        if query.lower() in j.lower():
                            recent_files.append([j, os.path.basename(j), os.path.dirname(j)])
                    else:
                        recent_files.append([j, os.path.basename(j), os.path.dirname(j)])
                
        items = [ExtensionResultItem(icon='images/icon{}.png'.format( "" if f_name == "Blender" else "2"),
                                     name=f_name,
                                     description=dir_name,
                                     on_enter=OpenAction(path) if f_name != "Blender" else RunScriptAction(path)
                                     )
                 for path, f_name, dir_name in recent_files
        ]

        return RenderResultListAction(items)


if __name__ == '__main__':
    BlenderExtension().run()
