# Create your views here.

from django.shortcuts import render
from django.shortcuts import redirect
from django.apps import apps
import cx_Oracle
from .forms import CarForm, GarajForm, OrasForm, SoferForm, ProducatorForm, ModelForm, AsiguratorForm, ConduceForm, AsiguraForm, CriteriuMasini, CriteriuSoferi, CriteriuOrase, CriteriuGaraje
from .forms import CriteriuAsiguratori, CriteriuProducatori, CriteriuModele, CriteriuConduce, CriteriuAsigura, VerifAsigForm, NrSoferi


def index(request):
    return render(request, 'index.html')

def connection():
    connection = cx_Oracle.connect(user = 'sys', password = '', dsn = '', encoding="UTF-8", mode=cx_Oracle.SYSDBA)
    return connection

def listmasini(request):

    if request.method == 'GET':
        sort = 'ID_MASINA'
        ord = 'ASC'
        crit = CriteriuMasini(request.POST)
        if crit.is_valid():
            sort = crit.cleaned_data.get('criteriu')
            ord = crit.cleaned_data.get('ord')
        cars = []
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM MASINI ORDER BY ID_MASINA ASC")
        for row in cursor.fetchall():
            cars.append({"id_masina": row[0], "model": row[1], "garaj_resedinta": row[2], "culoare": row[3], "nr_inmatriculare": row[4], "an_fabricatie": row[5]})
        conn.close()
        return render(request, 'listmasini.html', {'cars':cars, 'CriteriuMasini' : crit})
    if request.method == 'POST':
        sort = 'ID_MASINA'
        ord = 'ASC'
        crit = CriteriuMasini(request.POST)
        if crit.is_valid():
            sort = crit.cleaned_data.get('criteriu')
            ord = crit.cleaned_data.get('ord')
        cars = []
        conn = connection()
        cursor = conn.cursor()
        sql = "SELECT * FROM MASINI ORDER BY " + sort + ' ' + ord
        print(sql)
        cursor.execute(sql)
        for row in cursor.fetchall():
            cars.append({"id_masina": row[0], "model": row[1], "garaj_resedinta": row[2], "culoare": row[3], "nr_inmatriculare": row[4], "an_fabricatie": row[5]})
        conn.close()
        return render(request, 'listmasini.html', {'cars':cars, 'CriteriuMasini' : crit})

def addcar(request):
    if request.method == 'GET':
        form = CarForm()
        return render(request, 'addcar.html', {'CarForm': form})
    if request.method == 'POST':
        form = CarForm(request.POST)
        if form.is_valid():
            id_masina = form.cleaned_data.get("id_masina")
            model = form.cleaned_data.get("model")
            garaj_resedinta = form.cleaned_data.get("garaj_resedinta")
            culoare = form.cleaned_data.get("culoare")
            nr_inmatriculare = form.cleaned_data.get("nr_inmatriculare")
            an_fabricatie = form.cleaned_data.get("an_fabricatie")
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO MASINI VALUES (:id_masina, :model, :garaj_resedinta, :culoare, :nr_inmatriculare, :an_fabricatie)", [id_masina, model, garaj_resedinta, culoare, nr_inmatriculare, an_fabricatie])
        conn.commit()
        conn.close()
        return redirect('listmasini')

def deletecar(request, id):

    if request.method == 'GET':
        
        asig = []
        conduce = []

        conn = connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM ASIGURA WHERE ID_MASINA = :id", [id])
        for row in cursor.fetchall():
            asig.append({"id_masina": row[0], "id_asigurator": row[1], "data_inceput": row[2], "data_sfarsit": row[3], "valoare_polita" : row[4]})

        cursor.execute("SELECT * FROM CONDUCE WHERE ID_MASINA = :id", [id])
        for row in cursor.fetchall():
            conduce.append({"id_masina": row[0], "id_sofer": row[1], "data_inceput": row[2], "data_sfarsit": row[3]})

        conn.close()
        return render(request, 'deletecar.html', {'asig' : asig, 'conduce' : conduce})

    if request.method == 'POST':
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM MASINI WHERE id_masina = :id", [id])
        conn.commit()
        conn.close()
        return redirect('listmasini')

def updatecar(request, id):
    cr = []
    conn = connection()
    cursor = conn.cursor()
    
    if request.method == 'GET':
        
        cursor.execute("SELECT * FROM MASINI WHERE id_masina = :id_masina", [id])
        row = cursor.fetchone()
        cr.append({"id_masina": row[0], "model": row[1], "garaj_resedinta": row[2], "culoare": row[3], "nr_inmatriculare": row[4], "an_fabricatie": row[5]})
        conn.close()
        form = CarForm(initial={'id_masina': row[0], "model": row[1], "garaj_resedinta": row[2], "culoare": row[3], "nr_inmatriculare": row[4], "an_fabricatie": row[5]})   
        return render(request, 'addcar.html', {'CarForm': form})
    if request.method == 'POST':
        form = CarForm(request.POST)
        if form.is_valid():
            id_masina = form.cleaned_data.get("id_masina")
            model = form.cleaned_data.get("model")
            garaj_resedinta = form.cleaned_data.get("garaj_resedinta")
            culoare = form.cleaned_data.get("culoare")
            nr_inmatriculare = form.cleaned_data.get("nr_inmatriculare")
            an_fabricatie = form.cleaned_data.get("an_fabricatie")
            cursor.execute("UPDATE MASINI SET id_masina = :id_masina, model = :model, garaj_resedinta = :garaj_resedinta, culoare = :culoare, nr_inmatriculare = :nr_inmatriculare, an_fabricatie = :an_fabricatie WHERE id_masina = :id_masina", [id_masina, model, garaj_resedinta, culoare, nr_inmatriculare, an_fabricatie, id_masina])
            conn.commit()
        conn.close()
        return redirect('listmasini')

