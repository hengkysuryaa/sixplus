from django.db import models
from Mahasiswa.models import Student
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class Course(models.Model):
    course_id = models.CharField(max_length=6, unique=True)
    title = models.CharField(max_length=100)
    dept_name = models.CharField(max_length=10)
    credits = models.IntegerField()

    def __str__(self):
        return f"{self.course_id} {self.title}"

    def getCourse(self, c_id):
        return Course.objects.get(course_id = c_id)

class LO(models.Model):
    course_id = models.OneToOneField("Course", on_delete=models.CASCADE)
    lo_a = models.CharField(max_length=1)
    lo_b = models.CharField(max_length=1)
    lo_c = models.CharField(max_length=1)
    lo_d = models.CharField(max_length=1)
    lo_e = models.CharField(max_length=1)
    lo_f = models.CharField(max_length=1)
    lo_g = models.CharField(max_length=1)

    def __str__(self):
        return f"LO {self.course_id}"

    def getCourseLO(self, c_id):
        course = Course.objects.filter(course_id = c_id)
        item = LO.objects.filter(course_id = course[0])[0]
        lo_dict = {}
        if (item.lo_a != '-'):
            lo_dict['lo_a'] = item.lo_a
        if (item.lo_b != '-'):
            lo_dict['lo_b'] = item.lo_b
        if (item.lo_c != '-'):
            lo_dict['lo_c'] = item.lo_c
        if (item.lo_d != '-'):
            lo_dict['lo_d'] = item.lo_d
        if (item.lo_e != '-'):
            lo_dict['lo_e'] = item.lo_e
        if (item.lo_f != '-'):
            lo_dict['lo_f'] = item.lo_f
        if (item.lo_g != '-'):
            lo_dict['lo_g'] = item.lo_g
        return lo_dict, course[0]

