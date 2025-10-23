import os, json
from django.http import JsonResponse, Http404, FileResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .tcp_server import current_downloads, downloads_lock, FIRMWARE_DIR, METADATA_PATH, metadata_lock

# Load metadata
if not os.path.exists(METADATA_PATH):
    with open(METADATA_PATH, "w") as f:
        json.dump({}, f)

with open(METADATA_PATH, "r") as f:
    firmware_metadata = json.load(f)

def index(request):
    return render(request, 'firmware/index.html')

def logs(request):
    log_file = 'app.log'
    try:
        with open(log_file) as f:
            logs = f.read()
    except FileNotFoundError:
        logs = "No logs yet."
    return render(request, 'firmware/logs.html', {'logs': logs})

def get_completed_keys(data):
    return [k for k, v in data.items() if v.get('status') == 'Completed']

@csrf_exempt
def clear_downloads(request):
    if request.method == 'POST':
        with downloads_lock:
            completed = get_completed_keys(current_downloads)
            for key in completed:
                del current_downloads[key]
        return JsonResponse({"ok": True})

def downloads_status(request):
    with downloads_lock:
        snapshot = list(current_downloads.values())
    return JsonResponse(snapshot, safe=False)

def firmwares_api(request):
    with metadata_lock:
        items = [{"firmwareId": k,
                  "original_name": v.get("original_name"),
                  "stored_path": v.get("stored_path"),
                  "size": v.get("size", 0)} for k,v in firmware_metadata.items()]
    return JsonResponse(items, safe=False)

@csrf_exempt
def upload(request):
    if request.method != 'POST':
        return JsonResponse({"ok": False, "error": "POST required"}, status=400)
    file = request.FILES.get('file')
    firmware_id = request.POST.get('firmwareId', '').strip()
    if not file or not firmware_id:
        return JsonResponse({"ok": False, "error": "Missing file or firmwareId"}, status=400)

    os.makedirs(FIRMWARE_DIR, exist_ok=True)
    dest_path = os.path.join(FIRMWARE_DIR, f"{firmware_id}.bin")
    with open(dest_path, 'wb') as f:
        for chunk in file.chunks():
            f.write(chunk)

    with metadata_lock:
        firmware_metadata[firmware_id] = {"stored_path": dest_path, "original_name": file.name, "size": os.path.getsize(dest_path)}
        with open(METADATA_PATH, "w") as f:
            json.dump(firmware_metadata, f, indent=2)

    return JsonResponse({"ok": True, "firmwareId": firmware_id, "size": os.path.getsize(dest_path)})

def download_firmware(request, firmware_id):
    entry = firmware_metadata.get(firmware_id)
    if not entry or not os.path.exists(entry['stored_path']):
        raise Http404("Firmware not found")
    return FileResponse(open(entry['stored_path'], 'rb'), as_attachment=True, filename=entry['original_name'])
