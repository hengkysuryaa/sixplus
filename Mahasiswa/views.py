from django.shortcuts import render

# Create your views here.
from LO.models import Score, Course, BobotKomponenScore, LO, ResponseKerjasama, ResponseKomunikasi, Takes, Section
from Mahasiswa.models import Student

# Konstanta
BOBOT_FORM_KOMUNIKASI = 100 # dalam persen
BOBOT_FORM_KERJASAMA = 100 # dalam persen
lo_list = ['lo_a', 'lo_b', 'lo_c', 'lo_d', 'lo_e', 'lo_f', 'lo_g']
KMT = {
    "L" : 1,
    "M" : 2,
    "H" : 3
}
komponen_nilai_list = ["uts1", "uts2", "uas", "kuis", "tutorial"] #TODO apabila ada perubahan jumlah komponen dapat diganti disini
INDEKS_LULUS = ["A", "AB", "B", "BC", "C", "D"]

def TestView(request):
    
    score = calculateLOSuplemen("13120002", 2020, 2)
    return render(request, 'Mahasiswa/test.html', {'score' : score})

def scaleScore(_nim, _course_id, _year, _semester):
    std = Student.objects.filter(nim=_nim)
    course = Course.objects.filter(course_id=_course_id)

    std_score = list(Score.objects.filter(takes__student=std[0], 
            takes__section__course = course[0], 
            takes__section__year = _year, 
            takes__section__semester = _semester).values())[0]

    score_dict = {}
    for i in range(len(komponen_nilai_list)):
        score_dict[komponen_nilai_list[i]] = std_score[komponen_nilai_list[i]] / 100 * 4

    return score_dict

def createLOAndBobotDict(_course_id):
    dict = {}

    #get LO list from a course
    lo_list = list(LO.getCourseLO(LO, _course_id)[0].keys())
    n = len(lo_list)

    #get bobot komponen score from a course
    course = Course.objects.filter(course_id=_course_id)
    bobot_list = list(BobotKomponenScore.objects.filter(course=course[0]).values())[0]

    for i in range(n):
        komponen_dict = {}
        for j in range(len(komponen_nilai_list)):
            komponen_dict[komponen_nilai_list[j]] = bobot_list.get(komponen_nilai_list[j])[i]
        dict[lo_list[i]] = komponen_dict
    
    return dict

def mapScoreAndBobot(_nim, _course_id, _year, _semester):
    score = scaleScore(_nim, _course_id, _year, _semester)
    lo_bobot_dict = createLOAndBobotDict(_course_id)

    score_keys = list(score.keys())
    lo_bobot_keys = list(lo_bobot_dict.keys())

    mapped_score_dict = {}

    for i in range(len(lo_bobot_keys)):
        mapped_score = {}
        for j in range(len(score_keys)):
            mapped_score[score_keys[j]] = float(score.get(score_keys[j])) * float(lo_bobot_dict.get(lo_bobot_keys[i]).get(score_keys[j]) / float(100))
        mapped_score_dict[lo_bobot_keys[i]] = mapped_score

    return mapped_score_dict

def calculateLO(_nim, _course_id,  _year, _semester):
    map_score_dict = mapScoreAndBobot(_nim, _course_id, _year, _semester)
    lo_bobot_dict = createLOAndBobotDict(_course_id)
    
    lo_keys = list(map_score_dict.keys())
    komponen_keys = list(list(map_score_dict.values())[0].keys())
    
    final_lo_score_dict = {}
    for i in range(len(lo_keys)):
        sum = float(0)
        sum_divisor = float(0)
        for j in range(len(komponen_keys)):
            sum = sum + map_score_dict.get(lo_keys[i]).get(komponen_keys[j])
            sum_divisor = sum_divisor + (lo_bobot_dict.get(lo_keys[i]).get(komponen_keys[j])/100)
        
        #TODO jika ada tambahan penilaian dari rubrik / form lain tambahkan disini
        if (lo_keys[i] == 'lo_c' and summarizeResponseKomunikasi(_nim, _course_id, _year, _semester) != -999):
            sum = sum + summarizeResponseKomunikasi(_nim, _course_id, _year, _semester)
            sum_divisor = sum_divisor + (BOBOT_FORM_KOMUNIKASI / 100)
        elif (lo_keys[i] == 'lo_e' and summarizeResponseKerjasama(_nim, _course_id, _year, _semester) != -999):
            sum = sum + summarizeResponseKerjasama(_nim, _course_id, _year, _semester)
            sum_divisor = sum_divisor + (BOBOT_FORM_KERJASAMA / 100)

        final_lo_score_dict[lo_keys[i]] = round(sum/sum_divisor, 2)
    
    final_lo_score_dict["course"] = Course.objects.filter(course_id=_course_id)[0]
    return final_lo_score_dict

