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

class IdentitasKomunikasiForm(forms.Form):
    kelompok = forms.CharField(label="Kelompok ", max_length=10)

class PenilaianKomunikasiForm(forms.Form):
    Penyampaian1Choice = [
        (1,'Menyampaikan informasi tidak jelas, tidak lugas, dan tidak terstruktur'),
        (2,'Menyampaikan informasi cukup jelas tetapi kurang lugas dan tidak terstruktur sehingga sebagian sulit dimengerti'),
        (3,'Dapat menyampaikan informasi dengan jelas, lugas, namun kurang terstruktur'),
        (4,'Dapat menyampaikan informasi dengan terstruktur, jelas, lugas, dan mudah dimengerti') 
        ]
    Penyampaian2Choice = [
        (1,'Intonasi tidak tepat dan artikulasi tidak jelas'),
        (2,'Intonasi dan artikulasi cukup jelas'),
        (3,'Intonasi tepat dan artikulasi jelas'),
        (4,'Intonasi tepat, artikulasi jelas, dan mudah dipahami') 
    ]
    Penyampaian3Choice = [
        (1,'Tidak yakin dengan materi yang disampaikan dan gugup dalam penyampaiannya'),
        (2,'Yakin dengan materi yang disampaikan tetapi gugup dalam penyampaiannya'),
        (3,'Yakin dengan materi yang disampaikan'),
        (4,'Yakin dan percaya diri ketika penyampaikan informasi') 
    ]
    Penyampaian4Choice = [
        (1,'Tidak ada kontak mata dengan audiens, penggunaan gestur tubuh terbatas'),
        (2,'Melakukan kontak mata dengan audiens, penggunaan gestur tubuh terbatas'),
        (3,'Melakukan kontak mata dengan audiens dengan baik, menggunakan gestur tubuh dengan baik, tetapi terkesan dipaksakan'),
        (4,'Melakukan kontak mata dengan audiens dengan baik, menggunakan gestur tubuh dengan baik, dan menunjukkan antusiasme yang tinggi') 
    ]
    KontenChoice = [
        (1,'Informasi yang diberikan tidak relevan dengan topik yang sedang dibahas'),
        (2,'Informasi yang diberikan cukup relevan dengan topik yang sedang dibahas, seharusnya masih dpaat ditingkatkan dengan tambahan informasi lain yang lebih relevan'),
        (3,'Informasi yang diberikan sebagian besar relevan dengan topik yang sedang dibahas'),
        (4,'Informasi yang disampaikan relevan dengan topik yang sedang dibahas')
    ]
    BahasaChoice = [
        (1,'Bahasa yang digunakan tidak formal/sebagian besar tidak formal'),
        (2,'Menggunakan campuran bahasa formal dan non-formal'),
        (3,'Menggunakan bahasa formal dengan sedikit non-formal'),
        (4,'Menggunakan bahasa yang formal')
    ]
    PenguasaanChoice = [
        (1,'Tidak menguasai materi yang disampaikan'),
        (2,'Menguasai materi yang disampaikan tetapi masih banyak kekurangan'),
        (3,'Menguasai sebagian materi yang disampaikan dengan sedikit kekurangan'),
        (4,'Mampu menguasai semua materi yang disampaikan dengan baik')
    ]
    MenjawabChoice = [
        (1,'Tidak menjawab pertanyaan yang diajukan atau menjawab pertanyaan dengan bertele-tele dan tidak sesuai dengan pertanyaan yang diajukan'),
        (2,'Menjawab pertanyaan dengan bertele-tele dan sebagian jawaban relevan dengan pertanyaan yang diajukan'),
        (3,'Menjawab pertanyaan sesuai dengan pertanyaan yang diajukan'),
        (4,'Menjawab pertanyaan sesuai dengan pertanyaan yang diajukan, dengan jelas, singkat, dan mudah dipahami')
    ]
    MediaChoice = [
        (1,'Tidak menggunakan media pendukung untuk memudahkan audiens memahami materi yang disampaikan (slide, ilustrasi, alat peraga, dll)'),
        (2,'Media pendukung yang digunakan membingungkan/susah dipahami'),
        (3,'Media pendukung dapat mendukung gagasan dengan baik, tetapi masih ada kesalahan (misal labeling, tidak menampilkan data dengan jelas, dll)'),
        (4,'Menggunakan banyak media pendukung yang mendukung gagasan dengan baik dan jelas')
    ]
    WaktuChoice = [
        (1,'Waktu yang digunakan terlalu lama atau terlalu singkat untuk menyampaikan materi'),
        (2,'Waktu yang digunakan sesuai dengan yang ditentukan, tetapi masih dapat ditingkatkan penggunaannya dengan menambahkan atau mengurangi materi yang disampaikan'),
        (3,'Waktu digunakan sesuai dengan yang ditentukan untuk menyampaikan materi'),
        (4,'Waktu digunakan dengan efektif dan efisien untuk menyampaiakn materi dengan singkat, jelas, mudah dipahami, dan disertai  pendukung-pendukung yag memudahkan audiens memahami masalah yang dibahas')
    ]
    KelompokPeer = forms.IntegerField(label="Kelompok ", min_value=1)
    NamePeer = forms.CharField(label="Nama ", max_length=50)
    NIMPeer = forms.CharField(label="NIM ", max_length=10) 
    Penyampaian1 = forms.ChoiceField(widget=forms.RadioSelect, choices=Penyampaian1Choice, label='Penyampaian1')
    Penyampaian2 = forms.ChoiceField(widget=forms.RadioSelect, choices=Penyampaian2Choice, label='Penyampaian2')
    Penyampaian3 = forms.ChoiceField(widget=forms.RadioSelect, choices=Penyampaian3Choice, label='Penyampaian3')
    Penyampaian4 = forms.ChoiceField(widget=forms.RadioSelect, choices=Penyampaian4Choice, label='Penyampaian4')
    Konten = forms.ChoiceField(widget=forms.RadioSelect, choices=KontenChoice, label='Konten')
    Bahasa = forms.ChoiceField(widget=forms.RadioSelect, choices=BahasaChoice, label='Bahasa')
    Penguasaan = forms.ChoiceField(widget=forms.RadioSelect, choices=PenguasaanChoice, label='Penguasaan')
    Menjawab = forms.ChoiceField(widget=forms.RadioSelect, choices=MenjawabChoice, label='Menjawab')
    Media = forms.ChoiceField(widget=forms.RadioSelect, choices=MediaChoice, label='Media')
    Waktu = forms.ChoiceField(widget=forms.RadioSelect, choices=WaktuChoice, label='Waktu')