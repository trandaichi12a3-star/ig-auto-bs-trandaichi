# Instagram Reels auto-post (GitHub Actions)

Tự động đăng Reel cho kênh **@ths.bs.trandaichi** — máy tắt vẫn đăng.

## Cách hoạt động
- `videos/` — các file video (đặt tên không dấu). Instagram tải về qua link raw công khai.
- `queue.json` — hàng đợi Reel ĐÃ DUYỆT (id + tên video + caption), đăng theo thứ tự.
- `posted.json` — Reel đã đăng (Actions tự commit lại sau mỗi lần chạy).
- `post_next.py` — lấy Reel chưa đăng đầu tiên → tạo container → chờ Instagram xử lý xong → publish.
- `.github/workflows/post.yml` — cron **19:30 giờ VN** mỗi ngày (12:30 UTC). 1 Reel/ngày.

## Secret cần đặt trên GitHub (Settings → Secrets and variables → Actions)
- `IG_USER_ID` — ID tài khoản Instagram (đã đặt).
- `IG_ACCESS_TOKEN` — token dài hạn 60 ngày (**cần gia hạn trước khi hết hạn**).

## Thêm Reel mới
1. Copy video (không dấu, < 100MB) vào `videos/`.
2. Thêm 1 mục vào `REELS` trong `build_queue.py` (id + video + caption).
3. `python3 build_queue.py` → sinh lại `queue.json`.
4. `git add -A && git commit && git push`. Reel mới nối vào cuối hàng đợi.

## Test thủ công
Tab **Actions** trên GitHub → chọn workflow → **Run workflow** (đăng ngay 1 Reel).

## Đang hoãn
- Reel "loãng xương/lưng còng": video gốc 239MB > giới hạn 100MB → cần nén 1080p.
- Reel "ngón tay lò xo": chưa có video trong kho.

> ⚠️ Token KHÔNG nằm trong code — chỉ ở GitHub Secret (mã hóa). Repo công khai chỉ để Instagram tải video.
