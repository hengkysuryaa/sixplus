from django.shortcuts import render

# Create your views here.
from LO.models import Score, Course, BobotKomponenScore, LO, ResponseKerjasama, ResponseKomunikasi
from Mahasiswa.models import Student

# Konstanta
BOBOT_FORM_KOMUNIKASI = 100 # dalam persen
BOBOT_FORM_KERJASAMA = 100 # dalam persen
#TODO apabila ada perubahan jumlah komponen dapat diganti disini
komponen_nilai_list = ["uts1", "uts2", "uas", "kuis", "tutorial"]

##########################
### HOMEPAGE MAHASISWA ###
##########################
def HomepageMahasiswaView(request):
    return render(request, 'Mahasiswa/mahasiswa.html')

def TestView(request):
    
    score = calculateLO("13120002", "MS1210")
    summarizeResponseKomunikasi("13120002", "MS1210")
    return render(request, 'Mahasiswa/test.html', {'score' : score})

def scaleScore(_nim, _course_id):
    std = Student.objects.filter(nim=_nim)
    course = Course.objects.filter(course_id=_course_id)
    std_score = list(Score.objects.filter(nim=std[0], course=course[0]).values())[0]
    
    # #TODO apabila ada perubahan jumlah komponen dapat diganti disini
    # komponen_nilai_list = ["uts1", "uts2", "uas", "kuis", "tutorial"]

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

    # #TODO apabila ada perubahan jumlah komponen dapat diganti disini
    # komponen_nilai_list = ["uts1", "uts2", "uas", "kuis", "tutorial"]

    for i in range(n):
        komponen_dict = {}
        for j in range(len(komponen_nilai_list)):
            komponen_dict[komponen_nilai_list[j]] = bobot_list.get(komponen_nilai_list[j])[i]
        dict[lo_list[i]] = komponen_dict
    
    return dict

def mapScoreAndBobot(_nim, _course_id):
    score = scaleScore(_nim, _course_id)
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

def calculateLO(_nim, _course_id):
    map_score_dict = mapScoreAndBobot(_nim, _course_id)
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
        if (lo_keys[i] == 'lo_c' and summarizeResponseKomunikasi(_nim, _course_id) != -999):
            sum = sum + summarizeResponseKomunikasi(_nim, _course_id)
            sum_divisor = sum_divisor + (BOBOT_FORM_KOMUNIKASI / 100)
        elif (lo_keys[i] == 'lo_e' and summarizeResponseKerjasama(_nim, _course_id) != -999):
            sum = sum + summarizeResponseKerjasama(_nim, _course_id)
            sum_divisor = sum_divisor + (BOBOT_FORM_KERJASAMA / 100)

        final_lo_score_dict[lo_keys[i]] = round(sum/sum_divisor, 2)
    
    final_lo_score_dict["course"] = str(Course.objects.filter(course_id=_course_id)[0])
    return final_lo_score_dict

def summarizeResponseKerjasama(_nim, _course_id):
    std = Student.objects.filter(nim=_nim)
    course = Course.objects.filter(course_id=_course_id)
    responses = list(ResponseKerjasama.objects.filter(student=std[0], course=course[0]).values())
    
    if (len(responses) == 0):
        return -999

    total_sum = float(0)
    
    for i in range(len(responses)):
        #TODO jika ada atribut yang ingin dihilangkan pop disini
        responses[i].pop('id')
        responses[i].pop('student_id')
        responses[i].pop('course_id')

        keys = list(responses[i].keys())
        sum = float(0)
        
        for j in range(len(keys)):
            sum = sum + float(responses[i].get(keys[i]))
        total_sum = total_sum + (sum / len(keys))
    
    total_sum = total_sum / len(responses)
    
    return total_sum

def summarizeResponseKomunikasi(_nim, _course_id):
    std = Student.objects.filter(nim=_nim)
    course = Course.objects.filter(course_id=_course_id)
    responses = list(ResponseKomunikasi.objects.filter(student=std[0], course=course[0]).values())
    
    if (len(responses) == 0):
        return -999
    
    total_sum = float(0)
    
    for i in range(len(responses)):
        #TODO jika ada atribut yang ingin dihilangkan pop disini
        responses[i].pop('id')
        responses[i].pop('student_id')
        responses[i].pop('kelompok')
        responses[i].pop('course_id')

        keys = list(responses[i].keys())
        sum = float(0)
        
        for j in range(len(keys)):
            sum = sum + float(responses[i].get(keys[i]))
        total_sum = total_sum + (sum / len(keys))
    
    total_sum = total_sum / len(responses)
    
    return total_sum