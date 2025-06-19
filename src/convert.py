#!/usr/bin/env python3
"""
Simple “Text-to-MP3” GUI for gTTS
Author: Louis Ouellet  <louis@albcie.com>
"""

import sys
from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QWidget, QTextEdit, QComboBox, QLineEdit, QPushButton,
    QFileDialog, QLabel, QGridLayout, QMessageBox
)

from gtts import gTTS


# ---------------------------------------------------------------------------
# A very small whitelist of languages and matching top-level domains (country)
# Extend these as needed; codes must be valid for gTTS.
# ---------------------------------------------------------------------------
LANGUAGES = {
    "Français": "fr",
    "English": "en",
    "Español": "es",
}

TLDs = {
    "Canada": "ca",
    "France": "fr",
    "United States": "com",
    "United Kingdom": "co.uk",
    "Australia": "com.au",
}


class TTSWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Text ➜ MP3 (gTTS)")
        self.build_ui()

    # -------------------------------------------------------------------- UI
    def build_ui(self):
        layout = QGridLayout(self)
        layout.setSpacing(10)

        # Row 0 – Text input (big single-line QTextEdit)
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("Saisissez (ou collez) votre texte ici…")
        self.text_edit.setMinimumHeight(180)
        layout.addWidget(self.text_edit, 0, 0, 1, 3)

        # Row 1 – Language & country (same row)
        self.lang_combo = QComboBox()
        for label in LANGUAGES:
            self.lang_combo.addItem(label, LANGUAGES[label])

        self.country_combo = QComboBox()
        for label in TLDs:
            self.country_combo.addItem(label, TLDs[label])

        layout.addWidget(QLabel("Langue :"), 1, 0, Qt.AlignRight)
        layout.addWidget(self.lang_combo, 1, 1)
        layout.addWidget(QLabel("Pays :"), 1, 2, Qt.AlignRight)
        layout.addWidget(self.country_combo, 1, 3)

        # Row 2 – Output file selector
        self.output_edit = QLineEdit()
        self.output_edit.setPlaceholderText("Choisissez la destination MP3…")
        browse_btn = QPushButton("Parcourir…")
        browse_btn.clicked.connect(self.choose_file)

        layout.addWidget(QLabel("Fichier :"), 2, 0, Qt.AlignRight)
        layout.addWidget(self.output_edit, 2, 1, 1, 2)
        layout.addWidget(browse_btn, 2, 3)

        # Row 3 – Generate button
        save_btn = QPushButton("Générer l’audio")
        save_btn.clicked.connect(self.generate_audio)
        layout.addWidget(save_btn, 3, 0, 1, 4, Qt.AlignCenter)

    # ---------------------------------------------------------- File chooser
    def choose_file(self):
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Enregistrer sous…",
            str(Path.home() / "output.mp3"),
            "MP3 (*.mp3)"
        )
        if path:
            if not path.lower().endswith(".mp3"):
                path += ".mp3"
            self.output_edit.setText(path)

    # ----------------------------------------------------------- Generation
    def generate_audio(self):
        text = self.text_edit.toPlainText().strip()
        if not text:
            self.alert("Le texte ne peut pas être vide.")
            return

        out_path = self.output_edit.text().strip()
        if not out_path:
            self.alert("Veuillez sélectionner un fichier de sortie.")
            return

        lang = self.lang_combo.currentData()
        tld = self.country_combo.currentData()

        try:
            tts = gTTS(text=text, lang=lang, tld=tld, slow=False)
            tts.save(out_path)
            self.alert(f"Fichier enregistré :\n{out_path}", QMessageBox.Information)
        except Exception as exc:
            self.alert(f"Erreur : {exc}", QMessageBox.Critical)

    # -------------------------------------------------------------- Helpers
    @staticmethod
    def alert(message, icon=QMessageBox.Warning):
        dlg = QMessageBox()
        dlg.setIcon(icon)
        dlg.setText(message)
        dlg.exec_()


# ---------------------------------------------------------------------------

def main():
    app = QApplication(sys.argv)
    win = TTSWindow()
    win.resize(720, 320)
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
