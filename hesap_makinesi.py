import ast
import operator
import math
import tkinter as tk
from tkinter import messagebox

ARKA_PLAN = "#171923"
PANEL = "#222633"
EKRAN_RENGI = "#10131A"
SAYI_RENGI = "#303747"
ISLEM_RENGI = "#414C65"
VURGU_RENGI = "#6C8CFF"
YAZI_RENGI = "#F5F7FA"
IKINCIL_YAZI = "#AAB2C5"
SILME_RENGI = "#A84252"
ESITTIR_RENGI = "#5278F5"

OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def hesapla(ifade):

    def degerlendir(node):
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return node.value

        if isinstance(node, ast.BinOp) and type(node.op) in OPERATORS:
            sol = degerlendir(node.left)
            sag = degerlendir(node.right)

            if isinstance(node.op, ast.Div) and sag == 0:
                raise ZeroDivisionError

            if isinstance(node.op, ast.Pow) and abs(sag) > 1000:
                raise ValueError("Üs değeri çok büyük.")

            sonuc = OPERATORS[type(node.op)](sol, sag)

            if isinstance(sonuc, complex):
                raise ValueError("Karmaşık sayılar desteklenmiyor.")

            if isinstance(sonuc, float) and not math.isfinite(sonuc):
                raise ValueError("Sonuç çok büyük.")

            return sonuc

        if isinstance(node, ast.UnaryOp) and type(node.op) in OPERATORS:
            return OPERATORS[type(node.op)](degerlendir(node.operand))

        raise ValueError("Geçersiz matematiksel ifade.")

    agac = ast.parse(ifade, mode="eval")
    return degerlendir(agac.body)


