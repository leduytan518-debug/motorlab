import json
import os
import sqlite3
import urllib.request
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "studylab.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    # 1. Bảng Chuyên đề (thay cho vehicles)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS topics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT,
            title TEXT,
            subtitle TEXT,
            summary TEXT,
            key_points TEXT,
            exam_weight TEXT
        )
    """)

    # 2. Bảng Ngân hàng câu hỏi trắc nghiệm (thay cho faults)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chapter TEXT,
            question TEXT UNIQUE,
            option_a TEXT,
            option_b TEXT,
            option_c TEXT,
            option_d TEXT,
            correct_answer TEXT,
            explanation TEXT
        )
    """)

    # 3. Bảng Kho khái niệm & Phạm trù (thay cho parts)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS concepts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chapter TEXT,
            name TEXT,
            definition TEXT,
            relation TEXT,
            exam_tip TEXT,
            note TEXT
        )
    """)

    # 4. Bảng Phương pháp & Mẹo làm bài (thay cho tools)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS methods (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            group_name TEXT,
            name TEXT,
            usage TEXT,
            how_to_apply TEXT
        )
    """)

    # 5. Bảng Cấu trúc đề & Phân bổ điểm (thay cho prices)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS exam_structure (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chapter TEXT,
            topic_name TEXT,
            question_count TEXT,
            score_weight TEXT,
            note TEXT
        )
    """)

    # Nạp dữ liệu mặc định nếu mới khởi tạo
    if cur.execute("SELECT COUNT(*) FROM topics").fetchone()[0] == 0:
        cur.executemany("INSERT INTO topics (category, title, subtitle, summary, key_points, exam_weight) VALUES (?,?,?,?,?,?)", [
            ("Chương 1", "Triết học và Vấn đề cơ bản của Triết học", "Khái luận Triết học Mác - Lênin", "Nắm vững nguồn gốc triết học, hai mặt vấn đề cơ bản của triết học (Bản thể luận & Nhận thức luận).", "Chủ nghĩa duy vật, Chủ nghĩa duy tâm, Thuyết khả tri, Bất khả tri", "Chiếm 15% đề thi"),
            ("Chương 2", "Vật chất và Ý thức", "Chủ nghĩa duy vật biện chứng", "Định nghĩa vật chất của V.I.Lênin, nguồn gốc - bản chất của ý thức và mối quan hệ biện chứng giữa vật chất và ý thức.", "Thực tại khách quan, Lao động & Ngôn ngữ, Tôn trọng khách quan", "Chiếm 25% đề thi"),
            ("Chương 2", "Hai nguyên lý & Sáu cặp phạm trù", "Phép biện chứng duy vật", "Nguyên lý về mối liên hệ phổ biến, Nguyên lý về sự phát triển và 6 cặp phạm trù cơ bản.", "Quan điểm toàn diện, Lịch sử - cụ thể, Cái chung - Cái riêng, Nguyên nhân - Kết quả", "Chiếm 20% đề thi"),
            ("Chương 2", "Ba quy luật cơ bản của Phép biện chứng", "Hạt nhân của phép biện chứng", "Quy luật Lượng - Chất (cách thức), Quy luật Mâu thuẫn (nguồn gốc, động lực), Quy luật Phủ định của phủ định (khuynh hướng).", "Độ, Điểm nút, Bước nhảy, Thống nhất và đấu tranh giữa các mặt đối lập", "Chiếm 20% đề thi"),
            ("Chương 3", "Học thuyết Hình thái Kinh tế - Xã hội", "Chủ nghĩa duy vật lịch sử", "Quy luật Lực lượng sản xuất và Quan hệ sản xuất; Mối quan hệ biện chứng giữa Cơ sở hạ tầng và Kiến trúc thượng tầng.", "Công cụ lao động, Lực lượng sản xuất quyết định QHSX, CSHT quyết định KTTT", "Chiếm 15% đề thi"),
            ("Chương 3", "Giai cấp, Nhà nước & Con người", "Chủ nghĩa duy vật lịch sử", "Nguồn gốc giai cấp, bản chất nhà nước, mối quan hệ Tồn tại xã hội - Ý thức xã hội và bản chất con người.", "Tổng hòa các quan hệ xã hội, Quần chúng nhân dân là chủ thể lịch sử", "Chiếm 5% đề thi"),
        ])

    if cur.execute("SELECT COUNT(*) FROM questions").fetchone()[0] == 0:
        cur.executemany("""
            INSERT OR IGNORE INTO questions (chapter, question, option_a, option_b, option_c, option_d, correct_answer, explanation)
            VALUES (?,?,?,?,?,?,?,?)
        """, [
            ("Chương 1", "Vấn đề cơ bản lớn của mọi triết học, đặc biệt là của triết học hiện đại là gì?", "Quan hệ giữa con người và tự nhiên", "Quan hệ giữa tư duy và tồn tại (giữa ý thức và vật chất)", "Quan hệ giữa lý luận và thực tiễn", "Quan hệ giữa vật chất và vận động", "B", "Theo Ph.Ăngghen, vấn đề cơ bản lớn của mọi triết học là mối quan hệ giữa tư duy và tồn tại."),
            ("Chương 1", "Mặt thứ hai của vấn đề cơ bản của triết học trả lời cho câu hỏi nào?", "Vật chất và ý thức cái nào có trước?", "Cái nào quyết định cái nào?", "Con người có khả năng nhận thức được thế giới hay không?", "Thế giới tồn tại hữu hạn hay vô hạn?", "C", "Mặt thứ nhất (Bản thể luận): cái nào có trước. Mặt thứ hai (Nhận thức luận): con người có nhận thức được thế giới không."),
            ("Chương 2", "Theo V.I.Lênin, thuộc tính chung nhất và quan trọng nhất để phân biệt vật chất với ý thức là gì?", "Vận động không ngừng", "Tồn tại trong không gian và thời gian", "Thực tại khách quan (tồn tại độc lập với ý thức con người)", "Có khối lượng và cấu trúc nguyên tử", "C", "Thực tại khách quan là thuộc tính cơ bản nhất của mọi dạng vật chất."),
            ("Chương 2", "Nguồn gốc xã hội trực tiếp và quan trọng nhất quyết định sự ra đời của ý thức là gì?", "Bộ óc con người và thế giới khách quan", "Lao động và ngôn ngữ", "Sự phát triển của khoa học tự nhiên", "Giao tiếp bầy đàn của loài vượn cổ", "B", "Bộ óc và thế giới khách quan là nguồn gốc tự nhiên; Lao động và ngôn ngữ là nguồn gốc xã hội."),
            ("Chương 2", "Quy luật nào chỉ ra 'nguồn gốc, động lực' cơ bản của mọi sự vận động và phát triển?", "Quy luật Lượng - Chất", "Quy luật Thống nhất và đấu tranh các mặt đối lập (Mâu thuẫn)", "Quy luật Phủ định của phủ định", "Quy luật QHSX phù hợp với trình độ LLSX", "B", "Mâu thuẫn = Nguồn gốc/động lực; Lượng - Chất = Cách thức; Phủ định của phủ định = Khuynh hướng."),
            ("Chương 3", "Yếu tố nào được coi là động nhất, cách mạng nhất trong Lực lượng sản xuất?", "Người lao động", "Đối tượng lao động", "Công cụ lao động", "Tư liệu sản xuất", "C", "Công cụ lao động luôn cải tiến không ngừng, là yếu tố động nhất và cách mạng nhất trong LLSX."),
        ])

    if cur.execute("SELECT COUNT(*) FROM concepts").fetchone()[0] == 0:
        cur.executemany("INSERT INTO concepts (chapter, name, definition, relation, exam_tip, note) VALUES (?,?,?,?,?,?)", [
            ("Chương 2", "Phạm trù Vật chất", "Phạm trù triết học dùng để chỉ thực tại khách quan được đem lại cho con người trong cảm giác.", "Đối lập và quyết định Ý thức", "Từ khóa: Thực tại khách quan", "Luôn chọn đáp án có cụm từ 'Thực tại khách quan' khi hỏi định nghĩa vật chất của Lênin."),
            ("Chương 2", "Lao động & Ngôn ngữ", "Hai yếu tố tạo thành nguồn gốc xã hội trực tiếp quyết định sự hình thành và phát triển của ý thức.", "Thuộc học thuyết về Ý thức", "Từ khóa: Nguồn gốc xã hội", "Nếu đề hỏi 'nguồn gốc tự nhiên' thì chọn Bộ óc người; hỏi 'nguồn gốc xã hội' thì chọn Lao động & Ngôn ngữ."),
            ("Chương 2", "Độ - Điểm nút - Bước nhảy", "Ba khái niệm cốt lõi giải thích cách thức vận động trong Quy luật chuyển hóa từ Lượng thành Chất.", "Thuộc Quy luật Lượng - Chất", "Từ khóa: Cách thức phát triển", "Chưa đổi chất = Độ; Thời điểm đủ lượng = Điểm nút; Quá trình biến đổi chất = Bước nhảy."),
            ("Chương 2", "Thực tiễn", "Toàn bộ hoạt động vật chất - cảm tính, có tính lịch sử - xã hội của con người nhằm cải tạo tự nhiên và xã hội.", "Cơ sở, động lực, mục đích của nhận thức", "Từ khóa: Hoạt động vật chất", "Hoạt động sản xuất vật chất là hình thức cơ bản và quan trọng nhất của thực tiễn."),
            ("Chương 3", "Lực lượng sản xuất (LLSX)", "Sự kết hợp giữa người lao động với tư liệu sản xuất, tạo ra sức sản xuất và năng lực thực tiễn.", "Quyết định Quan hệ sản xuất (QHSX)", "Từ khóa: Nền tảng vật chất", "Người lao động là nhân tố hàng đầu; Công cụ lao động là yếu tố động nhất, cách mạng nhất."),
            ("Chương 3", "Cơ sở hạ tầng (CSHT)", "Toàn bộ những quan hệ sản xuất của một xã hội trong sự vận động hiện thực của chúng hợp thành cơ cấu kinh tế.", "Quyết định Kiến trúc thượng tầng (KTTT)", "Từ khóa: Quan hệ sản xuất (Kinh tế)", "Đừng nhầm CSHT trong triết học với điện, đường, trường, trạm! CSHT trong triết học là Kinh tế (các QHSX)."),
        ])

    if cur.execute("SELECT COUNT(*) FROM methods").fetchone()[0] == 0:
        cur.executemany("INSERT INTO methods (group_name, name, usage, how_to_apply) VALUES (?,?,?,?)", [
            ("Mẹo nhận diện", "Phân biệt Duy vật và Duy tâm", "Dùng cho các câu hỏi Chương 1 nhận diện trường phái triết học.", "Hễ đề nhắc 'Vật chất/Tự nhiên có trước' -> Duy vật. Nhắc 'Ý thức/Tinh thần/Thượng đế/Ý niệm tuyệt đối có trước' -> Duy tâm."),
            ("Mẹo nhận diện", "Phân biệt Biện chứng và Siêu hình", "Dùng cho câu hỏi phương pháp luận Chương 1 & Chương 2.", "Thấy 'Cô lập, tĩnh tại, bất biến, chỉ thấy cây không thấy rừng' -> Siêu hình. Thấy 'Liên hệ, vận động, chuyển hóa, phát triển' -> Biện chứng."),
            ("Mẹo từ khóa", "3 Quy luật cơ bản (Chương 2)", "Tránh nhầm lẫn vai trò của 3 quy luật trong Phép biện chứng duy vật.", "Hỏi 'Cách thức' -> Chọn Lượng - Chất. Hỏi 'Nguồn gốc, động lực, hạt nhân' -> Chọn Mâu thuẫn. Hỏi 'Khuynh hướng, xoáy ốc' -> Chọn Phủ định của phủ định."),
            ("Mẹo từ khóa", "Tránh bẫy Cơ sở hạ tầng (Chương 3)", "Câu bẫy kinh điển nhất trong các đề thi trắc nghiệm Triết học.", "Nếu đáp án liệt kê 'đường sá, cầu cống, nhà máy' là Cơ sở hạ tầng -> Loại ngay! CSHT trong Triết học gồm: QHSX thống trị, QHSX tàn dư và QHSX mầm mống."),
            ("Phương pháp luận", "Nguyên tắc Toàn diện & Lịch sử - Cụ thể", "Dùng cho câu hỏi rút ra bài học từ Nguyên lý mối liên hệ phổ biến.", "Đề hỏi cơ sở lý luận của 'Quan điểm toàn diện' -> Chọn ngay Nguyên lý về mối liên hệ phổ biến."),
            ("Phương pháp luận", "Nguyên tắc Khách quan", "Dùng cho câu hỏi rút ra từ mối quan hệ giữa Vật chất và Ý thức.", "Xuất phát từ thực tế khách quan, tôn trọng quy luật khách quan đồng thời phát huy tính năng động chủ quan. Bệnh 'chủ quan duy ý chí' là do vi phạm nguyên tắc này."),
        ])

    if cur.execute("SELECT COUNT(*) FROM exam_structure").fetchone()[0] == 0:
        cur.executemany("INSERT INTO exam_structure (chapter, topic_name, question_count, score_weight, note) VALUES (?,?,?,?,?)", [
            ("Chương 1", "Khái luận về Triết học và Triết học Mác - Lênin", "6 - 8 câu", "1.5 - 2.0 điểm", "Tập trung vào Vấn đề cơ bản của triết học và các hình thức Chủ nghĩa duy vật."),
            ("Chương 2", "Vật chất, Ý thức và mối quan hệ biện chứng", "8 - 10 câu", "2.0 - 2.5 điểm", "Định nghĩa vật chất của Lênin, nguồn gốc/bản chất ý thức và nguyên tắc khách quan."),
            ("Chương 2", "2 Nguyên lý, 6 Cặp phạm trù & 3 Quy luật cơ bản", "12 - 15 câu", "3.0 - 3.75 điểm", "Phần trọng tâm nhất của đề thi; thường hỏi vận dụng ca dao, tục ngữ vào quy luật."),
            ("Chương 2", "Thực tiễn và Lý luận nhận thức", "4 - 5 câu", "1.0 - 1.25 điểm", "Ba hình thức thực tiễn và con đường biện chứng của sự nhận thức (Trực quan sinh động -> Tư duy trừu tượng)."),
            ("Chương 3", "Hình thái Kinh tế - Xã hội (LLSX - QHSX, CSHT - KTTT)", "6 - 8 câu", "1.5 - 2.0 điểm", "Quy luật sự phù hợp của QHSX với trình độ phát triển của LLSX."),
            ("Chương 3", "Giai cấp, Nhà nước, Ý thức xã hội & Con người", "4 câu", "1.0 điểm", "Tính độc lập tương đối của ý thức xã hội và bản chất con người."),
        ])

    conn.commit()
    conn.close()

def generate_questions_with_ai(chapter="Chương 2", count=5, custom_api_key=""):
    """Gọi trực tiếp Google Gemini API để tự động sinh thêm câu hỏi mới vào ngân hàng"""
    api_key = custom_api_key.strip() or os.environ.get("GEMINI_API_KEY", "").strip()
    if not api_key:
        return {"success": False, "message": "Hãy dán mã GEMINI_API_KEY vào ô bên cạnh để AI tạo câu hỏi mới!"}

    prompt = f"""
    Hãy đóng vai giảng viên đại học môn Triết học Mác - Lênin.
    Tạo ra {count} câu hỏi trắc nghiệm khách quan mới (không trùng lặp), chuẩn giáo trình thuộc {chapter}.
    Trả về KẾT QUẢ DUY NHẤT là một mảng JSON chuẩn:
    [
      {{
        "chapter": "{chapter}",
        "question": "Nội dung câu hỏi...",
        "option_a": "Phương án A...",
        "option_b": "Phương án B...",
        "option_c": "Phương án C...",
        "option_d": "Phương án D...",
        "correct_answer": "A",
        "explanation": "Giải thích ngắn gọn..."
      }}
    ]
    """
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"responseMimeType": "application/json"}
    }
    try:
        req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(req, timeout=25) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            items = json.loads(result["candidates"][0]["content"]["parts"][0]["text"])
            conn = get_connection()
            cur = conn.cursor()
            added = 0
            for item in items:
                cur.execute("""
                    INSERT OR IGNORE INTO questions (chapter, question, option_a, option_b, option_c, option_d, correct_answer, explanation)
                    VALUES (?,?,?,?,?,?,?,?)
                """, (
                    item.get("chapter", chapter),
                    item.get("question", "").strip(),
                    item.get("option_a", "").strip(),
                    item.get("option_b", "").strip(),
                    item.get("option_c", "").strip(),
                    item.get("option_d", "").strip(),
                    item.get("correct_answer", "A").strip().upper()[:1],
                    item.get("explanation", "").strip()
                ))
                if cur.rowcount > 0:
                    added += 1
            conn.commit()
            conn.close()
            return {"success": True, "message": f"Đã tự động thêm {added} câu hỏi mới vào ngân hàng!"}
    except Exception as e:
        return {"success": False, "message": f"Lỗi gọi AI: {str(e)}"}