def listgaraje(request):
    
    if request.method == 'GET':
        sort = 'ID_GARAJ'
        ord = 'ASC'
        crit = CriteriuGaraje(request.POST)
        if crit.is_valid():
            sort = crit.cleaned_data.get('criteriu')
            ord = crit.cleaned_data.get('ord')
        garaje = []
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM GARAJE ORDER BY ID_GARAJ ASC")
        for row in cursor.fetchall():
            garaje.append({"id_garaj": row[0], "nume": row[1], "id_oras": row[2], "sector": row[3], "strada": row[4], "numar": row[5]})
        conn.close()
        return render(request, 'listgaraje.html', {'garaje':garaje, 'CriteriuGaraje' : crit})

    if request.method == 'POST':
        sort = 'ID_GARAJ'
        ord = 'ASC'
        crit = CriteriuGaraje(request.POST)
        if crit.is_valid():
            sort = crit.cleaned_data.get('criteriu')
            ord = crit.cleaned_data.get('ord')
        garaje = []
        conn = connection()
        cursor = conn.cursor()
        sql = "SELECT * FROM GARAJE ORDER BY " + sort + ' ' + ord
        cursor.execute(sql)
        for row in cursor.fetchall():
            garaje.append({"id_garaj": row[0], "nume": row[1], "id_oras": row[2], "sector": row[3], "strada": row[4], "numar": row[5]})
        conn.close()
        return render(request, 'listgaraje.html', {'garaje':garaje, 'CriteriuGaraje' : crit})


def addgaraj(request):
    form = GarajForm()
    if request.method == 'GET':
        return render(request, 'addgaraj.html', {'GarajForm': GarajForm})
    if request.method == 'POST':
        form = GarajForm(request.POST)
        if form.is_valid():
            id_garaj = form.cleaned_data.get("id_garaj")
            nume = form.cleaned_data.get("nume")
            id_oras = form.cleaned_data.get("id_oras")
            sector = form.cleaned_data.get("sector")
            strada = form.cleaned_data.get("strada")
            numar = form.cleaned_data.get("numar")
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO GARAJE VALUES (:id_garaj, :nume, :id_oras, :sector, :strada, :numar)", [id_garaj, nume, id_oras, sector, strada, numar])
        conn.commit()
        conn.close()
        return redirect('listgaraje')


def deletegaraj(request, id):
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM GARAJE WHERE id_garaj = :id", [id])
    conn.commit()
    conn.close()
    return redirect('listgaraje')

def updategaraj(request, id):
    gr = []
    conn = connection()
    cursor = conn.cursor()
    
    if request.method == 'GET':
        
        cursor.execute("SELECT * FROM GARAJE WHERE id_garaj = :id_garaj", [id])
        row = cursor.fetchone()
        gr.append({"id_garaj": row[0], "nume": row[1], "id_oras": row[2], "sector": row[3], "strada": row[4], "numar": row[5]})
        conn.close()
        form = GarajForm(initial={"id_garaj": row[0], "nume": row[1], "id_oras": row[2], "sector": row[3], "strada": row[4], "numar": row[5]})   
        return render(request, 'addgaraj.html', {'GarajForm': form})

    if request.method == 'POST':
        form = GarajForm(request.POST)
        if form.is_valid():
            id_garaj = form.cleaned_data.get("id_garaj")
            nume = form.cleaned_data.get("nume")
            id_oras = form.cleaned_data.get("id_oras")
            sector = form.cleaned_data.get("sector")
            strada = form.cleaned_data.get("strada")
            numar = form.cleaned_data.get("numar")
            cursor.execute("UPDATE GARAJE SET id_garaj = :id_garaj, nume = :nume, id_oras = :id_oras, sector = :sector, strada = :strada, numar = :numar WHERE id_garaj = :id_garaj", [id_garaj, nume, id_oras, sector, strada, numar, id_garaj])
            conn.commit()
        conn.close()
        return redirect('listgaraje')

def listorase(request):

    if request.method == 'GET':
        sort = 'ID_ORAS'
        ord = 'ASC'
        crit = CriteriuOrase(request.POST)
        if crit.is_valid():
            sort = crit.cleaned_data.get('criteriu')
            ord = crit.cleaned_data.get('ord')
        orase = []
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ORASE ORDER BY ID_ORAS ASC")
        for row in cursor.fetchall():
            orase.append({"id_oras": row[0], "nume": row[1], "suprafata": row[2], "nr_locuitori": row[3], "judet": row[4], "port": row[5], "aeroport" : row[6]})
        conn.close()
        return render(request, 'listorase.html', {'orase':orase, 'CriteriuOras' : crit})

    if request.method == 'POST':
        sort = 'ID_ORAS'
        ord = 'ASC'
        crit = CriteriuOrase(request.POST)
        if crit.is_valid():
            sort = crit.cleaned_data.get('criteriu')
            ord = crit.cleaned_data.get('ord')
        
        orase = []
        conn = connection()
        cursor = conn.cursor()
        sql = "SELECT * FROM ORASE ORDER BY " + sort + ' ' + ord
        cursor.execute(sql)
        for row in cursor.fetchall():
            orase.append({"id_oras": row[0], "nume": row[1], "suprafata": row[2], "nr_locuitori": row[3], "judet": row[4], "port": row[5], "aeroport" : row[6]})
        conn.close()
        return render(request, 'listorase.html', {'orase':orase, 'CriteriuOras' : crit})
        

