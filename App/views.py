from django.shortcuts import redirect, HttpResponse, render
from .models import korisnici, predmeti
from .models import upisi
from django.contrib.auth import logout,login,authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import DodajNoviPredmet, DodajNovogProfesora, DodajNovogStudenta, DodajPredmetProfesor, PromjeniKorisnikForm

# Create your views here.

def main(request):
    if not request.user.is_authenticated:
        return redirect('login')
    elif request.user.is_authenticated and request.user.role == 'stu':
        return redirect('student')
    elif request.user.is_authenticated and request.user.role == 'men':
        return redirect('mentor')


    if request.POST.get('dodaj-predmet-profesor-btn', False):
        form = DodajPredmetProfesor(request.POST)
        if form.is_valid():
            upis = upisi(student_id=form.cleaned_data["korisnik_id"],predmet_id=form.cleaned_data["predmet_id"],status=form.cleaned_data["status"])
            upis.save()
    elif request.POST.get('dodaj-predmet-btn', False):
        form = DodajNoviPredmet(request.POST)
        if form.is_valid():
            predmet = predmeti(name=form.cleaned_data["name"],kod=form.cleaned_data["kod"],program=form.cleaned_data["program"]
            ,ects=form.cleaned_data["ects"],sem_red=form.cleaned_data["sem_red"],sem_izv=form.cleaned_data["sem_izv"],
            izborni=form.cleaned_data["izborni"])
            predmet.save()
    elif request.POST.get('dodaj-novog-studenta-btn', False):
        form = DodajNovogStudenta(request.POST)
        if form.is_valid():
            form.save()



    lista_predmeta = predmeti.objects.all()
    lista_studenata = korisnici.objects.all().filter(role="stu")
    lista_profesora = korisnici.objects.all().filter(role="men")
    dodaj_novi_predmet_form = DodajNoviPredmet()
    dodaj_predmet_profesor_form = DodajPredmetProfesor()
    dodaj_novog_studenta_form = DodajNovogStudenta()
    dodaj_novog_profesora_form = DodajNovogProfesora()

    return render(request,'main.html',{'lista_predmeta':lista_predmeta,'dodaj_novi_predmet_form':dodaj_novi_predmet_form
    ,'dodaj_predmet_profesor_form':dodaj_predmet_profesor_form,'lista_studenata':lista_studenata,
    'dodaj_novog_studenta_form':dodaj_novog_studenta_form,'lista_profesora':lista_profesora,'dodaj_novog_profesora_form':dodaj_novog_profesora_form,
    })


def predmet_student_list(request,p_id):
    predmet = predmeti.objects.get(pk=p_id)
    upis_list = upisi.objects.all().filter(predmet_id=predmet)
    student_list = []
    for u in upis_list:
        if u.student_id.role == "stu":
            student_list.append(u.student_id)
    return render(request,'predmet-student-list.html',{'predmet':predmet,'student_list':student_list})

def predmet_promjena(request,p_id):
    if not request.user.is_staff:
        return redirect("main")
    predmet = predmeti.objects.get(pk=p_id)
    form = DodajNoviPredmet(initial={'name': predmet.name,'kod':predmet.kod,'program':predmet.program,'ects':predmet.ects,
    'sem_red':predmet.sem_red,'sem_izv':predmet.sem_izv,'izborni':predmet.izborni.upper()})

    if request.method == "POST":
        form = DodajNoviPredmet(request.POST)
        if form.is_valid():
            predmet.name = form.cleaned_data['name']
            predmet.kod = form.cleaned_data['kod']
            predmet.program = form.cleaned_data['program']
            predmet.ects = form.cleaned_data['ects']
            predmet.sem_red = form.cleaned_data['sem_red']
            predmet.sem_izv = form.cleaned_data['sem_izv']
            predmet.izborni = form.cleaned_data['izborni']
            predmet.save()
    return render(request,'promjena-predmet.html',{'form':form})

def korisnik_promjena(request,k_id):
    if not request.user.is_staff:
        return redirect("main")
    korisnik = korisnici.objects.get(pk=k_id)
    korisnik.password= ''
    form = PromjeniKorisnikForm(instance=korisnik)

    if request.method == "POST":
        form = PromjeniKorisnikForm(request.POST, instance=korisnik)
        if form.is_valid():
            korisnik.username = form.cleaned_data['username']
            korisnik.status = form.cleaned_data['status']
            korisnik.role = form.cleaned_data['role']
            korisnik.set_password(form.cleaned_data['password'])
            korisnik.save()
    return render(request,'promjena-korisnika.html',{'form':form})



