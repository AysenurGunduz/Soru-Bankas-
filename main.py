import sys
import os
import sqlite3
from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QMessageBox,
    QTableWidgetItem, QFileDialog, QAbstractItemView,
    QLabel
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from SoruBankası_ui import Ui_MainWindow as SoruBankasiUI
from SoruEkle_ui import Ui_MainWindow as SoruEkleUI
from soruseç_ui import Ui_MainWindow as SoruSecUI
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER

class SoruBankasi(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = SoruBankasiUI()
        self.ui.setupUi(self)
        
        self.setMinimumSize(800, 600)
        
        try:
          
            self.kapak_label = QLabel(self)
            pixmap = QPixmap("kapakfoto.png")
            menubar_height = self.menuBar().height()
            self.kapak_label.setGeometry(0, menubar_height, self.width(), self.height() - menubar_height)
            self.kapak_label.setScaledContents(True)
            self.kapak_label.setPixmap(pixmap)
            
            def resizeEvent(event):
                super(QMainWindow, self).resizeEvent(event)
                self.kapak_label.setGeometry(0, menubar_height, self.width(), self.height() - menubar_height)
            
            self.resizeEvent = resizeEvent
            
        except Exception as e:
            QMessageBox.warning(self, "Uyarı", f"Kapak fotoğrafı yüklenirken hata oluştu:\n{str(e)}")
        
        self.setStyleSheet("""
            QMainWindow {
                background-color: #FFE3E5;
            }
            QMenuBar {
                background-color: #FFCFD2;
                color: #4A4A4A;
                border-bottom: 1px solid #E8A0A4;
            }
            QMenuBar::item:selected {
                background-color: #E8A0A4;
                color: white;
            }
            QMenu {
                background-color: #FFE3E5;
                color: #4A4A4A;
                border: 1px solid #E8A0A4;
            }
            QMenu::item:selected {
                background-color: #FFCFD2;
            }
            QPushButton {
                background-color: #FFCFD2;
                border: 2px solid #E8A0A4;
                border-radius: 5px;
                padding: 5px 15px;
                color: #4A4A4A;
            }
            QPushButton:hover {
                background-color: #E8A0A4;
                color: white;
            }
            QTableWidget {
                background-color: white;
                alternate-background-color: #FFE3E5;
                border: 1px solid #E8A0A4;
            }
            QHeaderView::section {
                background-color: #FFCFD2;
                color: #4A4A4A;
                border: 1px solid #E8A0A4;
                padding: 4px;
            }
            QLabel {
                background-color: transparent;
            }
        """)
        
        # Veritabanı bağlantısı
        self.create_database()
        
        self.ui.SoruEkle_SayfasGe.triggered.connect(self.show_soru_ekle)
        self.ui.SoruSe_Sayfas.triggered.connect(self.show_soru_sec)
        
        self.soru_ekle_window = None
        self.soru_sec_window = None
    
    def create_database(self):
        conn = sqlite3.connect('sorular.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sorular (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                soru TEXT NOT NULL,
                secenek1 TEXT NOT NULL,
                secenek2 TEXT NOT NULL,
                secenek3 TEXT NOT NULL,
                secenek4 TEXT NOT NULL,
                secenek5 TEXT NOT NULL,
                dogru_cevap TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()
        
    def show_soru_ekle(self):
        if not self.soru_ekle_window:
            self.soru_ekle_window = SoruEkle()
        self.soru_ekle_window.show()
        
    def show_soru_sec(self):
        if not self.soru_sec_window:
            self.soru_sec_window = SoruSec()
        self.soru_sec_window.show()

class SoruEkle(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = SoruEkleUI()
        self.ui.setupUi(self)
        
        self.setStyleSheet("""
            QMainWindow {
                background-color: #FFE3E5;
            }
            QTextEdit {
                background-color: white;
                border: 1px solid #E8A0A4;
                border-radius: 3px;
                padding: 5px;
            }
            QPushButton {
                background-color: #FFCFD2;
                border: 2px solid #E8A0A4;
                border-radius: 5px;
                padding: 5px 15px;
                color: #4A4A4A;
            }
            QPushButton:hover {
                background-color: #E8A0A4;
                color: white;
            }
            QTableWidget {
                background-color: white;
                alternate-background-color: #FFE3E5;
                border: 1px solid #E8A0A4;
            }
            QHeaderView::section {
                background-color: #FFCFD2;
                color: #4A4A4A;
                border: 1px solid #E8A0A4;
                padding: 4px;
            }
            QLabel {
                color: #4A4A4A;
                font-weight: bold;
            }
        """)
        
        self.ui.soru_ekle.clicked.connect(self.save_soru)
        
        self.update_table()
        
    def save_soru(self):
        soru = self.ui.soru_girisi.toPlainText().strip()
        yanit1 = self.ui.yant_1.toPlainText().strip()
        yanit2 = self.ui.yant_2.toPlainText().strip()
        yanit3 = self.ui.yant_3.toPlainText().strip()
        yanit4 = self.ui.yant_4.toPlainText().strip()
        yanit5 = self.ui.yant_5.toPlainText().strip()
        
        if not all([soru, yanit1, yanit2, yanit3, yanit4, yanit5]):
            QMessageBox.warning(self, "Uyarı", "Tüm alanları doldurunuz!")
            return
            
        try:
            conn = sqlite3.connect('sorular.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO sorular (soru, secenek1, secenek2, secenek3, secenek4, secenek5, dogru_cevap)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (soru, yanit1, yanit2, yanit3, yanit4, yanit5, yanit1))  # İlk seçenek doğru cevap olarak kabul edilir
            conn.commit()
            conn.close()
            
            self.update_table()
            self.clear_inputs()
            QMessageBox.information(self, "Bilgi", "Soru başarıyla kaydedildi!")
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Soru kaydedilirken hata oluştu:\n{str(e)}")
    
    def update_table(self):
        try:
            conn = sqlite3.connect('sorular.db')
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM sorular')
            sorular = cursor.fetchall()
            conn.close()
            
            self.ui.soru_listele.setRowCount(len(sorular))
            for i, soru in enumerate(sorular):
                self.ui.soru_listele.setItem(i, 0, QTableWidgetItem(soru[1]))  # soru
                for j in range(5):
                    self.ui.soru_listele.setItem(i, j+1, QTableWidgetItem(soru[j+2]))  # seçenekler
        except Exception as e:
            QMessageBox.warning(self, "Uyarı", f"Tablo güncellenirken hata oluştu:\n{str(e)}")
    
    def clear_inputs(self):
        self.ui.soru_girisi.clear()
        self.ui.yant_1.clear()
        self.ui.yant_2.clear()
        self.ui.yant_3.clear()
        self.ui.yant_4.clear()
        self.ui.yant_5.clear()

class SoruSec(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = SoruSecUI()
        self.ui.setupUi(self)
        
        self.setStyleSheet("""
            QMainWindow {
                background-color: #FFE3E5;
            }
            QPushButton {
                background-color: #FFCFD2;
                border: 2px solid #E8A0A4;
                border-radius: 5px;
                padding: 5px 15px;
                color: #4A4A4A;
            }
            QPushButton:hover {
                background-color: #E8A0A4;
                color: white;
            }
            QTableWidget {
                background-color: white;
                alternate-background-color: #FFE3E5;
                border: 1px solid #E8A0A4;
            }
            QHeaderView::section {
                background-color: #FFCFD2;
                color: #4A4A4A;
                border: 1px solid #E8A0A4;
                padding: 4px;
            }
            QLabel {
                color: #4A4A4A;
                font-weight: bold;
            }
        """)
        #tabloda çoklu seçimi yapmaya çalıştım.
        self.ui.Sorulari_Gor.setSelectionMode(QAbstractItemView.MultiSelection)
        self.ui.Sorulari_Gor.setSelectionBehavior(QAbstractItemView.SelectRows)
        
        self.ui.Dosya_Sec.clicked.connect(self.export_to_pdf)
        self.ui.Yazdir.clicked.connect(self.export_to_pdf)
        
        self.update_table()
    
    def update_table(self):
        try:
            conn = sqlite3.connect('sorular.db')
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM sorular')
            sorular = cursor.fetchall()
            conn.close()
            
            self.ui.Sorulari_Gor.setRowCount(len(sorular))
            for i, soru in enumerate(sorular):
                self.ui.Sorulari_Gor.setItem(i, 0, QTableWidgetItem(soru[1]))  
                for j in range(5):
                    self.ui.Sorulari_Gor.setItem(i, j+1, QTableWidgetItem(soru[j+2]))  
                self.ui.Sorulari_Gor.setItem(i, 6, QTableWidgetItem(soru[7]))  
        except Exception as e:
            QMessageBox.warning(self, "Uyarı", f"Tablo güncellenirken hata oluştu:\n{str(e)}")
    
    def export_to_pdf(self):
        try:
            selected_rows = set(item.row() for item in self.ui.Sorulari_Gor.selectedItems())
            
            if not selected_rows:
                QMessageBox.warning(self, "Uyarı", "Lütfen yazdırılacak soruları seçin!")
                return
            
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            
            file_name, _ = QFileDialog.getSaveFileName(
                self,
                "PDF Kaydet",
                os.path.join(desktop, "sorular.pdf"),
                "PDF Dosyaları (*.pdf)"
            )
            
            if not file_name:
                return
            
            doc = SimpleDocTemplate(
                file_name,
                pagesize=letter,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=72
            )
            
            story = []
            soru_stili = ParagraphStyle(
                'SoruStili',
                fontSize=12,
                spaceAfter=20,
                spaceBefore=20,
                alignment=TA_CENTER
            )
            
            secenek_stili = ParagraphStyle(
                'SecenekStili',
                fontSize=11,
                leftIndent=30,
                spaceAfter=10,
                leading=16
            )
            
            dogru_cevap_stili = ParagraphStyle(
                'DogruCevapStili',
                fontSize=11,
                spaceBefore=15,
                spaceAfter=30,
                alignment=TA_CENTER
            )
            
            baslik_stili = ParagraphStyle(
                'Baslik',
                fontSize=24,
                alignment=TA_CENTER,
                spaceAfter=40
            )
            
            baslik = Paragraph("SORU BANKASI", baslik_stili)
            story.append(baslik)
            story.append(Spacer(1, 30))
            
            for i in selected_rows:
                soru = self.ui.Sorulari_Gor.item(i, 0).text()
                secenekler = [
                    self.ui.Sorulari_Gor.item(i, j+1).text()
                    for j in range(5)
                ]
                dogru_cevap = self.ui.Sorulari_Gor.item(i, 6).text()
                
                soru_no = len(story) // 4  
                if soru_no > 0:
                    story.append(Spacer(1, 20))
                
                soru_text = f"{soru_no + 1}. {soru}"
                story.append(Paragraph(soru_text, soru_stili))
                
                secenekler_harfler = ['A', 'B', 'C', 'D', 'E']
                for harf, secenek in zip(secenekler_harfler, secenekler):
                    secenek_text = f"{harf}) {secenek}"
                    story.append(Paragraph(secenek_text, secenek_stili))
                
                dogru_text = f"Doğru Cevap: {dogru_cevap}"
                story.append(Paragraph(dogru_text, dogru_cevap_stili))
            
            doc.build(story)
            
            QMessageBox.information(
                self,
                "Bilgi",
                f"Seçili sorular başarıyla PDF olarak kaydedildi!\nDosya: {file_name}"
            )
            
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"PDF oluşturulurken hata oluştu:\n{str(e)}")

def main():
    try:
        app = QApplication(sys.argv)
        window = SoruBankasi()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"Uygulama başlatılırken hata oluştu: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()