def addoras(request):
    form = OrasForm()
    if request.method == 'GET':
        return render(request, 'addoras.html', {'OrasForm': OrasForm})
    if request.method == 'POST':
        form = OrasForm(request.POST)
        if form.is_valid():
            id_oras = form.cleaned_data.get("id_oras")
            nume = form.cleaned_data.get("nume")
            suprafata = form.cleaned_data.get("suprafata")
            nr_locuitori = form.cleaned_data.get("nr_locuitori")
            judet = form.cleaned_data.get("judet")
            port = form.cleaned_data.get("port")
            aeroport = form.cleaned_data.get("aeroport")
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO ORASE VALUES (:id_oras, :nume, :suprafata, :nr_locuitori, :judet, :port, :aeroport)", [id_oras, nume, suprafata, nr_locuitori, judet, port, aeroport])
        conn.commit()
        conn.close()
        return redirect('listorase')

def deleteoras(request, id):
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ORASE WHERE id_oras = :id", [id])
    conn.commit()
    conn.close()
    return redirect('listorase')

def updateoras(request, id):
    oras = []
    conn = connection()
    cursor = conn.cursor()
    
    if request.method == 'GET':
        
        cursor.execute("SELECT * FROM ORASE WHERE id_oras = :id_oras", [id])
        row = cursor.fetchone()
        oras.append({"id_oras": row[0], "nume": row[1], "suprafata": row[2], "nr_locuitori": row[3], "judet": row[4], "port": row[5], "aeroport" : row[6]})
        conn.close()
        form = OrasForm(initial={"id_oras": row[0], "nume": row[1], "suprafata": row[2], "nr_locuitori": row[3], "judet": row[4], "port": row[5], "aeroport" : row[6]})   
        return render(request, 'addoras.html', {'OrasForm': form})

    if request.method == 'POST':
        form = OrasForm(request.POST)
        if form.is_valid():
            id_oras = form.cleaned_data.get("id_oras")
            nume = form.cleaned_data.get("nume")
            suprafata = form.cleaned_data.get("suprafata")
            nr_locuitori = form.cleaned_data.get("nr_locuitori")
            judet = form.cleaned_data.get("judet")
            port = form.cleaned_data.get("port")
            aeroport = form.cleaned_data.get("aeroport")
            cursor.execute("UPDATE ORASE SET id_oras = :id_oras, nume = :nume, suprafata = :suprafata, nr_locuitori = :nr_locuitori, judet = :judet, port = :port, aeroport = :aeroport WHERE id_oras = :id_oras", [id_oras, nume, suprafata, nr_locuitori, judet, port, aeroport, id_oras])
            conn.commit()
        conn.close()
        return redirect('listorase')

def listsoferi(request):

    if request.method == 'GET':
        sort = 'ID_SOFER'
        ord = 'ASC'
        crit = CriteriuSoferi(request.POST)
        if crit.is_valid():
            sort = crit.cleaned_data.get('criteriu')
            ord = crit.cleaned_data.get('ord')
        soferi = []
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM SOFERI ORDER BY ID_SOFER ASC")
        for row in cursor.fetchall():
            soferi.append({"id_sofer": row[0], "nume": row[1], "prenume": row[2], "cnp": row[3], "telefon": row[4], "email": row[5], "id_oras" : row[6]})
        conn.close()
        return render(request, 'listsoferi.html', {'soferi':soferi, 'CriteriuSoferi' : crit})

    if request.method == 'POST':
        sort = 'ID_MASINA'
        ord = 'ASC'
        crit = CriteriuSoferi(request.POST)
        if crit.is_valid():
            sort = crit.cleaned_data.get('criteriu')
            ord = crit.cleaned_data.get('ord')
        soferi = []
        conn = connection()
        cursor = conn.cursor()
        sql = "SELECT * FROM SOFERI ORDER BY " + sort + ' ' + ord
        print(sql)
        cursor.execute(sql)
        for row in cursor.fetchall():
            soferi.append({"id_sofer": row[0], "nume": row[1], "prenume": row[2], "cnp": row[3], "telefon": row[4], "email": row[5], "id_oras" : row[6]})
        conn.close()
        return render(request, 'listsoferi.html', {'soferi':soferi, 'CriteriuSoferi' : crit})

    

def addsofer(request):
    form = SoferForm()
    if request.method == 'GET':
        return render(request, 'addsofer.html', {'SoferForm': SoferForm})
    if request.method == 'POST':
        form = SoferForm(request.POST)
        if form.is_valid():
            id_sofer = form.cleaned_data.get("id_sofer")
            nume = form.cleaned_data.get("nume")
            prenume = form.cleaned_data.get("prenume")
            cnp = form.cleaned_data.get("cnp")
            telefon = form.cleaned_data.get("telefon")
            email = form.cleaned_data.get("email")
            id_oras = form.cleaned_data.get("id_oras")
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO SOFERI VALUES (:id_sofer, :nume, :prenume, :cnp, :telefon, :email, :id_oras)", [id_sofer, nume, prenume, cnp, telefon, email, id_oras])
        conn.commit()
        conn.close()
        return redirect('listsoferi')

def deletesofer(request, id):
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM SOFERI WHERE id_sofer = :id", [id])
    conn.commit()
    conn.close()
    return redirect('listsoferi')

