#!/usr/bin/env python3
"""Sinh queue.json cho auto-post Instagram.
Thêm Reel mới: thêm 1 dict vào REELS (id, video, caption) → chạy `python3 build_queue.py`.
- id: mã duy nhất (đừng trùng), dùng để đánh dấu đã đăng ở posted.json.
- video: TÊN FILE trong thư mục videos/ (đặt tên không dấu).
- caption: caption đầy đủ (kèm hashtag ở cuối).
Bài đã đăng rồi (posted.json) sẽ KHÔNG đăng lại dù còn trong queue.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))

REELS = [
    {
        "id": "reel01-phuc-hoi",
        "video": "reel01-phuc-hoi-khop-goi.mp4",
        "caption": """Có những bước đi bình thường với ta, lại là cả một hành trình với người khác.

Nhiều cô chú đến phòng khám với nỗi sợ: "Rồi có đi lại được như xưa không bác sĩ?"

Phục hồi cơ xương khớp hiếm khi là phép màu một ngày. Nó là kiên trì mỗi ngày một chút: đúng bài tập, đúng liều vận động, và không bỏ cuộc giữa chừng.

Điều tôi mong bạn mang về: đau kéo dài KHÔNG có nghĩa là hết cách. Nhưng càng để lâu, đường về càng xa. Đi khám sớm để biết mình đang ở đâu.

— ThS.BS Trần Đại Chí, chuyên khoa Chấn thương Chỉnh hình – Cơ Xương Khớp
Thông tin mang tính chia sẻ kiến thức, không thay thế thăm khám trực tiếp.
📩 Nhắn Zalo 0886 138 848 để được tư vấn.

