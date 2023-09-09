from pathlib import Path
import shutil
import sys, re


TRANSLIT_DICT = {
    ord("а"): "a", ord("б"): "b", ord("в"): "v", ord("г"): "g", ord("д"): "d", ord("е"): "e", ord("є"): "ie", ord("ж"): "zh", ord("з"): "z",
    ord("и"): "i", ord("і"): "i", ord("ї"): "ji", ord("й"): "j", ord("к"): "k", ord("л"): "l", ord("м"): "m", ord("н"): "n", ord("о"): "o",
    ord("п"): "p", ord("р"): "r", ord("с"): "s", ord("т"): "t", ord("у"): "u", ord("ф"): "f", ord("х"): "h", ord("ц"): "c", ord("ч"): "ch",
    ord("ш"): "sh", ord("щ"): "shch", ord("ь"): " ", ord("ю"): "ju", ord("я"): "ja",
    ord("А"): "A", ord("Б"): "B", ord("В"): "V", ord("Г"): "G", ord("Д"): "D", ord("Е"): "E", ord("Є"): "Ye", ord("Ж"): "Zh", ord("З"): "Z",
    ord("И"): "I", ord("І"): "I", ord("Ї"): "Ji", ord("Й"): "J", ord("К"): "K", ord("Л"): "L", ord("М"): "M", ord("Н"): "N", ord("О"): "O",
    ord("П"): "P", ord("Р"): "R", ord("С"): "S", ord("Т"): "T", ord("У"): "U", ord("Ф"): "F", ord("Х"): "H", ord("Ц"): "C", ord("Ч"): "Ch",
    ord("Ш"): "Sh", ord("Щ"): "Shch", ord("Ь"): " ", ord("Ю"): "Ju", ord("Я"): "Ja"
}  

usi_rozsh  = { 'documents' : ['.DOC', '.DOCX', '.TXT', '.PDF', '.XLSX', '.PPTX'], 
'images' : ['.JPEG', '.PNG', '.JPG', '.SVG', '.BMP'], 
'audio' : ['.MP3', '.OGG', '.WAV', '.AMR'],
'video' : ['.AVI', '.MP4', '.MOV', '.MKV'],
'archives' : ['.ZIP', '.GZ', '.TAR'] 
}

cpf = {} # count peremishchenna fajliv 
def dz6():
    try:
        shlah_do_papki = Path(sys.argv[1])
    except IndexError:
        print("Не введено шляху")
        return  
    if not shlah_do_papki.exists():
        print ("Шляху до папки не існує")
        return 
    else:



        def normalize(obj:Path): 
            lat_obj = obj.stem.translate(TRANSLIT_DICT)
            lat_obj = ''.join(char if char.isalnum() else '_' for char in lat_obj) + obj.suffix
            return lat_obj
    

        def sortirovka(obj:Path):  
            for ima_papky, rozsh in usi_rozsh.items():
                if obj.suffix.upper() in rozsh:
                    return ima_papky
            return "others"


        def peremishch_file(obj:Path, shlah_do_papki:Path, nova_papka:str):
            global cpf
            cilova_papka = Path(shlah_do_papki).joinpath(nova_papka) 

            if not cilova_papka.exists():
                cilova_papka.mkdir()  
                cpf[nova_papka] = 1
            
            normalize_z = normalize(obj)
            put1 = cilova_papka.joinpath(normalize_z)
            put2 = cilova_papka.joinpath(str(cpf.get(nova_papka)) + normalize_z)
            
            if not put1.exists():
                shutil.move(obj, put1)

                if cilova_papka.name == "archives":
                    shutil.unpack_archive(put1,put1.with_suffix(''))
                    put1.unlink()               
            else:
                
                shutil.move(obj, put2)

                if cilova_papka.name == "archives":
                    shutil.unpack_archive(put2,put2.with_suffix(''))
                    put2.unlink() 
                cpf[nova_papka] += 1     

            return


        
        
        usi_objekty = Path(shlah_do_papki).rglob("**/*")

        for obj in usi_objekty:
            
            if obj.is_file() and 'archives' not in str(obj):    
                if str(obj.parent.name) not in usi_rozsh and obj.parent.name != "others":     
                                           
                    nova_papka = sortirovka(obj)   
                    peremishch_file(obj, shlah_do_papki, nova_papka)              

        for obj in Path(shlah_do_papki).glob('*'):
            if obj.name not in usi_rozsh and obj.name != "others":
                shutil.rmtree(obj)

        print ("Готово")
        return 
    


if __name__ == "__main__":
 
    
    dz6()







