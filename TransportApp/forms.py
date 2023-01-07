from django import forms
import cx_Oracle

def connection():
    connection = cx_Oracle.connect(user = 'sys', password = '', dsn = '', encoding="UTF-8", mode=cx_Oracle.SYSDBA)
    return connection

judete = ['Alba', 'Arad', 'Argeş', 'Bacău', 'Bihor', 'Bistriţa-Năsăud', 'Botoşani', 'Brăila', 'Braşov',
'Buzău', 'București', 'Călăraşi', 'Caraş-Severin', 'Cluj', 'Constanţa', 'Covasna', 'Dâmboviţa', 'Dolj',
'Galaţi	', 'Giurgiu', 'Gorj', 'Harghita', 'Hunedoara', 'Ialomiţa', 'Iaşi', 'Ilfov', 'Maramureş', 'Mehedinţi',
'Mureş', 'Neamţ', 'Olt', 'Prahova', 'Sălaj', 'Satu Mare', 'Sibiu', 'Suceava', 'Teleorman', 'Timiş', 'Tulcea',
'Vaslui', 'Vâlcea', 'Vrancea']

listajudete = []

for judet in judete:
    listajudete.append((judet, judet))

da_nu = [('DA', 'DA'), ('NU', 'NU')]

# preluarea valorilor initiale

garaje = []
modele = []
masini = []
soferi = []
asiguratori = [] 
orase = []
producatori = []

conn = connection()
cursor = conn.cursor()

cursor.execute("SELECT NUME FROM GARAJE")
for row in cursor.fetchall():
    garaje.append((row[0],row[0]))

cursor.execute("SELECT NUME FROM MODELE")
for row in cursor.fetchall():
    modele.append((row[0],row[0]))

cursor.execute("SELECT ID_ORAS FROM ORASE")
for row in cursor.fetchall():
    orase.append((row[0], row[0]))

cursor.execute("SELECT NUME FROM PRODUCATORI")
for row in cursor.fetchall():
    producatori.append((row[0], row[0]))

cursor.execute("SELECT ID_MASINA FROM MASINI")
for row in cursor.fetchall():
    masini.append((row[0], row[0]))

cursor.execute("SELECT ID_SOFER FROM SOFERI")
for row in cursor.fetchall():
    soferi.append((row[0], row[0]))

cursor.execute("SELECT ID_ASIGURATOR FROM ASIGURATORI")
for row in cursor.fetchall():
    asiguratori.append((row[0], row[0]))

conn.close()

def update_garaje():
    garaje = []
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT NUME FROM GARAJE")

    for row in cursor.fetchall():
        garaje.append((row[0],row[0]))

    conn.close()
    return garaje

def update_modele():
    modele = []
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT NUME FROM MODELE")

    for row in cursor.fetchall():
        modele.append((row[0],row[0]))

    conn.close()
    return modele

def update_orase():
    orase = []
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT ID_ORAS FROM ORASE")

    for row in cursor.fetchall():
        orase.append((row[0], row[0]))

    conn.close()
    return orase

def update_producatori():
    producatori = []
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT NUME FROM PRODUCATORI")

    for row in cursor.fetchall():
        producatori.append((row[0], row[0]))

    conn.close()
    return producatori


class CarForm(forms.Form):

    # update in timp real al formularului
    def __init__(self, *args, **kwargs):
        super(CarForm, self).__init__(*args, **kwargs)
        garaje_ = update_garaje()
        modele_ = update_modele()
        self.fields['garaj_resedinta'] = forms.CharField(label='GARAJ RESEDINTA', widget=forms.Select(choices=garaje_),  required=True)
        self.fields['model'] = model = forms.CharField(label='MODEL', widget=forms.Select(choices=modele_),  required=True)

    id_masina = forms.IntegerField(label = 'ID MASINA', required=True)
    model = forms.CharField(label='MODEL', widget=forms.Select(choices=modele),  required=True)
    garaj_resedinta = forms.CharField(label='GARAJ RESEDINTA', widget=forms.Select(choices=garaje),  required=True)
    culoare = forms.CharField(max_length = 12, label = 'CULOARE',  required=True)
    nr_inmatriculare = forms.CharField(max_length=7, label = 'NR INMATRICULARE', required=False)
    an_fabricatie = forms.IntegerField(label = 'AN FABRICATIE',  required=True)

class GarajForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(GarajForm, self).__init__(*args, **kwargs)
        orase_ = update_orase()
        self.fields['id_oras'] = forms.IntegerField(label = 'ID ORAS', widget=forms.Select(choices = orase_), required=True)

    id_garaj = forms.IntegerField(label = 'ID GARAJ', required=True)
    nume = forms.CharField(max_length = 30, label = 'NUME',  required=True)
    id_oras = forms.IntegerField(label = 'ID ORAS', widget=forms.Select(choices = orase), required=True)
    sector = forms.IntegerField(label = 'SECTOR', required=False)
    strada = forms.CharField(max_length = 20, label = 'STRADA',  required=True)
    numar = forms.IntegerField(label = 'NUMAR', required=True)

class OrasForm(forms.Form):

    id_oras = forms.IntegerField(label = 'ID ORAS', required=True)
    nume = forms.CharField(max_length = 30, label = 'NUME',  required=True)
    suprafata = forms.IntegerField(label = 'SUPRAFATA', required=False)
    nr_locuitori = forms.IntegerField(label = 'NR LOCUITORI', required=False)
    judet = forms.CharField(max_length = 20, label = 'JUDET', widget=forms.Select(choices = listajudete), required=True)
    port = forms.CharField(max_length = 2, label = 'PORT', widget=forms.Select(choices = da_nu), required=False)
    aeroport = forms.CharField(max_length = 2, label = 'AEROPORT', widget=forms.Select(choices = da_nu), required=False)
    
class SoferForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(SoferForm, self).__init__(*args, **kwargs)
        orase_ = update_orase()
        self.fields['id_oras'] = forms.IntegerField(label = 'ID ORAS', widget=forms.Select(choices = orase_), required=True)

    id_sofer = forms.IntegerField(label = 'ID SOFER', required=True)
    nume = forms.CharField(max_length = 30, label = 'NUME',  required=True)
    prenume = forms.CharField(max_length = 30, label = 'PRENUME',  required=True)
    cnp = forms.CharField(max_length = 13, label = 'CNP',  required=True)
    telefon = forms.CharField(max_length = 12, label = 'TELEFON',  required=False)
    email = forms.EmailField(max_length = 40, label = "EMAIL", required=False)
    id_oras = forms.IntegerField(label = 'ID ORAS', widget=forms.Select(choices = orase), required=True)


class ProducatorForm(forms.Form):

    id_producator = forms.IntegerField(label = 'ID PRODUCATOR', required=True)
    nume = forms.CharField(max_length = 30, label = 'NUME',  required=True)
    tara_origine = forms.CharField(max_length = 30, label = 'TARA ORIGINE',  required=True)
    an_infiintare = forms.IntegerField(label = 'AN INFIINTARE', required=True)
    website = forms.CharField(max_length = 30, label = 'WEBSITE',  required=False)

class ModelForm(forms.Form):
    
    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        producatori_ = update_producatori()
        self.fields['producator'] = forms.CharField(label='PRODUCATOR', widget=forms.Select(choices=producatori_),  required=True)

    id_model = forms.IntegerField(label = 'ID MODEL', required=True)
    nume = forms.CharField(max_length = 30, label = 'NUME',  required=True)
    producator = forms.CharField(label='PRODUCATOR', widget=forms.Select(choices=producatori),  required=True)
    capacitate_motor = forms.IntegerField(label = 'CAPACITATE MOTOR', required=False)
    combustibil = forms.CharField(max_length = 20, label = 'COMBUSTIBIL',  required=True)
    greutate = forms.IntegerField(label = 'GREUTATE', required=True)
    inaltime = forms.IntegerField(label = 'INALTIME', required=True)