def summarizeResponseKerjasama(_nim, _course_id, _year, _semester):
    std = Student.objects.filter(nim=_nim)
    course = Course.objects.filter(course_id=_course_id)
    section = Section.objects.filter(course=course[0], year=_year, semester=_semester)
    takes = Takes.objects.filter(student=std[0], section=section[0])
    
    responses = list(ResponseKerjasama.objects.filter(takes=takes[0]).values())
    
    if (len(responses) == 0):
        return -999

    total_sum = float(0)
    for i in range(len(responses)):
        #TODO jika ada atribut yang ingin dihilangkan pop disini
        responses[i].pop('id')
        responses[i].pop('takes_id')

        keys = list(responses[i].keys())
        sum = float(0)
        
        for j in range(len(keys)):
            sum = sum + float(responses[i].get(keys[j]))
        total_sum = total_sum + (sum / len(keys))
    
    total_sum = total_sum / len(responses)
    
    return total_sum

def summarizeResponseKomunikasi(_nim, _course_id, _year, _semester):
    std = Student.objects.filter(nim=_nim)
    course = Course.objects.filter(course_id=_course_id)
    section = Section.objects.filter(course=course[0], year=_year, semester=_semester)
    takes = Takes.objects.filter(student=std[0], section=section[0])
    
    responses = list(ResponseKomunikasi.objects.filter(takes=takes[0]).values())
    
    if (len(responses) == 0):
        return -999
    
    total_sum = float(0)
    
    for i in range(len(responses)):
        #TODO jika ada atribut yang ingin dihilangkan pop disini
        responses[i].pop('id')
        responses[i].pop('takes_id')
        responses[i].pop('kelompok')

        keys = list(responses[i].keys())
        sum = float(0)
        
        for j in range(len(keys)):
            sum = sum + float(responses[i].get(keys[j]))
        total_sum = total_sum + (sum / len(keys))
    
    total_sum = total_sum / len(responses)
    
    return total_sum

def calculateLOSuplemen(_nim, _year, _semester):
    
    takes_list = []
    std = Student.objects.filter(nim=_nim)
    section = Section.objects.filter(year=_year, semester=_semester)
    
    for item in section:
        if (len(Takes.objects.filter(student=std[0], section=item)) != 0):
            takes = Takes.objects.filter(student=std[0], section=item)[0]
            if (takes.grade in INDEKS_LULUS):
                _course_id = takes.section.course.course_id
                takes_list.append(calculateLO(_nim, _course_id, _year, _semester))

    lo_suplemen_dict = {}
    for i in range(len(lo_list)):
        sum = float(0)
        sum_divisor = float(0)
        for j in range(len(takes_list)):
            # iterasi suatu mata kuliah
            lo_course_list = LO.getCourseLO(LO, takes_list[j].get('course').course_id)[0]
            val = takes_list[j].get(lo_list[i])
            if (val != None):
                sum = sum + (val * float(KMT.get(lo_course_list.get(lo_list[i]))))
                sum_divisor = sum_divisor + float(KMT.get(lo_course_list.get(lo_list[i])))
        if (sum!=0 and sum_divisor!=0):
            lo_suplemen_dict[lo_list[i]] = round(sum/sum_divisor, 2)
        else:
            lo_suplemen_dict[lo_list[i]] = "-"

    return lo_suplemen_dict