class HesapMakinesi:

    def __init__(self, pencere):
        self.pencere = pencere
        self.pencere.title("Akıllı Hesap Makinesi")
        self.pencere.geometry("390x570")
        self.pencere.resizable(False, False)
        self.pencere.configure(bg=ARKA_PLAN)

        self.ifade = tk.StringVar()
        self.gecmis = []

        baslik = tk.Label(
            pencere,
            text="AKILLI HESAP MAKİNESİ",
            font=("Arial", 12, "bold"),
            bg=ARKA_PLAN,
            fg=IKINCIL_YAZI
        )
        baslik.pack(pady=(18, 10))

        ekran_paneli = tk.Frame(
            pencere,
            bg=EKRAN_RENGI
        )
        ekran_paneli.pack(fill="x", padx=14, pady=(0, 12))

        self.ekran = tk.Entry(
            ekran_paneli,
            textvariable=self.ifade,
            font=("Arial", 25),
            bg=EKRAN_RENGI,
            fg=YAZI_RENGI,
            insertbackground=YAZI_RENGI,
            justify="right",
            relief="flat",
            bd=0
        )
        self.ekran.pack(fill="x", padx=12, pady=18, ipady=8)
        self.ekran.bind("<Key>", self.klavye_tusu)

        yardimci = tk.Frame(pencere, bg=ARKA_PLAN)
        yardimci.pack(fill="x", padx=12, pady=(0, 5))

        self.buton_olustur(
            yardimci, "Temizle", self.temizle,
            PANEL, SILME_RENGI
        ).pack(side="left", expand=True, fill="x", padx=3)

        self.buton_olustur(
            yardimci, "Sil ⌫", self.sil,
            PANEL, YAZI_RENGI
        ).pack(side="left", expand=True, fill="x", padx=3)

        self.buton_olustur(
            yardimci, "Geçmiş", self.gecmisi_goster,
            PANEL, YAZI_RENGI
        ).pack(side="left", expand=True, fill="x", padx=3)

        butonlar = [
            ["7", "8", "9", "÷"],
            ["4", "5", "6", "×"],
            ["1", "2", "3", "−"],
            ["±", "0", ".", "+"],
            ["(", ")", "%", "xʸ"],
        ]

        for satir in butonlar:
            cerceve = tk.Frame(pencere, bg=ARKA_PLAN)
            cerceve.pack(
                expand=True,
                fill="both",
                padx=10,
                pady=2
            )

            for metin in satir:
                renk = SAYI_RENGI
                yazi = YAZI_RENGI

                if metin in ["÷", "×", "−", "+", "%", "(", ")", "xʸ"]:
                    renk = ISLEM_RENGI

                if metin == "xʸ":
                    komut = lambda: self.ifade_ekle("**")
                elif metin == "±":
                    komut = self.isareti_degistir
                else:
                    komut = lambda x=metin: self.buton_tikla(x)

                self.buton_olustur(
                    cerceve, metin, komut, renk, yazi
                ).pack(
                    side="left",
                    expand=True,
                    fill="both",
                    padx=3,
                    pady=3
                )

        alt_satir = tk.Frame(pencere, bg=ARKA_PLAN)
        alt_satir.pack(fill="x", padx=10, pady=(5, 12))

        self.buton_olustur(
            alt_satir, "Yeni İşlem", self.temizle,
            PANEL, YAZI_RENGI
        ).pack(side="left", expand=True, fill="both", padx=3, ipady=8)

        self.buton_olustur(
            alt_satir, "=  HESAPLA", self.sonucu_hesapla,
            ESITTIR_RENGI, "#FFFFFF"
        ).pack(side="left", expand=True, fill="both", padx=3, ipady=8)

        self.ekran.focus_set()

    def buton_olustur(self, ebeveyn, metin, komut, arka_plan, yazi_rengi):
        return tk.Button(
            ebeveyn,
            text=metin,
            command=komut,
            font=("Arial", 12, "bold"),
            bg=arka_plan,
            fg=yazi_rengi,
            activebackground=VURGU_RENGI,
            activeforeground="#FFFFFF",
            relief="flat",
            bd=0,
            cursor="hand2"
        )

    def ifade_ekle(self, metin):
        self.ifade.set(self.ifade.get() + metin)

    def temizle(self):
        self.ifade.set("")

    def sil(self):
        self.ifade.set(self.ifade.get()[:-1])

    def isareti_degistir(self):
        mevcut = self.ifade.get()

        if not mevcut:
            self.ifade.set("-")
        elif mevcut.startswith("-"):
            self.ifade.set(mevcut[1:])
        else:
            self.ifade.set("-" + mevcut)

    def klavye_tusu(self, olay):
        tus = olay.char

        if tus in "0123456789.+-*/%()":
            self.ifade_ekle(tus)
            return "break"

        elif tus == "^":
            self.ifade_ekle("**")
            return "break"

        elif olay.keysym == "Return":
            self.sonucu_hesapla()
            return "break"

        elif olay.keysym == "BackSpace":
            self.sil()
            return "break"

        elif olay.keysym == "Escape":
            self.temizle()
            return "break"

    def buton_tikla(self, tus):
        donusum = {
            "÷": "/",
            "×": "*",
            "−": "-"
        }

        self.ifade_ekle(donusum.get(tus, tus))

    def gecmisi_goster(self):
        if self.gecmis:
            messagebox.showinfo(
                "İşlem Geçmişi",
                "\n".join(self.gecmis[-20:]),
                parent=self.pencere
            )
        else:
            messagebox.showinfo(
                "İşlem Geçmişi",
                "Henüz işlem yapmadınız.",
                parent=self.pencere
            )

    def sonucu_hesapla(self):
        ifade = self.ifade.get().strip()

        if not ifade:
            return

        try:
            sonuc = hesapla(ifade)
            kayit = f"{ifade} = {sonuc}"
            self.gecmis.append(kayit)
            self.ifade.set(str(sonuc))

        except ZeroDivisionError:
            messagebox.showerror(
                "Hata",
                "Bir sayı sıfıra bölünemez.",
                parent=self.pencere
            )

        except (ValueError, SyntaxError, TypeError, OverflowError):
            messagebox.showerror(
                "Hata",
                "Geçersiz işlem girdiniz.",
                parent=self.pencere
            )

pencere = tk.Tk()
uygulama = HesapMakinesi(pencere)
pencere.mainloop()