#coxuongkhop #vatlytrilieu #phuchoichucnang #drchi #bacsicoxuongkhop #suckhoexuongkhop""",
    },
    {
        "id": "reel03-khong-di-boi",
        "video": "reel03-khong-di-boi-tap-gi.mp4",
        "caption": """"Bác sĩ bảo đi bơi tốt cho khớp, mà tôi không biết bơi thì sao?"

Câu hỏi tôi nghe hoài. Tin vui: bơi không phải lựa chọn duy nhất.

Nguyên tắc chung với khớp đang đau là ưu tiên vận động ÍT dồn tải: đi bộ trên nền phẳng, đạp xe nhẹ, các bài tập trong nước (đi bộ dưới hồ), tập mạnh nhóm cơ quanh khớp. Cơ khỏe thì khớp được "gánh" đỡ hơn.

Quan trọng là chọn bài phù hợp với tình trạng của bạn — tập sai hoặc quá sức đôi khi làm đau thêm. Nên hỏi bác sĩ/kỹ thuật viên trước khi bắt đầu.

— ThS.BS Trần Đại Chí, chuyên khoa Chấn thương Chỉnh hình – Cơ Xương Khớp
Thông tin mang tính chia sẻ kiến thức, không thay thế thăm khám trực tiếp.
📩 Muốn nhận bài tập tại nhà phù hợp? Nhắn Zalo 0886 138 848.

#vatlytrilieu #coxuongkhop #thoaihoakhopgoi #vandong #drchi #suckhoexuongkhop""",
    },
    {
        "id": "reel06-dau-vai",
        "video": "reel06-dau-vai-keo-dai.mp4",
        "caption": """Đau vai vài hôm rồi tự hết thì thường không đáng ngại. Nhưng đau vai KÉO DÀI, mãi không dứt, lại là chuyện khác.

Vai là khớp vận động linh hoạt bậc nhất cơ thể, nên cũng dễ "trục trặc": viêm gân, viêm quanh khớp vai ("vai đông cứng"), rách gân chóp xoay… Mỗi nguyên nhân có hướng xử lý khác nhau, nên "đau vai" chung chung thì không thể tự đoán.

Dấu hiệu nên đi khám: đau kéo dài trên vài tuần, hạn chế đưa tay lên cao, đau về đêm mất ngủ, hoặc yếu tay. Khám đúng nguyên nhân thì phần lớn cải thiện tốt với điều trị bảo tồn.

— ThS.BS Trần Đại Chí, chuyên khoa Chấn thương Chỉnh hình – Cơ Xương Khớp
Thông tin mang tính chia sẻ kiến thức, không thay thế thăm khám trực tiếp.
📩 Đau vai lâu chưa khỏi? Nhắn Zalo 0886 138 848.

#dauvai #vaidongcung #coxuongkhop #vatlytrilieu #drchi #suckhoexuongkhop""",
    },
    {
        "id": "reel07-top3-prp",
        "video": "reel07-top3-prp.mp4",
        "caption": """PRP (huyết tương giàu tiểu cầu) đang được nhắc nhiều — nhưng không phải ai cũng cần, và cũng không phải "thần dược".

PRP là kỹ thuật lấy chính máu của bạn, tách phần giàu tiểu cầu rồi tiêm vào vùng tổn thương, với mong muốn hỗ trợ quá trình lành mô. Một số tình trạng thường được cân nhắc: thoái hóa khớp gối giai đoạn phù hợp, một số bệnh lý gân mạn tính (viêm điểm bám gân)…

Điều quan trọng: hiệu quả tùy từng người, từng giai đoạn bệnh, và PRP chỉ là MỘT trong nhiều lựa chọn. Có hợp với bạn hay không phải qua thăm khám mới biết — đừng làm chỉ vì thấy người khác làm.

— ThS.BS Trần Đại Chí, chuyên khoa Chấn thương Chỉnh hình – Cơ Xương Khớp
Thông tin mang tính chia sẻ kiến thức, không thay thế thăm khám trực tiếp.
📩 Muốn biết trường hợp của mình có phù hợp PRP? Nhắn Zalo 0886 138 848.

#prp #yhoctaitao #thoaihoakhopgoi #coxuongkhop #tiemkhop #drchi""",
    },
    {
        "id": "reel08-pickleball",
        "video": "reel08-pickleball.mp4",
        "caption": """Pickleball đang là môn "quốc dân" — vui, dễ chơi, nhưng phòng khám cũng bắt đầu gặp nhiều ca chấn thương vì môn này.

3 nhóm hay gặp:
• Khuỷu tay (kiểu "tennis elbow") do vung vợt lặp lại
• Cổ chân, gối do đổi hướng, dừng đột ngột
• Vai do với bóng quá tầm

Không phải để bạn sợ mà bỏ chơi — mà để chơi thông minh hơn: khởi động kỹ, tăng cường độ từ từ, dùng giày phù hợp, và nghe cơ thể. Đau nhẹ nghỉ vài hôm không đỡ, hoặc sưng/yếu khớp — nên đi khám sớm thay vì cố chơi tiếp.

— ThS.BS Trần Đại Chí, chuyên khoa Chấn thương Chỉnh hình – Cơ Xương Khớp
Thông tin mang tính chia sẻ kiến thức, không thay thế thăm khám trực tiếp.
📩 Chấn thương thể thao? Nhắn Zalo 0886 138 848.

#pickleball #chanthuongthethao #tenniselbow #coxuongkhop #drchi #suckhoexuongkhop""",
    },
    {
        "id": "reel09-gout",
        "video": "reel09-gout.mp4",
        "caption": """Nhiều người nghĩ gout chỉ là "đau khớp ngón chân vài hôm rồi hết". Đó là hiểu lầm khiến bệnh âm thầm nặng lên.

Cơn đau gout cấp qua đi không có nghĩa là bệnh đã khỏi. Nếu acid uric trong máu vẫn cao kéo dài mà không kiểm soát, tinh thể urat có thể tiếp tục lắng đọng — về lâu dài liên quan đến nổi cục tophi, tổn thương khớp, và ảnh hưởng đến thận.

Vì vậy điều trị gout không chỉ là cắt cơn đau, mà là quản lý lâu dài: chế độ ăn, lối sống, và theo dõi acid uric theo hướng dẫn của bác sĩ. Đừng đợi cơn đau tiếp theo mới lo.

— ThS.BS Trần Đại Chí, chuyên khoa Chấn thương Chỉnh hình – Cơ Xương Khớp
Thông tin mang tính chia sẻ kiến thức, không thay thế thăm khám trực tiếp.
📩 Bị gout tái đi tái lại? Nhắn Zalo 0886 138 848.

#gout #acuric #coxuongkhop #suckhoe #drchi #suckhoexuongkhop""",
    },
    {
        "id": "reel04-tiem-noi-khop",
        "video": "reel04-tiem-noi-khop.mp4",
        "caption": """"Nghe nói tiêm khớp nhiều là hư khớp, có đúng không bác sĩ?"

Nỗi lo rất phổ biến, và câu trả lời nằm ở chỗ: tiêm cái gì, đúng chỉ định không, ai tiêm.

Tiêm nội khớp là một công cụ điều trị — như con dao, dùng đúng thì hữu ích, dùng bừa mới hại. Vấn đề thường không nằm ở "mũi tiêm", mà ở việc lạm dụng, tiêm không đúng loại thuốc, không đúng vị trí, không kiểm soát.

Tại phòng khám, tiêm khớp được thực hiện dưới hướng dẫn siêu âm để vào đúng vị trí, và chỉ khi có chỉ định rõ ràng. Đừng tự đi tiêm ở nơi không kiểm soát, cũng đừng sợ đến mức bỏ qua một lựa chọn điều trị phù hợp — hãy để bác sĩ khám và tư vấn cho đúng ca của bạn.

— ThS.BS Trần Đại Chí, chuyên khoa Chấn thương Chỉnh hình – Cơ Xương Khớp
Thông tin mang tính chia sẻ kiến thức, không thay thế thăm khám trực tiếp.
📩 Còn băn khoăn về tiêm khớp? Nhắn Zalo 0886 138 848.

#tiemkhop #coxuongkhop #yhoctaitao #prp #drchi #suckhoexuongkhop""",
    },
]


def main():
    out = os.path.join(HERE, "queue.json")
    json.dump(REELS, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"Đã ghi {len(REELS)} Reel vào {out}")


if __name__ == "__main__":
    main()
