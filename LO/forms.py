from django import forms

class IdentitasForm(forms.Form):
    name = forms.CharField(label="Nama ", max_length=50)
    NIM = forms.CharField(label="NIM ", max_length=10)
    kelompok = forms.CharField(label="Kelompok ", max_length=10)

class PenilaianKerjasamaForm(forms.Form):
    KontribusiChoice = [
        (1,'Jarang memberikan ide yang berguna ketika berpartisipasi dalam kelompok dan diskusi dalam kelas. Mungkin menolak untuk ikut berpartisipasi'),
        (2,'Terkadang memberikan ide yang berguna ketika berpartisipasi dalam kelompok dan diskusi dalam kelas. Anggota kelompok yang melakukan apa yang diperlukan'),
        (3,'Biasanya memberikan ide yang berguna ketika berpartisipasi dalam kelompok dan diskusi dalam kelas. Anggota kelompok yang berusaha keras.'),
        (4,'Secara rutin memberikan ide yang berguna ketika berpartisipasi dalam kelompok dan diskusi dalam kelas. Seorang pemimpin yang menyumbang banyak usaha.') 
    ]
    PemecahanMasalahChoice = [
        (1,'Tidak mencoba memecahkan masalah atau tidak membantu orang lain memecahkan masalah. Memungkinkan orang lain melakukan pekerjaan.'),
        (2,'Tidak menyarankan atau tidak memberikan solusi, tetapi mau mencoba solusi yang disarankan oleh orang lain'),
        (3,'Menyempurnakan solusi yang disarankan oleh orang lain'),
        (4,'Secara aktif mencari dan menyarankan solusi utuk masalah yang dihadapi') 
    ]
    SikapChoice = [
        (1,'Sering mengkritik tugas atau pekerjaan anggota lain dalam kelompok secara terbuka. Selalu bersikap negatif tentang tugas yang diberikan.'),
        (2,'Terkadang secara terbuka mengkritik tugas atau pekerjaan anggota lain dalam kelompok. Biasanya memiliki sikat positif tentang tugas yang diberikan.'),
        (3,'Jarang secara terbuka mengkritik tugas atau pekerjaan anggota lain dalam kelompok. Seringkali memiliki sikat positif tentang tugas yang diberikan.'),
        (4,'Tidak pernah secara terbuka mengkritik tugas atau pekerjaan anggota lain dalam kelompok. Selalu memiliki sikat positif tentang tugas yang diberikan.') 
    ]
    FokusTerhadapTugasChoice = [
        (1,'Jarang fokus pada tugas dan apa yang perlu dilakukan. Memungkinkan orang lain melakukan pekerjaan.'),
        (2,'Berfokus pada tugas dan apa yang perlu dilakukan dalam beberapa waktu. Anggota kelompok lainnya kadang-kadang harus mengingatkan supaya mengerjakan tugas.'),
        (3,'Berfokus pada tugas dan apa yang perlu dilakukan dalam sebagian besar waktu untuk menyelesaikannya. Anggota kelompok lain dapat mengandalkan orang ini.'),
        (4,'Secara konsisten tetap fokus pada tugas dan apa yang perlu dilakukan. Sangat mandiri.') 
    ]
    BekerjaDenganOrangLainChoice = [
        (1,'Jarang mendengarkan, berbagi, dan mendukung upaya anggota lain dalam kelompok. Seringkali bukan anggota kelompok yang bagus.'),
        (2,'Seringkali mendengarkan, berbagi, dan mendukung upaya anggota lain dalam kelompok, tetapi terkadang bukan sebagai anggota kelompok yang baik.'),
        (3,'Biasanya mendengarkan, berbagi, dan mendukung upaya anggota lain dalam kelompok. Tidak menyebabkan perselisihan dalam kelompok.'),
        (4,'Hampir selalu mendengarkan, berbagi, dan mendukung upaya anggota lain dalam kelompok. Mencoba untuk membuat anggota lain bekerjasama dengan baik dalam kelompok.')
    ]
    NamePeer = forms.CharField(label="Nama ", max_length=50)
    NIMPeer = forms.CharField(label="NIM ", max_length=10) 
    Kontribusi = forms.ChoiceField(widget=forms.RadioSelect, choices=KontribusiChoice, label='Kontribusi')
    PemecahanMasalah = forms.ChoiceField(widget=forms.RadioSelect, choices=PemecahanMasalahChoice, label='Pemecahan Masalah')
    Sikap = forms.ChoiceField(widget=forms.RadioSelect, choices=SikapChoice, label='Sikap')
    FokusTerhadapTugas = forms.ChoiceField(widget=forms.RadioSelect, choices=FokusTerhadapTugasChoice, label='Fokus terhadap tugas')
    BekerjaDenganOrangLain = forms.ChoiceField(widget=forms.RadioSelect, choices=BekerjaDenganOrangLainChoice, label='Bekerja dengan orang lain')