def updatesofer(request, id):
    sofer = []
    conn = connection()
    cursor = conn.cursor()
    
    if request.method == 'GET':
        
        cursor.execute("SELECT * FROM SOFERI WHERE id_sofer = :id_sofer", [id])
        row = cursor.fetchone()
        sofer.append({"id_sofer": row[0], "nume": row[1], "prenume": row[2], "cnp": row[3], "telefon": row[4], "email": row[5], "id_oras" : row[6]})
        conn.close()
        form = SoferForm(initial={"id_sofer": row[0], "nume": row[1], "prenume": row[2], "cnp": row[3], "telefon": row[4], "email": row[5], "id_oras" : row[6]})   
        return render(request, 'addsofer.html', {'SoferForm': form})

    if request.method == 'POST':
        form = SoferForm(request.POST)
        if form.is_valid():
            id_sofer = form.cleaned_data.get("id_sofer")
            nume = form.cleaned_data.get("nume")
            prenume = form.cleaned_data.get("prenume")
            cnp = form.cleaned_data.get("cnp")
            telefon = form.cleaned_data.get("telefon")
            email = form.cleaned_data.get("email")
            id_oras = form.cleaned_data.get("id_oras")
            cursor.execute("UPDATE SOFERI SET id_sofer = :id_sofer, nume = :nume, prenume = :prenume, cnp = :cnp, telefon = :telefon, email = :email, id_oras = :id_oras WHERE id_sofer = :id_sofer", [id_sofer, nume, prenume, cnp, telefon, email, id_oras, id_sofer])
            conn.commit()
        conn.close()
        return redirect('listsoferi')

def listproducatori(request):

    if request.method == 'GET':
        sort = 'ID_PRODUCATOR'
        ord = 'ASC'
        crit = CriteriuProducatori(request.POST)
        if crit.is_valid():
            sort = crit.cleaned_data.get('criteriu')
            ord = crit.cleaned_data.get('ord')
        producatori = []
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM PRODUCATORI ORDER BY ID_PRODUCATOR")
        for row in cursor.fetchall():
            producatori.append({"id_producator": row[0], "nume": row[1], "tara_origine": row[2], "an_infiintare": row[3], "website": row[4]})
        conn.close()
        return render(request, 'listproducatori.html', {'producatori':producatori, 'CriteriuProducatori' : crit})

    if request.method == 'POST':
        sort = 'ID_PRODUCATOR'
        ord = 'ASC'
        crit = CriteriuProducatori(request.POST)
        if crit.is_valid():
            sort = crit.cleaned_data.get('criteriu')
            ord = crit.cleaned_data.get('ord')
        producatori = []
        conn = connection()
        cursor = conn.cursor()
        sql = "SELECT * FROM PRODUCATORI ORDER BY " + sort + ' ' + ord
        cursor.execute(sql)
        for row in cursor.fetchall():
            producatori.append({"id_producator": row[0], "nume": row[1], "tara_origine": row[2], "an_infiintare": row[3], "website": row[4]})
        conn.close()
        return render(request, 'listproducatori.html', {'producatori':producatori, 'CriteriuProducatori' : crit})

def addproducator(request):
    form = ProducatorForm()
    if request.method == 'GET':
        return render(request, 'addproducator.html', {'ProducatorForm': ProducatorForm})
    if request.method == 'POST':
        form = ProducatorForm(request.POST)
        if form.is_valid():
            id_producator = form.cleaned_data.get("id_producator")
            nume = form.cleaned_data.get("nume")
            tara_origine = form.cleaned_data.get("tara_origine")
            an_infiintare = form.cleaned_data.get("an_infiintare")
            website = form.cleaned_data.get("website")
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO PRODUCATORI VALUES (:id_producator, :nume, :tara_origine, :an_infiintare, :website)", [id_producator, nume, tara_origine, an_infiintare, website])
        conn.commit()
        conn.close()
        return redirect('listproducatori')

def deleteproducator(request, id):
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM PRODUCATORI WHERE id_producator = :id", [id])
    conn.commit()
    conn.close()
    return redirect('listproducatori')

def updateproducator(request, id):
    producator = []
    conn = connection()
    cursor = conn.cursor()
    
    if request.method == 'GET':
        
        cursor.execute("SELECT * FROM PRODUCATORI WHERE id_producator = :id_producator", [id])
        row = cursor.fetchone()
        producator.append({"id_producator": row[0], "nume": row[1], "tara_origine": row[2], "an_infiintare": row[3], "website": row[4]})
        conn.close()
        form = ProducatorForm(initial={"id_producator": row[0], "nume": row[1], "tara_origine": row[2], "an_infiintare": row[3], "website": row[4]})   
        return render(request, 'addproducator.html', {'ProducatorForm': form})

    if request.method == 'POST':
        form = ProducatorForm(request.POST)
        if form.is_valid():
            id_producator = form.cleaned_data.get("id_producator")
            nume = form.cleaned_data.get("nume")
            tara_origine = form.cleaned_data.get("tara_origine")
            an_infiintare = form.cleaned_data.get("an_infiintare")
            website = form.cleaned_data.get("website")
            cursor.execute("UPDATE PRODUCATORI SET id_producator = :id_producator, nume = :nume, tara_origine = :tara_origine, an_infiintare = :an_infiintare, website = :website WHERE id_producator = :id_producator", [id_producator, nume, tara_origine, an_infiintare, website, id_producator])
            conn.commit()
        conn.close()
        return redirect('listproducatori')

