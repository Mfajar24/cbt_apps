import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user
from werkzeug.utils import secure_filename
import os


app = Flask(__name__)

# Konfigurasi database SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Nama file database untuk soal
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'
db = SQLAlchemy(app)

# Inisialisasi Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Halaman login jika pengguna tidak login

# Model untuk tabel soal ujian
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(200), nullable=False)
    option1 = db.Column(db.String(50), nullable=False)
    option2 = db.Column(db.String(50), nullable=False)
    option3 = db.Column(db.String(50), nullable=False)
    option4 = db.Column(db.String(50), nullable=False)
    answer = db.Column(db.String(50), nullable=False)

# Model Pengguna
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# Model untuk tabel user_profil
class UserProfile(db.Model):
    __tablename__ = 'user_profile'  # Nama tabel di database Anda
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    class_name = db.Column(db.String(50), nullable=False)
    npm = db.Column(db.String(20), nullable=False)
    lecturer_name = db.Column(db.String(100), nullable=False)
    subject_name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"UserProfile('{self.name}', '{self.class_name}')"


# Tentukan lokasi penyimpanan file yang diunggah
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'xls', 'xlsx'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Fungsi untuk memeriksa ekstensi file yang diizinkan
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Fungsi untuk menambahkan soal dari file Excel ke database
def add_questions_from_excel(file_path):
    try:
        # Membaca file Excel menggunakan pandas
        df = pd.read_excel(file_path)
        print("File Excel berhasil dibaca!")
    except Exception as e:
        print(f"Error membaca file Excel: {e}")
        return
    
    # Memeriksa apakah kolom yang dibutuhkan ada dalam data
    required_columns = ['question', 'option1', 'option2', 'option3', 'option4', 'answer']
    if not all(col in df.columns for col in required_columns):
        print(f"File Excel tidak memiliki semua kolom yang diperlukan: {required_columns}")
        return

    # Iterasi melalui setiap baris soal di file Excel dan masukkan ke database
    for _, row in df.iterrows():
        try:
            question = Question(
                question=row['question'],
                option1=row['option1'],
                option2=row['option2'],
                option3=row['option3'],
                option4=row['option4'],
                answer=row['answer']
            )
            db.session.add(question)
            print(f"Menambahkan soal: {row['question']}")
        except Exception as e:
            print(f"Error menambahkan soal ke database: {e}")
            continue  # Melanjutkan jika ada kesalahan dengan soal tertentu

    # Menyimpan perubahan ke database
    try:
        db.session.commit()
        print("Soal berhasil ditambahkan ke database!")
    except Exception as e:
        print(f"Error menyimpan data ke database: {e}")
        db.session.rollback()  # Rollback jika ada error saat commit

# Fungsi untuk membuat semua tabel
def create_tables():
    with app.app_context():
        db.create_all()

# Memastikan bahwa file excel hanya dimuat sekali saat aplikasi dimulai

# Jalankan fungsi ini hanya sekali, saat pertama kali aplikasi dijalankan.
# Panggil fungsi load_questions di luar rute Flask untuk mengimpor soal ke dalam database.
#load_questions()

# Rute untuk halaman mengelola soal
@app.route('/manage_questions', methods=['GET', 'POST'])
@login_required
def manage_questions():
    # Periksa apakah pengguna sudah login dengan Flask-Login
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    if request.method == 'POST':
        action = request.form.get('action')
        question_id = request.form.get('question_id')

        if action == 'delete':
            # Menghapus soal dari database berdasarkan ID
            question = Question.query.get(question_id)
            if question:
                db.session.delete(question)
                db.session.commit()
                flash("Soal berhasil dihapus.", "success")
            else:
                flash("Soal tidak ditemukan.", "danger")
            return redirect(url_for('manage_questions'))
        
        elif action == 'add':
            # Menambahkan soal baru
            question_text = request.form['question']
            option1 = request.form['option1']
            option2 = request.form['option2']
            option3 = request.form['option3']
            option4 = request.form['option4']
            answer = request.form['answer']

            # Validasi input
            if not all([question_text, option1, option2, option3, option4, answer]):
                flash("Semua kolom harus diisi.", "danger")
                return redirect(url_for('manage_questions'))

            new_question = Question(
                question=question_text,
                option1=option1,
                option2=option2,
                option3=option3,
                option4=option4,
                answer=answer
            )
            db.session.add(new_question)
            db.session.commit()
            flash("Soal berhasil ditambahkan.", "success")
            return redirect(url_for('manage_questions'))

    # Mengambil semua soal dari database
    questions = Question.query.all()
    return render_template('manage_questions.html', questions=questions)

