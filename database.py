"""SQLite database setup and sample data for the vehicle technical library."""
from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "instance" / "garage_library.db"


def get_connection():
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def init_db():
    with get_connection() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS vehicles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                vehicle_type TEXT NOT NULL,
                brand TEXT NOT NULL,
                model TEXT NOT NULL,
                year INTEGER,
                engine TEXT,
                fuel_system TEXT,
                description TEXT
            );

            CREATE TABLE IF NOT EXISTS faults (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                vehicle_type TEXT NOT NULL,
                model TEXT NOT NULL DEFAULT 'Nhiều dòng xe',
                code TEXT,
                symptom TEXT NOT NULL,
                causes TEXT NOT NULL,
                checks TEXT NOT NULL,
                solution TEXT NOT NULL,
                severity TEXT NOT NULL DEFAULT 'Trung bình'
            );

            CREATE TABLE IF NOT EXISTS parts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                vehicle_type TEXT NOT NULL,
                name TEXT NOT NULL,
                compatible TEXT NOT NULL,
                function TEXT NOT NULL,
                price_min INTEGER,
                price_max INTEGER,
                price_note TEXT
            );

            CREATE TABLE IF NOT EXISTS tools (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                usage TEXT NOT NULL,
                caution TEXT
            );

            CREATE TABLE IF NOT EXISTS repair_prices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                vehicle_type TEXT NOT NULL,
                job TEXT NOT NULL,
                price_min INTEGER,
                price_max INTEGER,
                note TEXT
            );
            """
        )

        # Add starter data only on the first run. These are learning/demo records,
        # not verified live vehicle specifications or market quotations.
        if conn.execute("SELECT COUNT(*) FROM vehicles").fetchone()[0] == 0:
            conn.executemany(
                """INSERT INTO vehicles
                   (vehicle_type, brand, model, year, engine, fuel_system, description)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                [
                    ("oto", "Toyota", "Vios", 2022, "1.5L xăng", "Phun xăng điện tử", "Mẫu ô tô du lịch phổ biến. Thông số cụ thể cần đối chiếu theo phiên bản và thị trường."),
                    ("oto", "Honda", "City", 2023, "1.5L xăng", "Phun xăng điện tử", "Sedan cỡ nhỏ; dữ liệu mẫu để thử chức năng tra cứu."),
                    ("oto", "Ford", "Ranger", 2022, "2.0L diesel", "Common Rail", "Bán tải; cần chọn đúng phiên bản động cơ khi tra cứu phụ tùng."),
                    ("xemay", "Honda", "Wave Alpha", 2023, "110 cc", "Phun xăng điện tử tùy phiên bản/thị trường", "Xe số phổ thông; hãy kiểm tra đúng phiên bản trước khi mua phụ tùng."),
                    ("xemay", "Yamaha", "Exciter 155", 2023, "155 cc", "Phun xăng điện tử", "Xe côn tay; thông số và phụ tùng có thể khác theo đời xe."),
                    ("xemay", "Honda", "Air Blade 160", 2023, "156,9 cc", "Phun xăng điện tử", "Xe tay ga; cần đối chiếu mã phụ tùng theo số khung/phiên bản."),
                ],
            )

        if conn.execute("SELECT COUNT(*) FROM faults").fetchone()[0] == 0:
            conn.executemany(
                """INSERT INTO faults
                   (vehicle_type, model, code, symptom, causes, checks, solution, severity)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                [
                    ("oto", "Nhiều dòng ô tô", "P0300", "Động cơ rung, bỏ máy hoặc tăng tốc yếu", "Có thể liên quan đến bugi, bobin đánh lửa, kim phun, áp suất nhiên liệu hoặc độ kín buồng đốt.", "Đọc mã lỗi bằng máy chẩn đoán; kiểm tra dữ liệu misfire và lịch sử bảo dưỡng. Không tự tháo hệ thống nhiên liệu khi chưa có dụng cụ và kiến thức phù hợp.", "Khoanh vùng theo dữ liệu chẩn đoán rồi kiểm tra từng hệ thống. Thay linh kiện chỉ sau khi xác định nguyên nhân.", "Cao"),
                    ("oto", "Nhiều dòng ô tô", "P0128", "Động cơ lâu đạt nhiệt độ làm việc", "Có thể do van hằng nhiệt kẹt mở, cảm biến nhiệt độ nước làm mát hoặc hệ thống làm mát.", "Kiểm tra mức nước làm mát khi động cơ đã nguội; đọc nhiệt độ ECT trên máy chẩn đoán và kiểm tra rò rỉ.", "Sửa chữa hệ thống làm mát theo tài liệu sửa chữa đúng mẫu xe. Không mở nắp két nước khi động cơ nóng.", "Trung bình"),
                    ("oto", "Nhiều dòng ô tô", "Không xác định", "Xe khó khởi động hoặc không khởi động", "Có thể do ắc quy yếu, máy khởi động, hệ thống đánh lửa, cấp nhiên liệu hoặc chống trộm.", "Quan sát đèn báo, kiểm tra tình trạng ắc quy và nghe tiếng máy khởi động. Đọc mã lỗi nếu có thiết bị phù hợp.", "Kiểm tra theo quy trình của nhà sản xuất; đưa xe đến kỹ thuật viên nếu có mùi nhiên liệu, khói hoặc dây điện nóng bất thường.", "Cao"),
                    ("xemay", "Nhiều xe máy FI", "Không xác định", "Xe FI khó nổ, nhất là khi để lâu", "Có thể do ắc quy yếu, bugi mòn, lọc gió bẩn, áp suất nhiên liệu không phù hợp hoặc cảm biến/bơm xăng.", "Kiểm tra điện áp ắc quy, bugi và lọc gió theo sách hướng dẫn; quan sát đèn FI. Không tự mở đường ống xăng áp suất cao.", "Đọc mã lỗi bằng thiết bị tương thích, đo kiểm theo tài liệu sửa chữa và chỉ thay chi tiết sau khi xác định nguyên nhân.", "Trung bình"),
                    ("xemay", "Nhiều xe máy", "Không xác định", "Xe bị hụt ga hoặc giật khi tăng tốc", "Có thể do lọc gió, bugi, kim phun, nhiên liệu, truyền động hoặc cảm biến bướm ga.", "Ghi nhận điều kiện xuất hiện lỗi; kiểm tra bảo dưỡng cơ bản và đọc mã lỗi FI nếu xe có hệ thống này.", "Kiểm tra theo từng hệ thống. Với xe tay ga, cần phân biệt lỗi động cơ và lỗi bộ truyền động CVT.", "Trung bình"),
                    ("xemay", "Nhiều xe máy", "Không xác định", "Đèn báo FI sáng bất thường", "ECU có thể ghi nhận lỗi ở cảm biến, cơ cấu chấp hành, nguồn điện hoặc dây dẫn.", "Không đoán lỗi chỉ dựa vào đèn báo. Dùng thiết bị đọc lỗi phù hợp với hãng và đời xe; kiểm tra giắc cắm, dây dẫn theo sơ đồ.", "Ghi lại mã lỗi trước khi xóa; xử lý nguyên nhân rồi kiểm tra lại. Không nối tắt chân giắc nếu không có sơ đồ chính xác.", "Cao"),
                ],
            )

        if conn.execute("SELECT COUNT(*) FROM parts").fetchone()[0] == 0:
            conn.executemany(
                """INSERT INTO parts
                   (vehicle_type, name, compatible, function, price_min, price_max, price_note)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                [
                    ("oto", "Bugi đánh lửa", "Ô tô động cơ xăng; phải chọn đúng mã", "Tạo tia lửa đốt cháy hòa khí trong xi-lanh.", 0, 0, "Chưa có báo giá được xác minh; phụ thuộc mã bugi và thương hiệu."),
                    ("oto", "Lọc dầu động cơ", "Ô tô; chọn theo mã động cơ và đời xe", "Lọc cặn bẩn trong dầu bôi trơn.", 0, 0, "Chưa có báo giá được xác minh."),
                    ("oto", "Cảm biến oxy (O2)", "Một số động cơ xăng; cần đúng chuẩn giắc và mã", "Gửi thông tin về lượng oxy trong khí xả cho ECU điều khiển hòa khí.", 0, 0, "Chưa có báo giá được xác minh."),
                    ("oto", "Kim phun nhiên liệu", "Tùy hệ thống phun xăng/diesel và mã động cơ", "Phun nhiên liệu theo lệnh điều khiển, đúng lượng và thời điểm.", 0, 0, "Giá thay đổi lớn theo loại phun và mẫu xe."),
                    ("xemay", "Bugi", "Xe máy; chọn đúng nhiệt trị và mã bugi", "Tạo tia lửa đốt cháy hòa khí trong động cơ.", 0, 0, "Chưa có báo giá được xác minh."),
                    ("xemay", "Kim phun FI", "Xe máy phun xăng điện tử; chọn đúng mã", "Phun nhiên liệu dạng sương theo tín hiệu điều khiển ECU.", 0, 0, "Chưa có báo giá được xác minh."),
                    ("xemay", "Bơm xăng điện", "Xe máy FI; cần đúng áp suất và giắc điện", "Cấp nhiên liệu từ bình đến hệ thống phun theo áp suất thiết kế.", 0, 0, "Chưa có báo giá được xác minh."),
                    ("xemay", "Lọc gió", "Xe máy; đối chiếu đời xe và kiểu hộp lọc", "Lọc bụi trong không khí trước khi đi vào động cơ.", 0, 0, "Chưa có báo giá được xác minh."),
                ],
            )

        if conn.execute("SELECT COUNT(*) FROM tools").fetchone()[0] == 0:
            conn.executemany(
                "INSERT INTO tools (name, category, usage, caution) VALUES (?, ?, ?, ?)",
                [
                    ("Bộ khẩu và cần siết", "Dụng cụ cơ khí", "Tháo/lắp bu-lông, đai ốc nhiều kích cỡ.", "Dùng đúng cỡ; không dùng lực quá mức gây tuôn ren."),
                    ("Cờ lê lực", "Dụng cụ đo/siết", "Siết bu-lông theo mô-men quy định của nhà sản xuất.", "Tra thông số đúng mẫu xe; không tự ước lượng mô-men."),
                    ("Đồng hồ vạn năng", "Dụng cụ điện", "Đo điện áp, điện trở và kiểm tra thông mạch.", "Chọn đúng thang đo; không đo điện trở khi mạch đang có điện."),
                    ("Máy chẩn đoán OBD-II", "Thiết bị chẩn đoán ô tô", "Đọc/xóa mã lỗi và xem dữ liệu xe hỗ trợ chuẩn OBD-II.", "Không phải xe/đời xe nào cũng hỗ trợ đầy đủ chức năng; không xóa lỗi trước khi ghi nhận."),
                    ("Máy chẩn đoán FI xe máy", "Thiết bị chẩn đoán xe máy", "Đọc mã lỗi và dữ liệu trên các dòng xe tương thích.", "Phải đúng hãng, đời xe và giao thức; làm theo hướng dẫn thiết bị."),
                    ("Thước lá", "Dụng cụ đo", "Đo khe hở xupap hoặc khe hở kỹ thuật theo tài liệu.", "Đo khi động cơ ở điều kiện nhiệt độ được nhà sản xuất yêu cầu."),
                    ("Đồng hồ đo áp suất lốp", "Dụng cụ kiểm tra", "Kiểm tra áp suất lốp nguội.", "Bơm theo mức khuyến nghị trên xe hoặc sách hướng dẫn."),
                ],
            )

        if conn.execute("SELECT COUNT(*) FROM repair_prices").fetchone()[0] == 0:
            conn.executemany(
                "INSERT INTO repair_prices (vehicle_type, job, price_min, price_max, note) VALUES (?, ?, ?, ?, ?)",
                [
                    ("oto", "Kiểm tra bằng máy chẩn đoán", 0, 0, "Cần khảo sát gara địa phương; chưa nhập giá xác minh."),
                    ("oto", "Thay dầu và lọc dầu", 0, 0, "Phụ thuộc dung tích dầu, loại dầu, lọc và công thay."),
                    ("oto", "Kiểm tra hệ thống phanh", 0, 0, "Phụ thuộc tình trạng và cấu hình phanh."),
                    ("xemay", "Kiểm tra lỗi FI", 0, 0, "Phụ thuộc thiết bị, dòng xe và gara."),
                    ("xemay", "Thay dầu động cơ", 0, 0, "Phụ thuộc dung tích và loại dầu."),
                    ("xemay", "Kiểm tra/thay bugi", 0, 0, "Phụ thuộc mã bugi và mẫu xe."),
                ],
            )