def listmodele(request):

    if request.method == 'GET':
        sort = 'ID_PRODUCATOR'
        ord = 'ASC'
        crit = CriteriuModele(request.POST)
        if crit.is_valid():
            sort = crit.cleaned_data.get('criteriu')
            ord = crit.cleaned_data.get('ord')
        modele = []
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM MODELE ORDER BY ID_MODEL")
        for row in cursor.fetchall():
            modele.append({"id_model": row[0], "nume": row[1], "producator": row[2], "capacitate_motor": row[3], "combustibil" : row[4], "greutate" : row[5], "inaltime" : row[6]})
        conn.close()
        return render(request, 'listmodele.html', {'modele':modele, 'CriteriuModele' : crit})

    if request.method == 'POST':
        sort = 'ID_PRODUCATOR'
        ord = 'ASC'
        crit = CriteriuModele(request.POST)
        if crit.is_valid():
            sort = crit.cleaned_data.get('criteriu')
            ord = crit.cleaned_data.get('ord')
        modele = []
        conn = connection()
        cursor = conn.cursor()
        sql = "SELECT * FROM MODELE ORDER BY " + sort +  ' ' + ord
        cursor.execute(sql)
        for row in cursor.fetchall():
            modele.append({"id_model": row[0], "nume": row[1], "producator": row[2], "capacitate_motor": row[3], "combustibil" : row[4], "greutate" : row[5], "inaltime" : row[6]})
        conn.close()
        return render(request, 'listmodele.html', {'modele':modele, 'CriteriuModele' : crit})

def addmodel(request):
    form = ModelForm()
    if request.method == 'GET':
        return render(request, 'addmodel.html', {'ModelForm': ModelForm})
    if request.method == 'POST':
        form = ModelForm(request.POST)
        if form.is_valid():
            id_model = form.cleaned_data.get("id_model")
            nume = form.cleaned_data.get("nume")
            producator = form.cleaned_data.get("producator")
            capacitate_motor = form.cleaned_data.get("capacitate_motor")
            combustibil = form.cleaned_data.get("combustibil")
            greutate = form.cleaned_data.get("greutate")
            inaltime = form.cleaned_data.get("inaltime")

        conn = connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO MODELE VALUES (:id_model, :nume, :producator, :capacitate_motor, :combustibil, :greutate, :inaltime)", [id_model, nume, producator, capacitate_motor, combustibil, greutate, inaltime])
        conn.commit()
        conn.close()
        return redirect('listmodele')

def deletemodel(request, id):
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM MODELE WHERE id_model = :id", [id])
    conn.commit()
    conn.close()
    return redirect('listmodele')

def updatemodel(request, id):
    model = []
    conn = connection()
    cursor = conn.cursor()
    
    if request.method == 'GET':
        
        cursor.execute("SELECT * FROM MODELE WHERE id_model = :id_model", [id])
        row = cursor.fetchone()
        model.append({"id_model": row[0], "nume": row[1], "producator": row[2], "capacitate_motor": row[3], "combustibil" : row[4], "greutate" : row[5], "inaltime" : row[6]})
        conn.close()
        form = ModelForm(initial={"id_model": row[0], "nume": row[1], "producator": row[2], "capacitate_motor": row[3], "combustibil" : row[4], "greutate" : row[5], "inaltime" : row[6]})   
        return render(request, 'addmodel.html', {'ModelForm': form})

    if request.method == 'POST':
        form = ModelForm(request.POST)
        if form.is_valid():
            id_model = form.cleaned_data.get("id_model")
            nume = form.cleaned_data.get("nume")
            producator = form.cleaned_data.get("producator")
            capacitate_motor = form.cleaned_data.get("capacitate_motor")
            combustibil = form.cleaned_data.get("combustibil")
            greutate = form.cleaned_data.get("greutate")
            inaltime = form.cleaned_data.get("inaltime")
            cursor.execute("UPDATE MODELE SET id_model = :id_model, nume = :nume, producator = :producator, capacitate_motor = :capacitate_motor, combustibil = :combustibil, greutate = :greutate, inaltime = :inaltime WHERE id_model = :id_model", [id_model, nume, producator, capacitate_motor, combustibil, greutate, inaltime, id_model])
            conn.commit()
        conn.close()
        return redirect('listmodele')

def listasiguratori(request):

    if request.method == 'GET':
        sort = 'ID_ASIGURATOR'
        ord = 'ASC'
        crit = CriteriuAsiguratori(request.POST)
        if crit.is_valid():
            sort = crit.cleaned_data.get('criteriu')
            ord = crit.cleaned_data.get('ord')
        asiguratori = []
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ASIGURATORI ORDER BY ID_ASIGURATOR")
        for row in cursor.fetchall():
            asiguratori.append({"id_asigurator": row[0], "nume": row[1], "email": row[2], "telefon": row[3], "website": row[4]})
        conn.close()
        return render(request, 'listasiguratori.html', {'asiguratori':asiguratori, 'CriteriuAsiguratori' : crit})

    if request.method == 'POST':
        sort = 'ID_ASIGURATOR'
        ord = 'ASC'
        crit = CriteriuAsiguratori(request.POST)
        if crit.is_valid():
            sort = crit.cleaned_data.get('criteriu')
            ord = crit.cleaned_data.get('ord')
        asiguratori = []
        conn = connection()
        cursor = conn.cursor()
        sql = "SELECT * FROM ASIGURATORI ORDER BY " + sort + ' ' + ord
        cursor.execute(sql)
        for row in cursor.fetchall():
            asiguratori.append({"id_asigurator": row[0], "nume": row[1], "email": row[2], "telefon": row[3], "website": row[4]})
        conn.close()
        return render(request, 'listasiguratori.html', {'asiguratori':asiguratori, 'CriteriuAsiguratori' : crit})
        