@app.route('/edit_question/<int:question_id>', methods=['GET', 'POST'])
@login_required
def edit_question(question_id):

    # Ambil soal berdasarkan question_id
    question = Question.query.get_or_404(question_id)

    if request.method == 'POST':
        # Ambil data dari form dan update soal
        question.question = request.form['question']
        question.option1 = request.form['option1']
        question.option2 = request.form['option2']
        question.option3 = request.form['option3']
        question.option4 = request.form['option4']
        question.answer = request.form['answer']

        db.session.commit()
        flash("Soal berhasil diperbarui.", "success")
        return redirect(url_for('manage_questions'))

    return render_template('edit_question.html', question=question)


@app.route('/upload_questions', methods=['GET', 'POST'])
@login_required
def upload_questions():

    if request.method == 'POST':
        # Cek apakah file ada dalam request
        if 'excel_file' not in request.files:
            flash("Tidak ada file yang diunggah", "danger")
            return redirect(request.url)
        
        file = request.files['excel_file']
        
        if file.filename == '':
            flash("Tidak ada file yang dipilih", "danger")
            return redirect(request.url)
        
        # Jika file ada dan memiliki ekstensi yang diperbolehkan
        if file and allowed_file(file.filename):
            # Amankan nama file dan simpan ke server
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Menggunakan pandas untuk membaca file Excel
            try:
                df = pd.read_excel(file_path)
                print("File Excel berhasil dibaca!")

                # Memeriksa apakah kolom yang dibutuhkan ada dalam data
                required_columns = ['question', 'option1', 'option2', 'option3', 'option4', 'answer']
                if not all(col in df.columns for col in required_columns):
                    flash("File Excel tidak memiliki semua kolom yang diperlukan", "danger")
                    return redirect(url_for('upload_questions'))

                # Menambahkan soal ke dalam database
                for _, row in df.iterrows():
                    question = Question(
                        question=row['question'],
                        option1=row['option1'],
                        option2=row['option2'],
                        option3=row['option3'],
                        option4=row['option4'],
                        answer=row['answer']
                    )
                    db.session.add(question)

                # Menyimpan perubahan ke database
                db.session.commit()
                flash("Soal berhasil diunggah dan disimpan.", "success")
            except Exception as e:
                flash(f"Terjadi kesalahan saat memproses file Excel: {str(e)}", "danger")
                db.session.rollback()  # Rollback jika ada kesalahan
            finally:
                # Menghapus file yang diunggah setelah diproses
                os.remove(file_path)

            return redirect(url_for('manage_questions'))

    return render_template('upload_questions.html')


#folder upload manual
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])


# Fungsi user_loader untuk memuat pengguna berdasarkan ID
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Jalankan aplikasi
if __name__ == '__main__':
    # Pastikan folder uploads ada
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)


# Fungsi user_loader untuk memuat pengguna berdasarkan ID
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Rute untuk halaman utama
@app.route('/')
@app.route('/home')
@login_required
def home():
    # Mengambil data pengguna yang sedang login
    username = current_user.username

    # Mengambil semua soal dari database
    questions = Question.query.all()

    return render_template('home.html', username=username, questions=questions)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        # Memeriksa apakah password dan konfirmasi password cocok
        if password != confirm_password:
            return "Password dan konfirmasi password tidak cocok."
        
        # Memeriksa apakah username sudah ada
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return "Username sudah terdaftar, silakan pilih yang lain."
        
        # Meng-hash password sebelum disimpan ke database
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        
        # Menambahkan pengguna baru ke database
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('register.html')

#rute index 
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

