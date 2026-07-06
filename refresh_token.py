#!/usr/bin/env python3
"""Gia hạn token Instagram (chạy TẠI MÁY, ~mỗi 50 ngày).
- Đọc token hiện tại từ `.ig_token.local` (KHÔNG commit — nằm trong .gitignore).
- Gọi refresh endpoint của Instagram → token mới +60 ngày.
- Lưu token mới về `.ig_token.local` + cập nhật GitHub Secret IG_ACCESS_TOKEN.
- PAT GitHub lấy từ keychain của máy (git credential) — KHÔNG lưu lên cloud.
Chạy: python3 refresh_token.py
"""
import json, os, base64, subprocess, urllib.request, urllib.error
from nacl import encoding, public

HERE = os.path.dirname(os.path.abspath(__file__))
OWNER, REPO = "trandaichi12a3-star", "ig-auto-bs-trandaichi"
TOKEN_FILE = os.path.join(HERE, ".ig_token.local")


def get_pat():
    out = subprocess.run(["git", "credential", "fill"],
                         input="protocol=https\nhost=github.com\n\n",
                         capture_output=True, text=True).stdout
    for line in out.splitlines():
        if line.startswith("password="):
            return line[len("password="):]
    raise SystemExit("Không lấy được PAT GitHub từ keychain.")


def gh_api(pat, method, path, body=None):
    req = urllib.request.Request(f"https://api.github.com{path}",
        data=json.dumps(body).encode() if body is not None else None, method=method)
    req.add_header("Authorization", f"token {pat}")
    req.add_header("Accept", "application/vnd.github+json")
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.status, (json.load(r) if r.status != 204 else {})


def main():
    old = open(TOKEN_FILE).read().strip()
    resp = urllib.request.urlopen(
        "https://graph.instagram.com/refresh_access_token"
        f"?grant_type=ig_refresh_token&access_token={old}", timeout=30)
    data = json.load(resp)
    new = data.get("access_token")
    if not new:
        raise SystemExit(f"Refresh thất bại: {data}")
    open(TOKEN_FILE, "w").write(new)
    print(f"Token mới (sống thêm {data.get('expires_in',0)//86400} ngày). Đang cập nhật Secret...")

    pat = get_pat()
    _, key = gh_api(pat, "GET", f"/repos/{OWNER}/{REPO}/actions/secrets/public-key")
    pk = public.PublicKey(key["key"].encode(), encoding.Base64Encoder())
    enc = base64.b64encode(public.SealedBox(pk).encrypt(new.encode())).decode()
    st, _ = gh_api(pat, "PUT", f"/repos/{OWNER}/{REPO}/actions/secrets/IG_ACCESS_TOKEN",
                   {"encrypted_value": enc, "key_id": key["key_id"]})
    print("Cập nhật Secret IG_ACCESS_TOKEN:", "OK" if st in (201, 204) else st)


if __name__ == "__main__":
    main()