def addasigurator(request):
    form = AsiguratorForm()
    if request.method == 'GET':
        return render(request, 'addasigurator.html', {'AsiguratorForm': AsiguratorForm})
    if request.method == 'POST':
        form = AsiguratorForm(request.POST)
        if form.is_valid():
            id_asigurator = form.cleaned_data.get("id_asigurator")
            nume = form.cleaned_data.get("nume")
            email = form.cleaned_data.get("email")
            telefon = form.cleaned_data.get("telefon")
            website = form.cleaned_data.get("website")
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO ASIGURATORI VALUES (:id_asigurator, :nume, :email, :telefon, :website)", [id_asigurator, nume, email, telefon, website])
        conn.commit()
        conn.close()
        return redirect('listasiguratori')

def deleteasigurator(request, id):
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ASIGURATORI WHERE id_asigurator = :id", [id])
    conn.commit()
    conn.close()
    return redirect('listasiguratori')

def updateasigurator(request, id):
    asigurator = []
    conn = connection()
    cursor = conn.cursor()
    
    if request.method == 'GET':
        
        cursor.execute("SELECT * FROM ASIGURATORI WHERE id_asigurator = :id_asigurator", [id])
        row = cursor.fetchone()
        asigurator.append({"id_asigurator": row[0], "nume": row[1], "email": row[2], "telefon": row[3], "website": row[4]})
        conn.close()
        form = AsiguratorForm(initial={"id_asigurator": row[0], "nume": row[1], "email": row[2], "telefon": row[3], "website": row[4]})   
        return render(request, 'addasigurator.html', {'AsiguratorForm': form})

    if request.method == 'POST':
        form = AsiguratorForm(request.POST)
        if form.is_valid():
            id_asigurator = form.cleaned_data.get("id_asigurator")
            nume = form.cleaned_data.get("nume")
            email = form.cleaned_data.get("email")
            telefon = form.cleaned_data.get("telefon")
            website = form.cleaned_data.get("website")
            cursor.execute("UPDATE ASIGURATORI SET id_asigurator = :id_asigurator, nume = :nume, email = :email, telefon = :telefon, website = :website WHERE id_asigurator = :id_asigurator", [id_asigurator, nume, email, telefon, website, id_asigurator])
            conn.commit()
        conn.close()
        return redirect('listasiguratori')

def listconduce(request):
    if request.method == 'GET':
        sort = 'ID_MASINA'
        ord = 'ASC'
        crit = CriteriuConduce(request.POST)
        if crit.is_valid():
            sort = crit.cleaned_data.get('criteriu')
            ord = crit.cleaned_data.get('ord')
        conduce = []
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM CONDUCE ORDER BY ID_MASINA ASC")
        for row in cursor.fetchall():
            conduce.append({"id_masina": row[0], "id_sofer": row[1], "data_inceput": row[2], "data_sfarsit": row[3]})
        conn.close()
        return render(request, 'listconduce.html', {'conduce':conduce, 'CriteriuConduce' : crit})

    if request.method == 'POST':
        sort = 'ID_MASINA'
        ord = 'ASC'
        crit = CriteriuConduce(request.POST)
        if crit.is_valid():
            sort = crit.cleaned_data.get('criteriu')
            ord = crit.cleaned_data.get('ord')
        conduce = []
        conn = connection()
        cursor = conn.cursor()
        sql = "SELECT * FROM CONDUCE ORDER BY " + sort + ' ' + ord
        cursor.execute(sql)
        for row in cursor.fetchall():
            conduce.append({"id_masina": row[0], "id_sofer": row[1], "data_inceput": row[2], "data_sfarsit": row[3]})
        conn.close()
        return render(request, 'listconduce.html', {'conduce':conduce, 'CriteriuConduce' : crit})
        

def addconduce(request):
    form = ConduceForm()
    if request.method == 'GET':
        return render(request, 'addconduce.html', {'ConduceForm': ConduceForm})
    if request.method == 'POST':
        form = ConduceForm(request.POST)
        if form.is_valid():
            id_masina = form.cleaned_data.get("id_masina")
            id_sofer = form.cleaned_data.get("id_sofer")
            data_inceput = form.cleaned_data.get("data_inceput")
            data_sfarsit = form.cleaned_data.get("data_sfarsit")
            conn = connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO CONDUCE VALUES (:id_masina, :id_sofer, TO_DATE(:data_inceput), TO_DATE(:data_sfarsit))", [id_masina, id_sofer, data_inceput, data_sfarsit])
            conn.commit()
            conn.close()
        return redirect('listconduce')

def deleteconduce(request, id_masina, id_sofer):
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM CONDUCE WHERE id_masina = :id_masina AND id_sofer = :id_sofer", [id_masina, id_sofer])
    conn.commit()
    conn.close()
    return redirect('listconduce')