#rute login 
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Mencari pengguna di database
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)  # Menggunakan login_user dari Flask-Login
            return redirect(url_for('home'))  # Mengarahkan ke halaman utama setelah login berhasil
        else:
            return "Kredensial tidak valid. Silakan coba lagi."
    return render_template('login.html')

#rute untuk halaman kisi-kisi
@app.route('/kisi_kisi')
def kisi_kisi():
    # Logika untuk mengambil kisi-kisi ujian atau informasi terkait
    return render_template('kisi_kisi.html')

# Rute untuk halaman formulir
@app.route('/form', methods=['GET', 'POST'])
def form():
    if not current_user.is_authenticated:  # Memeriksa apakah pengguna sudah login
        return redirect(url_for('login'))  # Jika belum login, arahkan ke halaman login
    
    return render_template('form.html')  # Menampilkan halaman formulir


# Rute untuk meng-handle pengiriman formulir ujian
@app.route('/submit_form', methods=['POST'])
def submit_form():
    if not current_user.is_authenticated:  # Memeriksa apakah pengguna sudah login
        return redirect(url_for('login'))  # Jika belum login, arahkan ke halaman login

    if request.method == 'POST':
        name = request.form['name']
        class_name = request.form['class_name']
        npm = request.form['npm']
        subject_name = request.form['subject_name']
        lecturer_name = request.form['lecturer_name']

        # Menyimpan data formulir ke database
        user = current_user  # Menggunakan current_user untuk mendapatkan user yang sedang login
        user_profil = UserProfile(
            user_id=user.id,  # Menggunakan user.id untuk ID pengguna
            name=name,
            class_name=class_name,
            npm=npm,
            subject_name=subject_name,
            lecturer_name=lecturer_name
        )
        
        db.session.add(user_profil)
        db.session.commit()

        # Redirect setelah pengiriman sukses (misalnya ke halaman ujian atau konfirmasi)
        return redirect(url_for('exam', exam_id=1))  # Gantilah dengan id soal yang sesuai
    return redirect(url_for('form'))  # Jika bukan POST, arahkan kembali ke form

from flask_login import current_user

@app.route('/exam/<int:exam_id>', methods=['GET', 'POST'])
def exam(exam_id):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))  # Memastikan pengguna sudah login

    # Mengambil soal ujian berdasarkan exam_id dari database
    questions = Question.query.all()  # Mengambil semua soal
    if not questions:
        return "Ujian tidak ditemukan."  # Jika tidak ada soal, tampilkan pesan error

    # Memeriksa jika sesi belum memiliki 'correct_answers' atau 'incorrect_answers'
    if 'correct_answers' not in session:
        session['correct_answers'] = 0
        session['incorrect_answers'] = 0

    # Jika metode POST, berarti pengguna sudah mengirimkan jawaban
    if request.method == 'POST':
        user_answer = request.form.get('answer')  # Mengambil jawaban dari form
        
        # Mengecek apakah jawaban benar atau salah
        if user_answer == questions[exam_id - 1].answer:  # Periksa jawaban yang diberikan dengan jawaban yang benar
            session['correct_answers'] += 1  # Meningkatkan jumlah jawaban benar
        else:
            session['incorrect_answers'] += 1  # Meningkatkan jumlah jawaban salah

        # Jika ini adalah soal terakhir, tampilkan hasil akhir ujian
        if exam_id == len(questions):
            correct_answers = session['correct_answers']
            incorrect_answers = session['incorrect_answers']
            total_questions = len(questions)
            # Hapus hasil ujian dari sesi agar tidak terbawa ke ujian berikutnya
            session.pop('correct_answers', None)
            session.pop('incorrect_answers', None)
            return render_template('result.html', correct_answers=correct_answers, incorrect_answers=incorrect_answers, total_questions=total_questions)

        # Jika ada soal berikutnya, arahkan ke soal berikutnya
        return redirect(url_for('exam', exam_id=exam_id + 1))

    # Menampilkan soal ujian
    return render_template('exam.html', exam=questions[exam_id-1])

# Rute untuk logout
@app.route('/logout')
@login_required
def logout():
    logout_user()  # Menggunakan logout_user dari Flask-Login
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
