#!/usr/bin/env python3
"""Đăng Reel Instagram kế tiếp trong hàng đợi. Chạy bởi GitHub Actions (máy tắt vẫn đăng).
Token đọc từ biến môi trường (GitHub secret), KHÔNG hardcode.
Trạng thái đã đăng lưu ở posted.json (Actions commit lại sau mỗi lần chạy)."""
import datetime, json, os, sys, time, urllib.parse, urllib.request, urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
MIN_HOURS = 40  # giãn cách tối thiểu giữa 2 lần đăng → nhịp ~2 ngày/bài
USER_ID = os.environ["IG_USER_ID"]
TOKEN = os.environ["IG_ACCESS_TOKEN"]
BASE = "https://graph.instagram.com/v21.0"
# Link video công khai để Instagram tải về
RAW_BASE = "https://raw.githubusercontent.com/trandaichi12a3-star/ig-auto-bs-trandaichi/main/videos/"


def api_get(node, params):
    url = f"{BASE}/{node}?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(url, timeout=60) as r:
        return json.load(r)


def api_post(node, params):
    data = urllib.parse.urlencode(params).encode()
    req = urllib.request.Request(f"{BASE}/{node}", data=data, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        try:
            return {"error": json.load(e)}
        except Exception:
            return {"error": e.read().decode(errors="replace")}


def main():
    queue = json.load(open(os.path.join(HERE, "queue.json"), encoding="utf-8"))
    posted_path = os.path.join(HERE, "posted.json")
    posted = json.load(open(posted_path, encoding="utf-8")) if os.path.exists(posted_path) else []
    posted_ids = {p["id"] for p in posted}

    # Nhịp ~2 ngày/bài: nếu bài gần nhất đăng chưa đủ MIN_HOURS thì bỏ qua lượt hôm nay.
    if posted:
        try:
            last = datetime.datetime.strptime(posted[-1]["at"], "%Y-%m-%d %H:%M UTC")
            hrs = (datetime.datetime.utcnow() - last).total_seconds() / 3600
            if hrs < MIN_HOURS:
                print(f"CHƯA TỚI CỮ: mới đăng {hrs:.1f}h trước (cần ≥{MIN_HOURS}h) → bỏ qua hôm nay.")
                return 0
        except Exception as e:
            print("Không đọc được thời gian bài trước, vẫn tiếp tục:", e)

    nxt = next((item for item in queue if item["id"] not in posted_ids), None)
    if nxt is None:
        print("HẾT HÀNG ĐỢI: không còn Reel chưa đăng. Cần bổ sung queue.json.")
        return 0

    video_url = RAW_BASE + urllib.parse.quote(nxt["video"])
    caption = nxt.get("caption", "")
    print(f"→ Chuẩn bị đăng: {nxt['id']}  ({nxt['video']})")

    # Bước 1: tạo media container (REELS)
    create = api_post(f"{USER_ID}/media", {
        "media_type": "REELS",
        "video_url": video_url,
        "caption": caption,
        "access_token": TOKEN,
    })
    cid = create.get("id")
    if not cid:
        print("LỖI tạo container:", create, file=sys.stderr)
        return 1
    print(f"  container id = {cid}, chờ Instagram xử lý video...")

    # Bước 2: chờ status FINISHED (tối đa ~5 phút)
    for _ in range(30):
        time.sleep(10)
        st = api_get(cid, {"fields": "status_code", "access_token": TOKEN})
        code = st.get("status_code")
        print(f"  status = {code}")
        if code == "FINISHED":
            break
        if code == "ERROR":
            print("LỖI Instagram xử lý video:", st, file=sys.stderr)
            return 1
    else:
        print("QUÁ THỜI GIAN chờ xử lý video (>5 phút).", file=sys.stderr)
        return 1

    # Bước 3: publish
    pub = api_post(f"{USER_ID}/media_publish", {
        "creation_id": cid,
        "access_token": TOKEN,
    })
    pid = pub.get("id")
    if not pid:
        print("LỖI publish:", pub, file=sys.stderr)
        return 1

    posted.append({
        "id": nxt["id"],
        "ig_media_id": pid,
        "at": time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime()),
    })
    json.dump(posted, open(posted_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"✅ ĐÃ ĐĂNG {nxt['id']} — Media ID {pid}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