def updateconduce(request, id_masina, id_sofer):
    cond = []
    conn = connection()
    cursor = conn.cursor()
    
    if request.method == 'GET':
        
        cursor.execute("SELECT * FROM CONDUCE WHERE id_masina = :id_masina AND id_sofer = :id_sofer", [id_masina, id_sofer])
        row = cursor.fetchone()
        cond.append({"id_masina": row[0], "id_sofer": row[1], "data_inceput": row[2], "data_sfarsit": row[3]})
        conn.close()
        form = ConduceForm(initial={"id_masina": row[0], "id_sofer": row[1]})   
        return render(request, 'addconduce.html', {'ConduceForm': form})

    if request.method == 'POST':
        form = ConduceForm(request.POST)
        if form.is_valid():
            id_masina = form.cleaned_data.get("id_masina")
            id_sofer = form.cleaned_data.get("id_sofer")
            data_inceput = form.cleaned_data.get("data_inceput")
            data_sfarsit = form.cleaned_data.get("data_sfarsit")
            cursor.execute("UPDATE CONDUCE SET id_masina = :id_masina, id_sofer = :id_sofer, data_inceput = :data_inceput, data_sfarsit = :data_sfarsit WHERE id_masina = :id_masina AND id_sofer = :id_sofer", [id_masina, id_sofer, data_inceput, data_sfarsit, id_masina, id_sofer])
            conn.commit()
        conn.close()
        return redirect('listconduce')

def listasigura(request):

    if request.method == 'GET':
        sort = 'ID_MASINA'
        ord = 'ASC'
        crit = CriteriuAsigura(request.POST)
        if crit.is_valid():
            sort = crit.cleaned_data.get('criteriu')
            ord = crit.cleaned_data.get('ord')
        polita = []
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ASIGURA ORDER BY ID_MASINA")
        for row in cursor.fetchall():
            polita.append({"id_masina": row[0], "id_asigurator": row[1], "data_inceput": row[2], "data_sfarsit": row[3], "valoare_polita" : row[4]})
        conn.close()
        return render(request, 'listasigura.html', {'asigura':polita, 'CriteriuAsigura' : crit})

    if request.method == 'POST':
        sort = 'ID_MASINA'
        ord = 'ASC'
        crit = CriteriuAsigura(request.POST)
        if crit.is_valid():
            sort = crit.cleaned_data.get('criteriu')
            ord = crit.cleaned_data.get('ord')
        polita = []
        conn = connection()
        cursor = conn.cursor()
        sql = "SELECT * FROM ASIGURA ORDER BY " + sort + ' ' + ord
        cursor.execute(sql)
        for row in cursor.fetchall():
            polita.append({"id_masina": row[0], "id_asigurator": row[1], "data_inceput": row[2], "data_sfarsit": row[3], "valoare_polita" : row[4]})
        conn.close()
        return render(request, 'listasigura.html', {'asigura':polita, 'CriteriuAsigura' : crit})

def addasigura(request):
    form = AsiguraForm()
    if request.method == 'GET':
        return render(request, 'addasigura.html', {'AsiguraForm': AsiguraForm})
    if request.method == 'POST':
        form = AsiguraForm(request.POST)
        if form.is_valid():
            id_masina = form.cleaned_data.get("id_masina")
            id_asigurator = form.cleaned_data.get("id_asigurator")
            data_inceput = form.cleaned_data.get("data_inceput")
            data_sfarsit = form.cleaned_data.get("data_sfarsit")
            valoare_polita = form.cleaned_data.get("valoare_polita")
            conn = connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO ASIGURA VALUES (:id_masina, :id_asigurator, TO_DATE(:data_inceput), TO_DATE(:data_sfarsit), :valoare_polita)", [id_masina, id_asigurator, data_inceput, data_sfarsit, valoare_polita])
            conn.commit()
            conn.close()
        return redirect('listasigura')

def deleteasigura(request, id_masina, id_asigurator):
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ASIGURA WHERE id_masina = :id_masina AND id_asigurator = :id_asigurator", [id_masina, id_asigurator])
    conn.commit()
    conn.close()
    return redirect('listasigura')

def updateasigura(request, id_masina, id_asigurator):
    asig = []
    conn = connection()
    cursor = conn.cursor()
    
    if request.method == 'GET':
        
        cursor.execute("SELECT * FROM ASIGURA WHERE id_masina = :id_masina AND id_asigurator = :id_asigurator", [id_masina, id_asigurator])
        row = cursor.fetchone()
        asig.append({"id_masina": row[0], "id_sofer": row[1], "data_inceput": row[2], "data_sfarsit": row[3], "valoare_polita" : row[4]})
        conn.close()
        form = AsiguraForm(initial={"id_masina": row[0], "id_asigurator": row[1]})   
        return render(request, 'addasigura.html', {'AsiguraForm': form})

    if request.method == 'POST':
        form = AsiguraForm(request.POST)
        if form.is_valid():
            id_masina = form.cleaned_data.get("id_masina")
            id_asigurator = form.cleaned_data.get("id_asigurator")
            data_inceput = form.cleaned_data.get("data_inceput")
            data_sfarsit = form.cleaned_data.get("data_sfarsit")
            valoare_polita = form.cleaned_data.get("valoare_polita")
            cursor.execute("UPDATE ASIGURA SET id_masina = :id_masina, id_asigurator = :id_asigurator, data_inceput = :data_inceput, data_sfarsit = :data_sfarsit, valoare_polita = :valoare_polita WHERE id_masina = :id_masina AND id_asigurator = :id_asigurator", [id_masina, id_asigurator, data_inceput, data_sfarsit, valoare_polita, id_masina, id_asigurator])
            conn.commit()
        conn.close()
        return redirect('listasigura')


