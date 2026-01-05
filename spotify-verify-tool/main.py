"""
Spotify Student Verification Tool + Telegram Notif
Author: Toko RootSec Bot
"""
import os, re, sys, json, time, random, hashlib
from pathlib import Path
from io import BytesIO
try: import httpx
except ImportError: sys.exit("Install httpx: pip install httpx")
try: from PIL import Image, ImageDraw, ImageFont
except ImportError: sys.exit("Install Pillow: pip install Pillow")

# ============ CONFIG ============
PROGRAM_ID = "67c8c14f5f17a83b745e3f82"
SHEERID_API_URL = "https://services.sheerid.com/rest/v2"

# ============ TELEGRAM NOTIFIER ============
def send_telegram_alert(msg):
    try:
        # Cari file telegram.json di folder utama (parent dari folder ini)
        config_path = Path(__file__).parent.parent / "telegram.json"
        if not config_path.exists(): return
        
        with open(config_path) as f: config = json.load(f)
        token, chat_id = config.get("token"), config.get("chat_id")
        
        if token and chat_id:
            url = f"https://api.telegram.org/bot{token}/sendMessage"
            httpx.post(url, json={"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"})
    except Exception: pass

# ============ STATS TRACKING ============
class Stats:
    def __init__(self):
        self.file = Path(__file__).parent / "stats.json"
        self.data = self._load()
    def _load(self):
        try: return json.loads(self.file.read_text())
        except: return {"total": 0, "success": 0, "failed": 0, "orgs": {}}
    def _save(self): self.file.write_text(json.dumps(self.data, indent=2))
    def record(self, org, success):
        self.data["total"] += 1; self.data["success" if success else "failed"] += 1
        if org not in self.data["orgs"]: self.data["orgs"][org] = {"success": 0, "failed": 0}
        self.data["orgs"][org]["success" if success else "failed"] += 1
        self._save()
    def get_rate(self, org=None):
        if org:
            o = self.data["orgs"].get(org, {})
            t = o.get("success", 0) + o.get("failed", 0)
            return o.get("success", 0)/t*100 if t else 50
        return self.data["success"]/self.data["total"]*100 if self.data["total"] else 0
    def print_stats(self):
        print(f"\n📊 Stats: Total: {self.data['total']} | ✅ {self.data['success']} | ❌ {self.data['failed']}")

stats = Stats()

# ============ UNIVERSITIES (Partial List for Brevity) ============
UNIVERSITIES = [
    {"id": 2565, "name": "Pennsylvania State University-Main Campus", "domain": "psu.edu", "weight": 100},
    {"id": 3499, "name": "University of California, Los Angeles", "domain": "ucla.edu", "weight": 98},
    {"id": 3491, "name": "University of California, Berkeley", "domain": "berkeley.edu", "weight": 97},
    # ... (List aslinya panjang, kode ini tetap akan jalan dengan list pendek)
]

def select_university():
    return random.choice(UNIVERSITIES)

# ============ UTILITIES ============
FIRST_NAMES = ["James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph"]
LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis"]

def generate_fingerprint():
    return hashlib.md5(f"{time.time()}|{random.random()}".encode()).hexdigest()

def generate_name(): return random.choice(FIRST_NAMES), random.choice(LAST_NAMES)
def generate_email(f, l, d): return f"{f[0].lower()}{l.lower()}{random.randint(100,999)}@{d}"
def generate_birth_date(): return f"{random.randint(2000,2006)}-{random.randint(1,12):02d}-{random.randint(1,28):02d}"

# ============ DOCUMENT GENERATOR ============
def generate_student_id(first, last, school):
    w, h = 650, 400
    img = Image.new("RGB", (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw.rectangle([(0, 0), (w, 60)], fill=(0, 51, 102))
    draw.text((w//2, 30), "STUDENT ID", fill="white", anchor="mm")
    draw.text((w//2, 90), school[:50], fill="black", anchor="mm")
    draw.text((100, 150), f"Name: {first} {last}", fill="black")
    buf = BytesIO(); img.save(buf, format="PNG")
    return buf.getvalue()

# ============ VERIFIER ============
class SpotifyVerifier:
    def __init__(self, url, proxy=None):
        self.vid = re.search(r"verificationId=([a-f0-9]+)", url).group(1) if "verificationId" in url else None
        self.proxies = {"all://": f"http://{proxy}"} if proxy else None
        self.client = httpx.Client(timeout=30, proxies=self.proxies)
        self.org = None

    def _request(self, m, ep, json=None):
        try:
            r = self.client.request(m, f"{SHEERID_API_URL}{ep}", json=json)
            return r.json(), r.status_code
        except: return {}, 500

    def verify(self):
        if not self.vid: return {"success": False, "error": "Invalid URL"}
        try:
            first, last = generate_name()
            # Fallback jika UNIVERSITIES kosong/error
            self.org = select_university() if UNIVERSITIES else {"id":2565, "name":"PSU", "domain":"psu.edu"}
            self.org["idExtended"] = str(self.org["id"])
            email = generate_email(first, last, self.org["domain"])
            dob = generate_birth_date()
            
            print(f"\n   🎓 {first} {last} | {self.org['name']}")
            
            # Step 1: Doc
            doc = generate_student_id(first, last, self.org["name"])
            
            # Step 2: Info
            body = {
                "firstName": first, "lastName": last, "birthDate": dob, "email": email,
                "organization": self.org, "deviceFingerprintHash": generate_fingerprint(),
                "metadata": {"verificationId": self.vid}
            }
            data, status = self._request("POST", f"/verification/{self.vid}/step/collectStudentPersonalInfo", body)
            if status != 200: return {"success": False, "error": "Submit failed"}

            # Step 3: Skip SSO
            self._request("DELETE", f"/verification/{self.vid}/step/sso")
            
            # Step 4: Upload
            u_body = {"files": [{"fileName": "card.png", "mimeType": "image/png", "fileSize": len(doc)}]}
            data, _ = self._request("POST", f"/verification/{self.vid}/step/docUpload", u_body)
            upload_url = data.get("documents", [{}])[0].get("uploadUrl")
            if upload_url: self.client.put(upload_url, content=doc, headers={"Content-Type": "image/png"})
            
            # Step 5: Complete
            self._request("POST", f"/verification/{self.vid}/step/completeDocUpload")
            stats.record(self.org["name"], True)
            
            # TELEGRAM NOTIF
            msg = (f"✅ *SPOTIFY SUCCESS*\n\n"
                   f"👤 Name: `{first} {last}`\n"
                   f"📧 Email: `{email}`\n"
                   f"🏫 School: `{self.org['name']}`\n"
                   f"🎂 DOB: `{dob}`")
            send_telegram_alert(msg)
            print(f"   🎉 Telegram Notification Sent!")

            return {"success": True, "student": f"{first} {last}", "email": email, "school": self.org["name"]}
            
        except Exception as e:
            return {"success": False, "error": str(e)}

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("url", nargs="?")
    args = parser.parse_args()
    
    url = args.url or input("   URL: ").strip()
    if "sheerid" not in url: return
    
    verifier = SpotifyVerifier(url)
    res = verifier.verify()
    
    if res["success"]:
        print(f"\n   ✅ SUCCESS: {res['email']}")
    else:
        print(f"\n   ❌ FAILED: {res.get('error')}")
    stats.print_stats()

if __name__ == "__main__":
    main()
