import os
from typing import Any, Optional

from android_utils import log, run_on_ui_thread
from base_plugin import BasePlugin, HookResult, HookStrategy
from client_utils import run_on_queue, get_last_fragment, send_message
from ui.alert import AlertDialogBuilder
from markdown_utils import parse_markdown

__id__ = "shareui_tree"
__name__ = "Tree Explorer"
__description__ = "Shows exteraGram/ayugram directory structure. Usage: .et"
__author__ = "@shareui"
__version__ = "1.0.0"
__icon__ = "Sankt_Peterburg45/7"
__min_version__ = "12.2.3"


class TreePlugin(BasePlugin):
    def __init__(self):
        super().__init__()
        self.progress_dialog_builder: Optional[AlertDialogBuilder] = None

    def on_plugin_load(self):
        self.add_on_send_message_hook()

    def _get_package_name(self):
        try:
            from org.telegram.messenger import ApplicationLoader
            context = ApplicationLoader.applicationContext
            if context:
                package_name = context.getPackageName()
                log(f"Detected package name: {package_name}")
                return package_name
        except Exception as e:
            log(f"Error getting package name: {str(e)}")
        return "com.exteragram.messenger"

    def _get_base_path(self):
        package_name = self._get_package_name()
        possible_paths = [
            f"/data/data/{package_name}",
            f"/data/user/0/{package_name}",
            f"/storage/emulated/0/Android/data/{package_name}"
        ]
        for path in possible_paths:
            if os.path.exists(path):
                log(f"Found base path: {path}")
                return path
        log(f"No base path found, using default for {package_name}")
        return f"/data/user/0/{package_name}"

    def _get_tree_structure(
        self,
        path: str,
        prefix: str = "",
        max_depth: int = 5,
        current_depth: int = 0,
        folders_only: bool = False,
        show_hidden: bool = False
    ) -> list:
        if current_depth >= max_depth:
            return []

        lines = []
        try:
            if not os.path.exists(path):
                return [f"{prefix}[Path not found: {path}]"]

            if not os.path.isdir(path):
                return [f"{prefix}[Not a directory: {path}]"]

            try:
                items = sorted(os.listdir(path))
            except PermissionError:
                return [f"{prefix}[Permission denied]"]
            except Exception as e:
                return [f"{prefix}[Error: {str(e)}]"]

            if not show_hidden:
                items = [item for item in items if not item.startswith('.')]

            if folders_only:
                filtered_items = []
                for item in items:
                    item_path = os.path.join(path, item)
                    try:
                        if os.path.isdir(item_path):
                            filtered_items.append(item)
                    except:
                        pass
                items = filtered_items

            for i, item in enumerate(items):
                item_path = os.path.join(path, item)
                is_last = i == len(items) - 1
                connector = "└── " if is_last else "├── "
                extension = "    " if is_last else "│   "

                try:
                    if os.path.isdir(item_path):
                        lines.append(f"{prefix}{connector}{item}/")
                        if current_depth < max_depth - 1:
                            lines.extend(
                                self._get_tree_structure(
                                    item_path,
                                    prefix + extension,
                                    max_depth,
                                    current_depth + 1,
                                    folders_only,
                                    show_hidden
                                )
                            )
                    else:
                        if not folders_only:
                            try:
                                size = os.path.getsize(item_path)
                                size_str = self._format_size(size)
                                lines.append(f"{prefix}{connector}{item} ({size_str})")
                            except:
                                lines.append(f"{prefix}{connector}{item}")
                except PermissionError:
                    lines.append(f"{prefix}{connector}{item} [Permission denied]")
                except Exception as e:
                    lines.append(f"{prefix}{connector}{item} [Error: {str(e)}]")
        except Exception as e:
            lines.append(f"{prefix}[Error reading directory: {str(e)}]")

        return lines

    def _format_size(self, size: int) -> str:
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f}{unit}"
            size /= 1024.0
        return f"{size:.1f}TB"

    def _parse_flags(self, args: str):
        folders_only = False
        show_hidden = False
        path = "/"
        parts = args.split()
        for part in parts:
            if part.startswith('-'):
                if 'f' in part:
                    folders_only = True
                if 'h' in part:
                    show_hidden = True
            else:
                path = part
        return path, folders_only, show_hidden

    def _process_tree_request(self, target_path: str, peer_id: Any, folders_only: bool, show_hidden: bool):
        try:
            base_path = self._get_base_path()
            if target_path == "/":
                full_path = base_path
                display_path = "exteraGram Home"
            else:
                clean_path = target_path.lstrip('/')
                full_path = os.path.join(base_path, clean_path)
                display_path = f"/{clean_path}"

            flags_info = []
            if folders_only:
                flags_info.append("folders only")
            if show_hidden:
                flags_info.append("show hidden")
            flags_text = f" [{', '.join(flags_info)}]" if flags_info else ""

            log(f"Building tree for: {full_path}{flags_text}")

            tree_lines = self._get_tree_structure(
                full_path,
                "",
                max_depth=4,
                folders_only=folders_only,
                show_hidden=show_hidden
            )

            if not tree_lines:
                tree_lines = ["[Empty directory or no access]"]

            max_lines = 150
            if len(tree_lines) > max_lines:
                tree_lines = tree_lines[:max_lines]
                tree_lines.append(f"... (truncated, showing first {max_lines} items)")

            tree_content = "\n".join(tree_lines)

            markdown_message = (
                f"*Directory Tree:* {display_path}{flags_text}\n"
                f"*Full path:* `{full_path}`\n\n"
                f"```tree\n"
                f"{tree_content}\n"
                f"```"
            )

            try:
                parsed_message = parse_markdown(markdown_message)
                message_params = {
                    "message": parsed_message.text,
                    "peer": peer_id,
                    "entities": [e.to_tlrpc_object() for e in parsed_message.entities]
                }
            except Exception as parse_error:
                log(f"Markdown parse error: {str(parse_error)}")
                message_params = {
                    "message": f"Directory Tree: {display_path}{flags_text}\n{full_path}\n\n{tree_content}",
                    "peer": peer_id
                }
        except Exception as e:
            log(f"Tree plugin error: {str(e)}")
            import traceback
            log(f"Traceback: {traceback.format_exc()}")
            message_params = {
                "message": f"Error building tree: {str(e)}",
                "peer": peer_id
            }

        def _send_message_and_dismiss_dialog():
            try:
                if self.progress_dialog_builder:
                    self.progress_dialog_builder.dismiss()
                    self.progress_dialog_builder = None
                send_message(message_params)
                log("Message sent successfully")
            except Exception as send_error:
                log(f"Error sending message: {str(send_error)}")

        run_on_ui_thread(_send_message_and_dismiss_dialog)

    def on_send_message_hook(self, account: int, params: Any) -> HookResult:
        if not isinstance(params.message, str) or not params.message.startswith(".et"):
            return HookResult()

        try:
            message_text = params.message.strip()
            if message_text == ".et":
                package_name = self._get_package_name()
                params.message = (
                    "Tree Explorer Usage:\n\n"
                    ".et / - show home directory\n"
                    ".et /files - show specific directory\n"
                    ".et -f / - show folders only\n"
                    ".et -h / - show hidden files\n"
                    ".et -fh /cache - combine flags\n\n"
                    f"Current package: {package_name}"
                )
                return HookResult(strategy=HookStrategy.MODIFY, params=params)

            args = message_text[3:].strip()
            target_path, folders_only, show_hidden = self._parse_flags(args)
            peer_id = params.peer

            def _show_progress_and_process():
                try:
                    current_fragment = get_last_fragment()
                    if current_fragment:
                        activity = current_fragment.getParentActivity()
                        if activity:
                            self.progress_dialog_builder = AlertDialogBuilder(activity)
                            self.progress_dialog_builder.set_message("Building directory tree...")
                            self.progress_dialog_builder.show()
                except Exception as dialog_error:
                    log(f"Error showing dialog: {str(dialog_error)}")
                run_on_queue(lambda: self._process_tree_request(target_path, peer_id, folders_only, show_hidden))

            run_on_ui_thread(_show_progress_and_process)
            return HookResult(strategy=HookStrategy.BLOCK)

        except Exception as e:
            log(f"Tree plugin hook error: {str(e)}")
            import traceback
            log(f"Traceback: {traceback.format_exc()}")
            params.message = f"Error: {str(e)}"
            return HookResult(strategy=HookStrategy.MODIFY, params=params)