def verifica_asigurare(request):

    if request.method == 'GET':
        return render(request, 'verifica_asigurare.html', {'VerifAsigForm' : VerifAsigForm()})

    if request.method == 'POST':
        form = VerifAsigForm(request.POST)
        nr = ''
        if form.is_valid():
            nr = form.cleaned_data.get('nr_inmatriculare')

        masina = []
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("SELECT m.nr_inmatriculare, g.nume, a.data_sfarsit FROM MASINI m JOIN asigura a ON a.id_masina = m.id_masina JOIN asiguratori g ON g.id_asigurator = a.id_asigurator WHERE m.nr_inmatriculare = :nr_inm  AND a.data_sfarsit >= sysdate", [nr])
        for row in cursor.fetchall():
            masina.append({"nr_inmatriculare": row[0], "nume": row[1], "data_sfarsit": row[2]})
        conn.close()

        return render(request, 'verifica_asigurare.html', {'VerifAsigForm' : VerifAsigForm(), 'masina' : masina})


def nrsoferi(request):

    if request.method == 'GET':
        orase = []
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("SELECT O.NUME, COUNT(S.ID_SOFER) AS NR_SOFERI FROM SOFERI S JOIN ORASE O ON O.ID_ORAS = S.ID_ORAS GROUP BY(O.NUME)")
        for row in cursor.fetchall():
            orase.append({"nume": row[0], "nr_soferi": row[1]})
        conn.close()
        return render(request, 'nrsoferi.html', {'NrSoferi' : NrSoferi(), 'orase' : orase})

    if request.method == 'POST':
        form = NrSoferi(request.POST)
        min = 0
        max = 0
        if form.is_valid():
            min = form.cleaned_data.get('min')
            max = form.cleaned_data.get('max')
            
        orase = []
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("SELECT O.NUME, COUNT(S.ID_SOFER) AS NR_SOFERI FROM SOFERI S JOIN ORASE O ON O.ID_ORAS = S.ID_ORAS GROUP BY(O.NUME) HAVING COUNT(S.ID_SOFER) BETWEEN :min and :max", [min, max])
        for row in cursor.fetchall():
            orase.append({"nume": row[0], "nr_soferi": row[1]})
        conn.close()
        return render(request, 'nrsoferi.html', {'NrSoferi' : form, 'orase' : orase})

def orase_masini(request):

    masini = []
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ORASE_MASINI")
    for row in cursor.fetchall():
        masini.append({"id_masina": row[0], "model": row[1], "garaj_resedinta": row[2], "culoare": row[3], "nr_inmatriculare": row[4], "an_fabricatie": row[5], "oras" : row[6]})

    conn.close()

    return render(request, 'orasemasini.html', {'masini':masini})

def add_orase_masini(request):
    if request.method == 'GET':
        form = CarForm()
        return render(request, 'addcar.html', {'CarForm': form})
    if request.method == 'POST':
        form = CarForm(request.POST)
        if form.is_valid():
            id_masina = form.cleaned_data.get("id_masina")
            model = form.cleaned_data.get("model")
            garaj_resedinta = form.cleaned_data.get("garaj_resedinta")
            culoare = form.cleaned_data.get("culoare")
            nr_inmatriculare = form.cleaned_data.get("nr_inmatriculare")
            an_fabricatie = form.cleaned_data.get("an_fabricatie")
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO ORASE_MASINI (ID_MASINA, MODEL, GARAJ_RESEDINTA, CULOARE, NR_INMATRICULARE, AN_FABRICATIE) VALUES (:id_masina, :model, :garaj_resedinta, :culoare, :nr_inmatriculare, :an_fabricatie)", [id_masina, model, garaj_resedinta, culoare, nr_inmatriculare, an_fabricatie])
        conn.commit()
        conn.close()
        return redirect('orasemasini')

def delete_orase_masini(request, id):

    conn = connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ORASE_MASINI WHERE id_masina = :id", [id])
    conn.commit()
    conn.close()
    return redirect('orasemasini')

def update_orase_masini(request, id):

    cr = []
    conn = connection()
    cursor = conn.cursor()
    
    if request.method == 'GET':
        
        cursor.execute("SELECT * FROM ORASE_MASINI WHERE id_masina = :id_masina", [id])
        row = cursor.fetchone()
        cr.append({"id_masina": row[0], "model": row[1], "garaj_resedinta": row[2], "culoare": row[3], "nr_inmatriculare": row[4], "an_fabricatie": row[5]})
        conn.close()
        form = CarForm(initial={'id_masina': row[0], "model": row[1], "garaj_resedinta": row[2], "culoare": row[3], "nr_inmatriculare": row[4], "an_fabricatie": row[5]})   
        return render(request, 'addcar.html', {'CarForm': form})
    if request.method == 'POST':
        form = CarForm(request.POST)
        if form.is_valid():
            id_masina = form.cleaned_data.get("id_masina")
            model = form.cleaned_data.get("model")
            garaj_resedinta = form.cleaned_data.get("garaj_resedinta")
            culoare = form.cleaned_data.get("culoare")
            nr_inmatriculare = form.cleaned_data.get("nr_inmatriculare")
            an_fabricatie = form.cleaned_data.get("an_fabricatie")
            cursor.execute("UPDATE ORASE_MASINI SET id_masina = :id_masina, model = :model, garaj_resedinta = :garaj_resedinta, culoare = :culoare, nr_inmatriculare = :nr_inmatriculare, an_fabricatie = :an_fabricatie WHERE id_masina = :id_masina", [id_masina, model, garaj_resedinta, culoare, nr_inmatriculare, an_fabricatie, id_masina])
            conn.commit()
        conn.close()
        return redirect('orasemasini')

def nrvehicule(request):

    prod = []
    conn = connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM NR_VEHICULE")

    for row in cursor:
        prod.append({"nume" : row[0], "numar": row[1]})

    conn.close()

    return render(request, 'nrvehicule.html', {"prod" : prod})
