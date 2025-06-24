import tkinter as tk
from tkinter import ttk, messagebox
import threading, cv2, pickle, numpy as np, os, time, csv
from datetime import datetime
from sklearn.neighbors import KNeighborsClassifier
from win32com.client import Dispatch
from PIL import Image, ImageTk

DATA_DIR = 'data/'
os.makedirs(DATA_DIR, exist_ok=True)
FACES_FILE = os.path.join(DATA_DIR, 'faces_data.pkl')
NAMES_FILE = os.path.join(DATA_DIR, 'names.pkl')
VOTE_FILE = 'votes.csv'
USER_FILE = 'users.csv'

def speak(text):
    speaker = Dispatch("SAPI.SpVoice")
    speaker.Speak(text)

class FaceVotingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Recognition Voting System")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        self.style = ttk.Style()
        self.style.configure("TButton", font=("Segoe UI", 10), padding=6)
        self.style.configure("TLabel", font=("Segoe UI", 11))
        self.style.configure("Header.TLabel", font=("Segoe UI", 16, "bold"))

        self.notebook = ttk.Notebook(self.root)
        self.register_frame = ttk.Frame(self.notebook, padding=20)
        self.vote_frame = ttk.Frame(self.notebook, padding=20)
        self.notebook.add(self.register_frame, text="Register")
        self.notebook.add(self.vote_frame, text="Vote")
        self.notebook.pack(expand=True, fill="both")

        self.build_register_tab()
        self.build_vote_tab()

    def build_register_tab(self):
        ttk.Label(self.register_frame, text="Register New Voter", style="Header.TLabel").pack(pady=10)

        form = ttk.LabelFrame(self.register_frame, text="Voter Information", padding=20)
        form.pack(pady=20)

        ttk.Label(form, text="Aadhar Number:").grid(row=0, column=0, sticky="e", pady=5)
        self.aadhar_entry = ttk.Entry(form, width=30)
        self.aadhar_entry.grid(row=0, column=1, pady=5)

        ttk.Label(form, text="Full Name:").grid(row=1, column=0, sticky="e", pady=5)
        self.name_entry = ttk.Entry(form, width=30)
        self.name_entry.grid(row=1, column=1, pady=5)

        ttk.Label(form, text="Country:").grid(row=2, column=0, sticky="e", pady=5)
        self.country_entry = ttk.Entry(form, width=30)
        self.country_entry.grid(row=2, column=1, pady=5)

        self.register_btn = ttk.Button(self.register_frame, text="Start Face Capture", command=self.start_capture_thread)
        self.register_btn.pack(pady=20)

    def start_capture_thread(self):
        self.register_btn.config(state="disabled", text="Capturing...")
        threading.Thread(target=self.capture_faces).start()

    def capture_faces(self):
        aadhar = self.aadhar_entry.get().strip()
        name = self.name_entry.get().strip()
        country = self.country_entry.get().strip()

        if not aadhar.isdigit() or not name or not country:
            messagebox.showerror("Input Error", "Please fill all fields correctly.")
            self.register_btn.config(state="normal", text="Start Face Capture")
            return

        write_header = not os.path.exists(USER_FILE)
        with open(USER_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            if write_header:
                writer.writerow(['AADHAR', 'NAME', 'COUNTRY'])
            writer.writerow([aadhar, name, country])

        video = cv2.VideoCapture(0)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        face_data, i, total_frames = [], 0, 200
        while True:
            ret, frame = video.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                crop = frame[y:y+h, x:x+w]
                resized = cv2.resize(crop, (50, 50))
                if len(face_data) < total_frames and i % 2 == 0:
                    face_data.append(resized)
                i += 1
                cv2.putText(frame, f"{len(face_data)} / {total_frames}", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)
                cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 2)
            cv2.imshow("Capturing Face", frame)
            if cv2.waitKey(1) == ord('q') or len(face_data) >= total_frames:
                break
        video.release()
        cv2.destroyAllWindows()

        face_data = np.asarray(face_data).reshape((total_frames, -1))
        names = []
        if os.path.exists(NAMES_FILE):
            with open(NAMES_FILE, 'rb') as f:
                names = pickle.load(f)
        names += [aadhar] * total_frames
        with open(NAMES_FILE, 'wb') as f:
            pickle.dump(names, f)

        if os.path.exists(FACES_FILE):
            with open(FACES_FILE, 'rb') as f:
                existing = pickle.load(f)
            face_data = np.append(existing, face_data, axis=0)
        with open(FACES_FILE, 'wb') as f:
            pickle.dump(face_data, f)

        messagebox.showinfo("Success", "Face registration complete!")
        self.register_btn.config(state="normal", text="Start Face Capture")

    def build_vote_tab(self):
        ttk.Label(self.vote_frame, text="Vote Section", style="Header.TLabel").pack(pady=10)
        ttk.Button(self.vote_frame, text="Start Voting", command=self.start_face_recognition_flow).pack(pady=20)

    def start_face_recognition_flow(self):
        threading.Thread(target=self.face_and_then_vote).start()

    def face_and_then_vote(self):
        self.recognized_user = None
        self.recognize_face()

        if self.recognized_user:
            self.open_party_selection_window()

    def open_party_selection_window(self):
        vote_window = tk.Toplevel(self.root)
        vote_window.title("Select Your Party")
        vote_window.geometry("400x300")

        ttk.Label(vote_window, text="Choose Your Party", font=("Segoe UI", 14, "bold")).pack(pady=10)

        party_var = tk.StringVar()

        for party in ["BJP", "CONGRESS", "AAP", "NONE"]:
            ttk.Radiobutton(vote_window, text=party, variable=party_var, value=party).pack(anchor="w", padx=20, pady=5)

        def submit():
            selected = party_var.get()
            if not selected:
                messagebox.showwarning("Warning", "Please select a party.")
                return
            self.submit_vote_data(selected)
            vote_window.destroy()

        ttk.Button(vote_window, text="Submit Vote", command=submit).pack(pady=20)

    def recognize_face(self):
        if not os.path.exists(FACES_FILE) or not os.path.exists(NAMES_FILE):
            messagebox.showerror("Error", "No face data available.")
            return

        with open(NAMES_FILE, 'rb') as f:
            labels = pickle.load(f)
        with open(FACES_FILE, 'rb') as f:
            faces = pickle.load(f)

        knn = KNeighborsClassifier(n_neighbors=5)
        knn.fit(faces, labels)

        video = cv2.VideoCapture(0)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        identified = None
        while True:
            ret, frame = video.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                crop_img = frame[y:y + h, x:x + w]
                resized_img = cv2.resize(crop_img, (50, 50)).flatten().reshape(1, -1)
                distances, indices = knn.kneighbors(resized_img)
                if distances[0][0] > 5000:
                    identified = None
                else:
                    identified = knn.predict(resized_img)[0]
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.imshow('Face Recognition - Press Q to continue', frame)
            if cv2.waitKey(1) == ord('q'):
                break
        video.release()
        cv2.destroyAllWindows()

        if identified is None:
            speak("You are not registered.")
            messagebox.showerror("Not Registered", "Face not recognized. Please register first.")
            return

        user_info = identified
        try:
            with open(USER_FILE, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row['AADHAR'] == identified:
                        user_info = f"{row['NAME']} from {row['COUNTRY']}"
                        break
        except Exception:
            pass

        if self.has_voted(identified):
            speak("You have already voted.")
            messagebox.showinfo("Notice", "You have already voted.")
        else:
            speak(f"Welcome {user_info}. Please select your party.")
            self.recognized_user = identified

    def has_voted(self, aadhar):
        if not os.path.exists(VOTE_FILE):
            return False
        with open(VOTE_FILE, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if row and row[0] == aadhar:
                    return True
        return False

    def submit_vote_data(self, party):
        if not self.recognized_user:
            messagebox.showwarning("Warning", "Please recognize face first.")
            return

        date = datetime.now().strftime("%d-%m-%Y")
        time_now = datetime.now().strftime("%H:%M:%S")
        write_header = not os.path.exists(VOTE_FILE)
        with open(VOTE_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            if write_header:
                writer.writerow(["NAME", "VOTE", "DATE", "TIME"])
            writer.writerow([self.recognized_user, party, date, time_now])
        speak("Thank you for voting.")
        messagebox.showinfo("Success", "Vote submitted successfully.")
        self.recognized_user = None

if __name__ == "__main__":
    root = tk.Tk()
    app = FaceVotingApp(root)
    root.mainloop()