class AsiguratorForm(forms.Form):

    id_asigurator = forms.IntegerField(label = 'ID ASIGURATOR', required=True)
    nume = forms.CharField(max_length = 30, label = 'NUME',  required=True)
    email = forms.EmailField(max_length = 30, label = "EMAIL", required=False)
    telefon = forms.CharField(max_length = 12, label = 'TELEFON',  required=False)
    website = forms.CharField(max_length = 30, label = 'WEBSITE',  required=False)

class ConduceForm(forms.Form):

    id_masina = forms.IntegerField(label = 'ID MASINA', widget=forms.Select(choices=masini), required=True)
    id_sofer = forms.IntegerField(label = 'ID SOFER', widget=forms.Select(choices=soferi), required=True)
    data_inceput = forms.DateField(label = "DATA INCEPUT", help_text='dd/mm/yyyy', required=True, widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    data_sfarsit = forms.DateField(label = "DATA SFARSIT", help_text="dd/mm/yyyy", required=True, widget=forms.widgets.DateInput(attrs={'type': 'date'}))

class AsiguraForm(forms.Form):

    id_masina = forms.IntegerField(label = 'ID MASINA', widget=forms.Select(choices=masini), required=True)
    id_asigurator = forms.IntegerField(label = 'ID ASIGURATOR', widget=forms.Select(choices=asiguratori), required=True)
    data_inceput = forms.DateField(label = "DATA INCEPUT", help_text='dd/mm/yyyy', required=True, widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    data_sfarsit = forms.DateField(label = "DATA SFARSIT", help_text="dd/mm/yyyy", required=True, widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    valoare_polita = forms.IntegerField(label = 'VALOARE POLITA', required=True)

asc_desc = [('ASC', 'CRESCATOR'), ('DESC', 'DESCRESCATOR')]

CriteriiMasini = [('ID_MASINA', 'ID MASINA'), ('MODEL', 'MODEL'), ('GARAJ_RESEDINTA', 'GARAJ RESEDINTA'), ('CULOARE', 'CULOARE'),
('NR_INMATRICULARE', 'NR INMATRICULARE') ,('AN_FABRICATIE', 'AN FABRICATIE')]

CriteriiSoferi = [('ID_SOFER', 'ID SOFER'), ('NUME', 'NUME'), ('PRENUME', 'PRENUME'), ('CNP', 'CNP'),
('TELEFON', 'TELEFON'), ('EMAIL', 'EMAIL'), ('ID_ORAS', 'ID ORAS')]

CriteriiOrase = [('ID_ORAS', 'ID ORAS'), ('NUME', 'NUME'), ('SUPRAFATA', 'SUPRAFATA'), ('NR_LOCUITORI', 'NR LOCUITORI'),
('JUDET', 'JUDET'), ('PORT', 'PORT'), ('AEROPORT', 'AEROPORT')]

CriteriiGaraje = [('ID_GARAJ', 'ID GARAJ'), ('NUME', 'NUME'), ('ID_ORAS', 'ID ORAS'), ('SECTOR', 'SECTOR'),
 ('STRADA', 'STRADA'), ('NUMAR', 'NUMAR')]

CriteriiAsiguratori = [('ID_ASIGURATOR', 'ID ASIGURATOR'), ('NUME', 'NUME'), ('EMAIL', 'EMAIL'),
('TELEFON', 'TELEFON'), ('WEBSITE', 'WEBSITE')]

CriteriiProducatori = [('ID_PRODUCATOR', 'ID PRODUCATOR'), ('NUME', 'NUME'), ('TARA_ORIGINE', 'TARA ORIGINE'),
('AN_INFIINTARE', 'AN INFIINTARE'), ('WEBSITE', 'WEBSITE')]

CriteriiModele = [('ID_MODEL', 'ID MODEL'), ('NUME', 'NUME'), ('PRODUCATOR', 'PRODUCATOR'), ('CAPACITATE_MOTOR', 'CAPACITATE MOTOR'),
('COMBUSTIBIL', 'COMBUSTIBIL'), ('GREUTATE', 'GREUTATE'), ('INALTIME', 'INALTIME')]

CriteriiConduce = [('ID_MASINA', 'ID MASINA'), ('ID_SOFER', 'ID SOFER'),
('DATA_INCEPUT', 'DATA INCEPUT'), ('DATA_SFARSIT', 'DATA SFARSIT')]

CriteriiAsigura = [('ID_MASINA', 'ID MASINA'), ('ID_ASIGURATOR', 'ID ASIGURATOR'),
('DATA_INCEPUT', 'DATA INCEPUT'), ('DATA_SFARSIT', 'DATA SFARSIT'), ('VALOARE_POLITA', 'VALOARE POLITA')]

class CriteriuAsiguratori(forms.Form):

    criteriu = forms.CharField(label='SORTEAZA DUPA ', widget=forms.Select(choices=CriteriiAsiguratori),  required=False, initial='ID_ASIGURATOR')
    ord = forms.CharField(label = '', widget=forms.Select(choices=asc_desc),  required=False, initial='ASC')
    
class CriteriuSoferi(forms.Form):

    criteriu = forms.CharField(label='SORTEAZA DUPA ', widget=forms.Select(choices=CriteriiSoferi),  required=False, initial='ID_SOFER')
    ord = forms.CharField(label = '', widget=forms.Select(choices=asc_desc),  required=False, initial='ASC')

class CriteriuMasini(forms.Form):

    criteriu = forms.CharField(label='SORTEAZA DUPA ', widget=forms.Select(choices=CriteriiMasini),  required=False, initial='ID_MASINA')
    ord = forms.CharField(label = '', widget=forms.Select(choices=asc_desc),  required=False, initial='ASC')

class CriteriuOrase(forms.Form):

    criteriu = forms.CharField(label='SORTEAZA DUPA ', widget=forms.Select(choices=CriteriiOrase),  required=False, initial='ID_ORAS')
    ord = forms.CharField(label = '', widget=forms.Select(choices=asc_desc),  required=False, initial='ASC')

class CriteriuGaraje(forms.Form):

    criteriu = forms.CharField(label='SORTEAZA DUPA ', widget=forms.Select(choices=CriteriiGaraje),  required=False, initial='ID_GARAJ')
    ord = forms.CharField(label = '', widget=forms.Select(choices=asc_desc),  required=False, initial='ASC')

class CriteriuProducatori(forms.Form):

    criteriu = forms.CharField(label='SORTEAZA DUPA ', widget=forms.Select(choices=CriteriiProducatori),  required=False, initial='ID_PRODUCATOR')
    ord = forms.CharField(label = '', widget=forms.Select(choices=asc_desc),  required=False, initial='ASC')

class CriteriuModele(forms.Form):

    criteriu = forms.CharField(label='SORTEAZA DUPA ', widget=forms.Select(choices=CriteriiModele),  required=False, initial='ID_MODEL')
    ord = forms.CharField(label = '', widget=forms.Select(choices=asc_desc),  required=False, initial='ASC')

class CriteriuConduce(forms.Form):

    criteriu = forms.CharField(label='SORTEAZA DUPA ', widget=forms.Select(choices=CriteriiConduce),  required=False, initial='ID_MASINA')
    ord = forms.CharField(label = '', widget=forms.Select(choices=asc_desc),  required=False, initial='ASC')

class CriteriuAsigura(forms.Form):

    criteriu = forms.CharField(label='SORTEAZA DUPA ', widget=forms.Select(choices=CriteriiAsigura),  required=False, initial='ID_MASINA')
    ord = forms.CharField(label = '', widget=forms.Select(choices=asc_desc),  required=False, initial='ASC')

class VerifAsigForm(forms.Form):

    nr_inmatriculare = forms.CharField(max_length=7, label = 'NR INMATRICULARE', required=True)

class NrSoferi(forms.Form):

    min = forms.IntegerField(label = '', required=False)
    max = forms.IntegerField(label = '', required=False)
