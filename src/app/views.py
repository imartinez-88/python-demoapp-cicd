from flask import render_template, current_app as app

try:
    import cpuinfo
except Exception:
    cpuinfo = None

import psutil
import platform
import datetime


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/info")
def info():
    osinfo = {}

    if cpuinfo:
        osinfo["cpu"] = cpuinfo.get_cpu_info().get("brand_raw", "Unknown CPU")
    else:
        osinfo["cpu"] = "Unknown CPU"

    osinfo["platform"] = platform.platform()
    osinfo["memory"] = psutil.virtual_memory().total
    osinfo["time"] = datetime.datetime.utcnow().isoformat()

    return osinfo