def korisnik_upisni_list(request,s_id):
    if not request.user.is_staff:
        return redirect('main')
    user = korisnici.objects.get(pk=s_id)
    subjects = predmeti.objects.all()
    if request.POST.get('add', False):
        if not upisi.objects.filter(student_id=user.id,predmet_id=request.POST["add"]).exists():
            upis = upisi(student_id=user,predmet_id=predmeti.objects.get(pk=request.POST["add"]),status="Upisan")
            upis.save()
    elif request.POST.get('remove', False):
        if upisi.objects.filter(student_id=user.id,predmet_id=request.POST["remove"]).exists():
            upis = upisi.objects.get(predmet_id=request.POST["remove"],student_id=user.id)
            print(upis)
            upis.delete()
    
    upisi_korisnika = upisi.objects.all().filter(student_id=user.id)
    upisani_predmeti = []
    for u in upisi_korisnika:
        if user.status == 'red':
            upisani_predmeti.append(u.predmet_id)
        elif user.status == 'izv':
            upisani_predmeti.append(u.predmet_id)

    return render(request,'student-upisni-list.html',{'subjects':subjects,'user':user,'upisi':upisani_predmeti,
                                        'range':range(1,11)})




def student(request):
    user = request.user
    if (user.is_authenticated and user.role != 'stu') or not user.is_authenticated:
            return redirect('main')
    subjects = predmeti.objects.all()
    if request.POST.get('add', False):
        if not upisi.objects.filter(student_id=user.id,predmet_id=request.POST["add"]).exists():
            upis = upisi(student_id=user,predmet_id=predmeti.objects.get(pk=request.POST["add"]),status="Upisan")
            upis.save()


    elif request.POST.get('remove', False):
        if upisi.objects.filter(student_id=user.id,predmet_id=request.POST["remove"]).exists():
            upis = upisi.objects.get(predmet_id=request.POST["remove"],student_id=user.id)
            upis.delete()

    upisi_korisnika = upisi.objects.all().filter(student_id=user.id)
    upisani_predmeti = []
    for u in upisi_korisnika:
        if user.status == 'red':
            upisani_predmeti.append(u.predmet_id)
        elif user.status == 'izv':
            upisani_predmeti.append(u.predmet_id)

    return render(request, 'student.html', {'subjects':subjects,'user':user,'upisi':upisani_predmeti,
                                        'range':range(1,11)})




def logoutView(request):
    logout(request)
    return redirect('main')


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            us = request.POST['username']
            pa = request.POST['password']
            user = authenticate(request, username=us, password=pa)
            if user is not None:
                login(request, user)
                if user.role == "stu":
                    return redirect('student')
                elif user.role == "men":
                    return redirect('mentor')
                else:
                    return redirect('main')
    else:
        form = AuthenticationForm()
    return render(request,'login.html',{'form':form})


def mentor(request):
    user = request.user
    if user.role != 'men' or not user.is_authenticated:
        return redirect('main')
    svi_upisi = upisi.objects.all().filter(student_id=user.id)
    subjects = []
    print(svi_upisi)
    for u in svi_upisi:
        subjects.append(predmeti.objects.get(pk=u.predmet_id.id))
    print(subjects)


    return render(request,'mentor.html',{'subjects':subjects})


def mentor_predmet_list(request,p_id,slug):
    user = request.user
    if user.role != 'men' or not user.is_authenticated:
        return redirect('main')
    elif not upisi.objects.all().filter(student_id=request.user,predmet_id=p_id).exists():
        return redirect('main')

    if request.POST.get('status-change', False):
        if request.POST.getlist("status","none") != "none":
            upis = upisi.objects.get(predmet_id=p_id,student_id=request.POST["status-change"])
            if request.POST.getlist("status","none")[0] == "polozen":
                upis.status = "Položen"
            elif request.POST.getlist("status","none")[0] == "izgubio_potpis":
                upis.status = "Izgubio potpis"
            elif request.POST.getlist("status","none")[0] == "potpis":
                upis.status = "Dobio potpis ali nije položen"
            upis.save()

    students = []
    if slug == 'svi':
        svi_upisi = upisi.objects.all().filter(predmet_id=p_id)
        for u in svi_upisi:
            if u.student_id.role == 'stu':
                students.append(u)
    elif slug == 'izgubili-potpis':
        svi_upisi = upisi.objects.all().filter(predmet_id=p_id,status="Izgubio potpis")
        for u in svi_upisi:
            if u.student_id.role == 'stu':
                students.append(u)
    elif slug == 'dobili-potpis':
        svi_upisi = upisi.objects.all().filter(predmet_id=p_id,status="Dobio potpis ali nije položen")
        for u in svi_upisi:
            if u.student_id.role == 'stu':
                students.append(u)
    elif slug == 'polozili':
        svi_upisi = upisi.objects.all().filter(predmet_id=p_id,status="Položio")
        for u in svi_upisi:
            if u.student_id.role == 'stu':
                students.append(u)       
    return render(request,'mentor-predmet-list.html',{'students':students,'p_id':p_id})