class Section(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    sec_id = models.IntegerField()
    semester = models.IntegerField()
    year = models.IntegerField()

    def __str__(self):
        return f"{self.course}, K{self.sec_id}, {self.semester}-{self.year}"


class Takes(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    final_score = models.CharField(default='-', max_length=10) 
    grade = models.CharField(default='-', max_length=2)
    isKuesionerFilled = models.BooleanField(default = False)

    def __str__(self):
        return f"{self.student}, {self.section}, {self.grade}"
    
    def get_student_takes(self, Section):
        t = Takes.objects.filter(section = Section).order_by('student__nim')
        student_nim_list = []
        student_name_list = []
        for obj in t:
            student_nim_list.append(obj.student.nim)
            student_name_list.append(obj.student.name)
        return student_nim_list, student_name_list

    def get_individual_student_takes(self, nim, section):
        return Takes.objects.filter(student__nim = nim, section = section)

class ListKomponenScore(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    komponen = ArrayField(models.CharField(max_length=100))

    DEFAULT_KOMPONEN = ['uts1', 'uts2', 'uas', 'kuis', 'tutorial']

    def __str__(self):
        return f"{self.section} - {self.komponen}"

    def setListKomponenScores(self, section, columns, default = False):
        if(default):
            columns = self.DEFAULT_KOMPONEN

        check = ListKomponenScore.objects.filter(section = section)
        different = False
        if(len(check) != 0):
            if(len(columns) != len(check[0].komponen)):
                check[0].delete()
                new_komponen = ListKomponenScore.objects.create(section = section, komponen = columns)
                different = True
            else:
                for i in range(len(columns)):
                    different = (columns[i].lower() != check[0].komponen[i].lower())
                    if(different):
                        check[0].delete()
                        new_komponen = ListKomponenScore.objects.create(section = section, komponen = columns)
                        break
        else:
            new_komponen = ListKomponenScore.objects.create(section = section, komponen = columns)
            different = True

        if(different):
            bobot = BobotKomponenScores.objects.filter(section = section)
            if(len(bobot) != 0):
                bobot[0].delete()


            from Dosen.models import BobotIndeks
            persentase = BobotIndeks.objects.filter(section = section)
            if(len(persentase) != 0):
                persentase[0].delete()

        return different

class Scores(models.Model):
    takes = models.ForeignKey(Takes, on_delete=models.CASCADE)
    scores = ArrayField(models.IntegerField())

    def __str__(self):
        return f"{self.takes}, Skor:{self.scores}"

    def getStudentTakesScores(self, course_id, year, semester, section_id):
        scores = Scores.objects.filter( 
            takes__section__course__course_id = course_id, 
            takes__section__year = year, 
            takes__section__semester = semester,
            takes__section__sec_id = section_id).order_by('takes__student__nim')
        score_list = []

        for obj in scores:
            score_list.append(obj)
        return scores

    def setStudentScore(self, takes, row):
        check = Scores.objects.filter(takes = takes)
        if(len(check) != 0):
            check[0].delete()
        new_score = Scores.objects.create(takes = takes, scores = row)

class Score(models.Model):
    takes = models.ForeignKey(Takes, on_delete=models.CASCADE)
    uts1 = models.IntegerField()
    uts2 = models.IntegerField()
    uas = models.IntegerField()
    kuis = models.IntegerField()
    tutorial = models.IntegerField()

    def __str__(self):
        return f"{self.takes}, UTS1:{self.uts1}, UTS2:{self.uts2}, UAS:{self.uas}, Kuis:{self.kuis}, Tutorial:{self.tutorial}"

    def getStudentTakesScores(self, course_id, year, semester, section_id):
        scores = Score.objects.filter( 
            takes__section__course__course_id = course_id, 
            takes__section__year = year, 
            takes__section__semester = semester,
            takes__section__sec_id = section_id)
        score_list = []

        for obj in scores:
            score_list.append(obj)
        return scores

    def getStudentScore(self, nim, course_id, year, semester, section_id):
        return Score.objects.filter(takes__student__nim=nim, 
            takes__section__course__course_id = course_id, 
            takes__section__year = year, 
            takes__section__semester = semester,
            takes__section__sec_id = section_id)

    def setStudentScore(self, nim, course_id, year, semester, section_id, nilai_uts1, nilai_uts2, nilai_uas, nilai_kuis, nilai_tutorial):
        course_filter = Course.objects.filter(course_id=course_id)
        if(len(course_filter) == 0):
            return False
        course = course_filter[0]

        student_filter = Student.objects.filter(nim=nim)
        if(len(student_filter) == 0):
            return False
        student = student_filter[0]

        section = Section.objects.get(course__course_id = course_id, sec_id = section_id, year = year, semester = semester)
        takes = Takes.get_individual_student_takes(Takes, nim, section)
        if(len(takes) != 0):
            score = self.getStudentScore(self, nim = nim, course_id = course_id, year = year, semester = semester, section_id = section_id)
            if(len(score) != 0):
                score[0].delete()
            new_score = Score.objects.create(takes = takes[0], uts1=nilai_uts1, uts2=nilai_uts2, uas=nilai_uas, kuis=nilai_kuis, tutorial=nilai_tutorial)
            return True
        return False

class BobotKomponenScore(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    uts1 = ArrayField(models.IntegerField())
    uts2 = ArrayField(models.IntegerField())
    uas = ArrayField(models.IntegerField())
    kuis = ArrayField(models.IntegerField())
    tutorial = ArrayField(models.IntegerField())

    def __str__(self):
        return f"{self.course}, UTS1:{self.uts1}, UTS2:{self.uts2}, UAS:{self.uas}, Kuis:{self.kuis}, Tutorial:{self.tutorial}"

class BobotKomponenScores(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    bobot = ArrayField(ArrayField(models.IntegerField()))

    def __str__(self):
        return f"{self.section}, bobot:{self.bobot}"

class ResponseKerjasama(models.Model):
    takes = models.ForeignKey(Takes, on_delete=models.CASCADE)
    Kontribusi = models.IntegerField()
    PemecahanMasalah = models.IntegerField()
    Sikap = models.IntegerField()
    FokusTerhadapTugas = models.IntegerField()
    BekerjaDenganOrangLain = models.IntegerField()

    def __str__(self):
        return f"Mahasiswa: {self.takes.student} Matkul: {self.takes.section.course_id} Kontribusi: {self.Kontribusi} PemecahanMasalah: {self.PemecahanMasalah} Sikap: {self.Sikap} FokusTerhadapTugas: {self.FokusTerhadapTugas} BekerjaDenganOrangLain: {self.BekerjaDenganOrangLain}"
        
class ResponseKomunikasi(models.Model):
    takes = models.ForeignKey(Takes, on_delete=models.CASCADE)
    kelompok = models.IntegerField(default=1)
    Penyampaian1 = models.IntegerField()
    Penyampaian2 = models.IntegerField()
    Penyampaian3 = models.IntegerField()
    Penyampaian4 = models.IntegerField()
    Konten = models.IntegerField()
    Bahasa = models.IntegerField()
    Penguasaan = models.IntegerField()
    Menjawab = models.IntegerField()
    Media = models.IntegerField()
    Waktu = models.IntegerField()

    def __str__(self):
        return f"Mahasiswa: {self.takes.student} Kelompok: {self.kelompok} Matkul: {self.takes.section.course_id} CaraPenyampaianInformasi1: {self.Penyampaian1} CaraPenyampaianInformasi2: {self.Penyampaian2} CaraPenyampaianInformasi3: {self.Penyampaian3} CaraPenyampaianInformasi4: {self.Penyampaian4} KontenInformasiYangDisampaikan: {self.Konten} BahasaYangDigunakanDalamPenyampaianInformasi: {self.Bahasa} PenguasaanMateri: {self.Penguasaan} MenjawabPertanyaan: {self.Menjawab} PenggunaanMediaPendukung: {self.Media} MenggunakanWaktuDenganEfektifDanEfisien: {self.Waktu}"

class ResponseKuesioner(models.Model):
    takes = models.ForeignKey(Takes, on_delete=models.CASCADE)
    Kuesioner1 = models.IntegerField()
    Kuesioner2 = models.IntegerField()
    Kuesioner3 = models.IntegerField()
    Kuesioner4 = models.IntegerField()
    Kuesioner5 = models.IntegerField()
    Kuesioner6 = models.IntegerField()
    Kuesioner7 = models.IntegerField()
    Kuesioner8 = models.IntegerField()
    Kuesioner9 = models.IntegerField()
    Kuesioner10 = models.IntegerField()
    Kuesioner11 = models.IntegerField()
    Kuesioner12 = models.IntegerField()

    def __str__(self):
        return f"Mahasiswa: {self.takes.student} Matkul: {self.takes.section.course_id} \
        Informasi Yang Cukup: {self.Kuesioner1} \
        Pelaksanaan: {self.Kuesioner2} \
        Menguasai: {self.Kuesioner3} \
        Perkuliahan Terorganisir: {self.Kuesioner4} \
        Komunikasi Dosen: {self.Kuesioner5} \
        Kepedulian Dosen: {self.Kuesioner6} \
        Keadilan Dosen: {self.Kuesioner7} \
        Beban Kerja Sesuai: {self.Kuesioner8} \
        Sarana Prasarana: {self.Kuesioner9} \
        Fasilitas Pendukung: {self.Kuesioner10} \
        Usaha: {self.Kuesioner11} \
        PengalamanBelajar: {self.Kuesioner12} \
        "


class LOSuplemenSemester(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    semester = models.IntegerField()
    year = models.IntegerField()
    lo_a = models.FloatField()
    lo_b = models.FloatField()
    lo_c = models.FloatField()
    lo_d = models.FloatField()
    lo_e = models.FloatField()
    lo_f = models.FloatField()
    lo_g = models.FloatField()

class LOSuplemenCourse(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    lo_a = models.FloatField()
    lo_b = models.FloatField()
    lo_c = models.FloatField()
    lo_d = models.FloatField()
    lo_e = models.FloatField()
    lo_f = models.FloatField()
    lo_g = models.FloatField()

class CourseAssessmentScore(models.Model):
    semester = models.IntegerField()
    year = models.IntegerField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    section_count = models.IntegerField(default = 1)
    section_count_str = models.CharField(max_length = 9)

    courseOutcomeScore = models.FloatField()
    kuesionerScore = models.FloatField()
    portfolioScore = models.FloatField(default = 4.0)

    finalScore = models.FloatField()

    def setCourseAssessment(self, semester, year, course_id, section_count, courseOutcomeScore, kuesionerScore, finalScore):
        courseAssessment = CourseAssessmentScore.objects.filter(semester = semester, year = year, course__course_id = course_id)

        if(len(courseAssessment) != 0):
            courseAssessment[0].courseOutcomeScore = courseOutcomeScore
            courseAssessment[0].kuesionerScore = kuesionerScore
            courseAssessment[0].finalScore = finalScore
            courseAssessment[0].section_count = section_count
            courseAssessment[0].section_count_str = self.sectionCountView(self, section_count)
            
            courseAssessment[0].save()
            return courseAssessment[0]
        else:
            course = Course.objects.get(course_id = course_id)
            courseAssessmentScore = CourseAssessmentScore.objects.create(semester = semester, year = year, 
                course = course, section_count = section_count, section_count_str = self.sectionCountView(self, section_count),
                courseOutcomeScore = courseOutcomeScore, kuesionerScore = kuesionerScore, finalScore = finalScore)
            return courseAssessmentScore

    def sectionCountView(self, count):
        if(count == 1):
            return "K1"
        else:
            return "K1 - K" + str(count)