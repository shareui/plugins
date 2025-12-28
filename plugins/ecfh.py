__id__ = "shareui_efch"
__name__ = "exteraFetch"
__description__ = "displays sys info [.efch]"
__author__ = "@shareui"
__version__ = "1.0.0"
__icon__ = "miyabiZZZ/1"
__min_version__ = "12.1.1"

from base_plugin import BasePlugin, HookResult, HookStrategy
from typing import Any
from android_utils import log, run_on_ui_thread
from ui.settings import Header, Switch
from client_utils import get_send_messages_helper, get_user_config
from markdown_utils import parse_markdown
from java.util import ArrayList
from org.telegram.tgnet import TLRPC
import subprocess
import os
import threading

class ExteraFetchPlugin(BasePlugin):
    def on_plugin_load(self):
        self.add_on_send_message_hook()
# The plugin is used voluntarily to obtain information at will, it is not a malicious plugin
    def create_settings(self):
        return [
            Header(text="Display Settings"),
            Switch(key="show_app_version", text="App Version", default=True),
            Switch(key="show_package_name", text="Package Name", default=True),
            Switch(key="show_pid", text="PID", default=True),
            Switch(key="show_uid", text="UID", default=True),
            Switch(key="show_foreground_activity", text="Foreground Activity", default=True),
            Switch(key="show_app_ram", text="App RAM Usage", default=True),
            Switch(key="show_used_ram", text="Used RAM", default=True),
            Switch(key="show_available_ram", text="Available RAM", default=True),
            Switch(key="show_cpu_cores", text="CPU Cores", default=True),
            Switch(key="show_cpu_freq", text="CPU Frequency", default=True),
            Switch(key="show_android_version", text="Android Version", default=True),
            Switch(key="show_root_status", text="Root Status", default=True),
            Switch(key="show_total_ram", text="Total RAM", default=True),
            Switch(key="show_uptime", text="System Uptime", default=True),
            Switch(key="show_network_type", text="Network Type", default=False), # disabled for security
            Switch(key="show_storage", text="Storage Usage", default=True),
            Switch(key="show_battery", text="Battery Level", default=True),
            Switch(key="show_device_model", text="Device Model", default=True),
            Switch(key="show_screen_resolution", text="Screen Resolution", default=True),
            Switch(key="show_density_dpi", text="Density DPI", default=True),
            Switch(key="show_free_ram", text="Free RAM", default=True),
            Switch(key="show_ip_address", text="IP Address", default=False), # disabled for security
            Switch(key="show_sim_operator", text="SIM Operator", default=False), # disabled for security
            Switch(key="show_manufacturer", text="Manufacturer", default=True),
            Switch(key="show_board", text="Board", default=True),
            Switch(key="show_brand", text="Product Line", default=True),
            Switch(key="show_hardware", text="Hardware", default=True),
            Switch(key="show_refresh_rate", text="Refresh Rate", default=True),
            Switch(key="show_java_vm", text="Java VM Version", default=True),
            Switch(key="show_user_id", text="User ID", default=True),
            Switch(key="show_premium", text="Premium Status", default=True),
        ]

    def get_system_info(self):
        from org.telegram.messenger import BuildVars, ApplicationLoader
        from android.os import Build, Process, SystemClock
        from android.app import ActivityManager
        from android.content import Context
        from android.os import StatFs
        from android.content import Intent, IntentFilter
        from android.os import BatteryManager
        from android.util import DisplayMetrics
        from android.telephony import TelephonyManager
        from java.lang import System as JavaSystem
        import socket

        context = ApplicationLoader.applicationContext
        info = {}

        if self.get_setting("show_app_version", True):
            info["app_version"] = BuildVars.BUILD_VERSION_STRING

        if self.get_setting("show_package_name", True):
            info["package_name"] = context.getPackageName()

        if self.get_setting("show_pid", True):
            info["pid"] = str(Process.myPid())

        if self.get_setting("show_uid", True):
            info["uid"] = str(Process.myUid())

        if self.get_setting("show_foreground_activity", True):
            try:
                am = context.getSystemService(Context.ACTIVITY_SERVICE)
                tasks = am.getRunningTasks(1)
                if tasks and len(tasks) > 0:
                    info["foreground_activity"] = tasks[0].topActivity.getClassName()
            except:
                info["foreground_activity"] = "N/A"

        if self.get_setting("show_app_ram", True) or self.get_setting("show_used_ram", True) or self.get_setting("show_available_ram", True) or self.get_setting("show_total_ram", True) or self.get_setting("show_free_ram", True):
            am = context.getSystemService(Context.ACTIVITY_SERVICE)
            mem_info = ActivityManager.MemoryInfo()
            am.getMemoryInfo(mem_info)

            if self.get_setting("show_app_ram", True):
                try:
                    pids = [Process.myPid()]
                    mi = am.getProcessMemoryInfo(pids)
                    if mi and len(mi) > 0:
                        info["app_ram"] = str(mi[0].getTotalPss() // 1024)
                except:
                    info["app_ram"] = "N/A"

            if self.get_setting("show_used_ram", True):
                info["used_ram"] = str((mem_info.totalMem - mem_info.availMem) // (1024 * 1024))

            if self.get_setting("show_available_ram", True):
                info["available_ram"] = str(mem_info.availMem // (1024 * 1024))

            if self.get_setting("show_total_ram", True):
                info["total_ram"] = str(mem_info.totalMem // (1024 * 1024))

            if self.get_setting("show_free_ram", True):
                info["free_ram"] = str(mem_info.availMem // (1024 * 1024))

        if self.get_setting("show_cpu_cores", True):
            info["cpu_cores"] = str(os.cpu_count())

        if self.get_setting("show_cpu_freq", True):
            try:
                with open("/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq", "r") as f:
                    freq = int(f.read().strip()) // 1000
                    info["cpu_freq"] = str(freq)
            except:
                info["cpu_freq"] = "N/A"

        if self.get_setting("show_android_version", True):
            info["android_version"] = Build.VERSION.RELEASE

        if self.get_setting("show_root_status", True):
            try:
                result = subprocess.run(["su", "-c", "echo test"], capture_output=True, timeout=1)
                info["is_rooted"] = "Yes" if result.returncode == 0 else "No"
            except:
                info["is_rooted"] = "No"

        if self.get_setting("show_uptime", True):
            try:
                uptime_ms = SystemClock.elapsedRealtime()
                uptime_seconds = int(uptime_ms / 1000)
                hours = uptime_seconds // 3600
                minutes = (uptime_seconds % 3600) // 60
                info["uptime"] = f"{hours}h {minutes}m"
            except:
                info["uptime"] = "N/A"

        if self.get_setting("show_network_type", False):
            try:
                from android.net import ConnectivityManager, NetworkCapabilities
                cm = context.getSystemService(Context.CONNECTIVITY_SERVICE)
                network = cm.getActiveNetwork()
                if network:
                    caps = cm.getNetworkCapabilities(network)
                    if caps:
                        conn_type = "Unknown"
                        for t, n in [
                            (NetworkCapabilities.TRANSPORT_WIFI, "WiFi"),
                            (NetworkCapabilities.TRANSPORT_CELLULAR, "Mobile"),
                            (NetworkCapabilities.TRANSPORT_ETHERNET, "Ethernet"),
                            (NetworkCapabilities.TRANSPORT_VPN, "VPN"),
                        ]:
                            if caps.hasTransport(t):
                                conn_type = n
                                break
                        info["network_type"] = conn_type
                    else:
                        info["network_type"] = "Disconnected"
                else:
                    info["network_type"] = "Disconnected"
            except:
                info["network_type"] = "N/A"

        if self.get_setting("show_storage", True):
            try:
                stat = StatFs(os.path.expanduser("~"))
                total = (stat.getBlockCount() * stat.getBlockSize()) / (1024 ** 3)
                available = (stat.getAvailableBlocks() * stat.getBlockSize()) / (1024 ** 3)
                used = total - available
                info["storage_used"] = f"{used:.1f}"
                info["storage_total"] = f"{total:.1f}"
            except:
                info["storage_used"] = "N/A"
                info["storage_total"] = "N/A"

        if self.get_setting("show_battery", True):
            try:
                battery_intent = context.registerReceiver(None, IntentFilter(Intent.ACTION_BATTERY_CHANGED))
                level = battery_intent.getIntExtra(BatteryManager.EXTRA_LEVEL, -1)
                scale = battery_intent.getIntExtra(BatteryManager.EXTRA_SCALE, -1)
                info["battery"] = str(int((level / float(scale)) * 100))
            except:
                info["battery"] = "N/A"

        if self.get_setting("show_device_model", True):
            info["device_model"] = Build.MODEL

        if self.get_setting("show_manufacturer", True):
            info["manufacturer"] = Build.MANUFACTURER

        if self.get_setting("show_board", True):
            info["board"] = Build.BOARD

        if self.get_setting("show_brand", True):
            info["product_line"] = Build.BRAND

        if self.get_setting("show_hardware", True):
            info["hardware"] = Build.HARDWARE

        if self.get_setting("show_screen_resolution", True) or self.get_setting("show_density_dpi", True) or self.get_setting("show_refresh_rate", True):
            try:
                metrics = context.getResources().getDisplayMetrics()
                if self.get_setting("show_screen_resolution", True):
                    info["screen_width"] = str(metrics.widthPixels)
                    info["screen_height"] = str(metrics.heightPixels)
                if self.get_setting("show_density_dpi", True):
                    info["density_dpi"] = str(metrics.densityDpi)
                if self.get_setting("show_refresh_rate", True):
                    try:
                        wm = context.getSystemService(Context.WINDOW_SERVICE)
                        display = wm.getDefaultDisplay()
                        refresh_rate = display.getRefreshRate()
                        info["refresh_rate"] = f"{round(float(refresh_rate), 1)}"
                    except:
                        info["refresh_rate"] = "N/A"
            except:
                if self.get_setting("show_screen_resolution", True):
                    info["screen_width"] = "N/A"
                    info["screen_height"] = "N/A"
                if self.get_setting("show_density_dpi", True):
                    info["density_dpi"] = "N/A"
                if self.get_setting("show_refresh_rate", True):
                    info["refresh_rate"] = "N/A"

        if self.get_setting("show_ip_address", False):
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(("8.8.8.8", 80))
                info["ip_address"] = s.getsockname()[0]
                s.close()
            except:
                info["ip_address"] = "N/A"

        if self.get_setting("show_sim_operator", False):
            try:
                tm = context.getSystemService(Context.TELEPHONY_SERVICE)
                info["sim_operator"] = tm.getNetworkOperatorName() or "N/A"
            except:
                info["sim_operator"] = "N/A"

        if self.get_setting("show_java_vm", True):
            try:
                info["java_vm"] = JavaSystem.getProperty('java.vm.version')
            except:
                info["java_vm"] = "N/A"

        if self.get_setting("show_user_id", True):
            try:
                user_config = get_user_config()
                info["user_id"] = str(user_config.getClientUserId())
            except:
                info["user_id"] = "N/A"

        if self.get_setting("show_premium", True):
            try:
                user_config = get_user_config()
                info["premium"] = "Yes" if user_config.isPremium() else "No"
            except:
                info["premium"] = "N/A"

        return info

    def format_info(self, info):
        lines = ["*exteraFetch*\n"]

        if "app_version" in info:
            lines.append(f"app version: {info['app_version']}")
        if "package_name" in info:
            lines.append(f"package name: {info['package_name']}")
        if "pid" in info:
            lines.append(f"pid: {info['pid']}")
        if "uid" in info:
            lines.append(f"uid: {info['uid']}")
        if "foreground_activity" in info:
            lines.append(f"foreground activity: {info['foreground_activity']}")
        if "app_ram" in info:
            lines.append(f"app RAM usage: {info['app_ram']}MB")
        if "used_ram" in info:
            lines.append(f"used RAM: {info['used_ram']}MB")
        if "available_ram" in info:
            lines.append(f"available RAM: {info['available_ram']}MB")
        if "cpu_cores" in info:
            lines.append(f"CPU cores: {info['cpu_cores']}")
        if "cpu_freq" in info:
            lines.append(f"CPU frequency: {info['cpu_freq']}MHz")
        if "android_version" in info:
            lines.append(f"Android version: {info['android_version']}")
        if "is_rooted" in info:
            lines.append(f"root status: {info['is_rooted']}")
        if "total_ram" in info:
            lines.append(f"RAM: {info['total_ram']}MB")
        if "uptime" in info:
            lines.append(f"system uptime: {info['uptime']}")
        if "network_type" in info:
            lines.append(f"network type: {info['network_type']}")
        if "storage_used" in info and "storage_total" in info:
            lines.append(f"storage usage: {info['storage_used']}/{info['storage_total']}GB")
        if "battery" in info:
            lines.append(f"battery lvl: {info['battery']}%")
        if "device_model" in info:
            lines.append(f"model: {info['device_model']}")
        if "manufacturer" in info:
            lines.append(f"manufacturer: {info['manufacturer']}")
        if "board" in info:
            lines.append(f"board: {info['board']}")
        if "product_line" in info:
            lines.append(f"product line: {info['product_line']}")
        if "hardware" in info:
            lines.append(f"hardware: {info['hardware']}")
        if "screen_width" in info and "screen_height" in info:
            lines.append(f"screen resolution: {info['screen_width']}x{info['screen_height']}")
        if "density_dpi" in info:
            lines.append(f"density DPI: {info['density_dpi']}")
        if "refresh_rate" in info:
            lines.append(f"refresh rate: {info['refresh_rate']}Hz")
        if "free_ram" in info:
            lines.append(f"free RAM: {info['free_ram']}MB")
        if "ip_address" in info:
            lines.append(f"IP address: {info['ip_address']}")
        if "sim_operator" in info:
            lines.append(f"SIM operator: {info['sim_operator']}")
        if "java_vm" in info:
            lines.append(f"JVM: {info['java_vm']}")
        if "user_id" in info:
            lines.append(f"user ID: {info['user_id']}")
        if "premium" in info:
            lines.append(f"premium: {info['premium']}")

        return "\n".join(lines)

    def on_send_message_hook(self, account: int, params: Any) -> HookResult:
        if not isinstance(params.message, str) or not params.message.strip().startswith(".efch"):
            return HookResult()

        def run_fetch():
            try:
                info = self.get_system_info()
                markdown_string = self.format_info(info)
                
                parsed_message_object = parse_markdown(markdown_string)
                params.message = parsed_message_object.text
                
                entities_list = ArrayList()
                title_end = len("exteraFetch\n".encode(encoding='utf_16_le')) // 2
                
                for raw_entity in parsed_message_object.entities:
                    tlrpc_entity = raw_entity.to_tlrpc_object()
                    entities_list.add(tlrpc_entity)
                
                quote_entity = TLRPC.TL_messageEntityBlockquote()
                quote_entity.collapsed = True
                quote_entity.offset = title_end
                quote_entity.length = int(len(params.message.encode(encoding='utf_16_le')) / 2) - title_end
                entities_list.add(quote_entity)
                
                params.entities = entities_list

                run_on_ui_thread(lambda: self._send_message(params))
            except Exception as e:
                log(f"exteraFetch error: {str(e)}")
                params.message = f"Error: {str(e)}"
                run_on_ui_thread(lambda: self._send_message(params))

        threading.Thread(target=run_fetch, daemon=True).start()
        return HookResult(strategy=HookStrategy.CANCEL)

    def _send_message(self, params):
        try:
            params.replyToMsg = params.replyToMsg
            params.replyToTopMsg = params.replyToTopMsg
        except:
            pass
        send_helper = get_send_messages_helper()
        send_helper.sendMessage(params)