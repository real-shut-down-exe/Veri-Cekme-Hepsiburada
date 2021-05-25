import tqdm
from bs4 import BeautifulSoup
import requests
import pandas as pd
from tqdm import tqdm

print("""
                _             _                   
               (_)           | |                  
__   _____ _ __ _     ___ ___| | ___ __ ___   ___ 
\ \ / / _ \ '__| |   / __/ _ \ |/ / '_ ` _ \ / _ /
 \ V /  __/ |  | |   |(_|  __/   <| | | | | |  __/
  \_/ \___|_|  |_|   \___\___|_|\_\_| |_| |_|\___|
__________________________________________________
""")

sayfa_linki = input("Sayfa Linki : ")
ilk_kac_sayfa = input("İlk kaç sayfa alınsın? (sayı ile yazınız) : ")
exel_tablo_adi = input("Exel tablo adı ne olsun : ")

liste = []
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36'}
sayfa_ = "?sayfa="
a = 1
print("")

while a <= int(ilk_kac_sayfa):

    #print("\n")
    print("#" * 13 + " " + str(a) + " Sayfa " + "#" * 13)

    r = requests.get(sayfa_linki + sayfa_ + str(a) + "", headers=headers)
    soup = BeautifulSoup(r.content, "lxml")

    st1 = soup.find("div", attrs={"class": "contain-lg-3 contain-md-3 contain-sm-3 fluid with-bottom-border"})
    st2 = st1.find("ul", attrs={"data-bind": "css: {grid: isGridSelected, list: isListSelected}"})
    st3 = st2.find_all("li", attrs={"data-index": "1"})

    x = 1

    bar = tqdm(st3)

    for detaylar in bar:
        bar.set_description("Veri Çekiliyor ")
        link_sonu = detaylar.a.get("href")
        link_bası = "https://www.hepsiburada.com"
        link = link_bası + link_sonu

        #print("\n" + "_" * 9 + " " + str(a) + ".Sayfanın / " + str(x) + ".Ürünü " + "_" * 9)
        #print("\nKategori Linki: " + link)

        r1 = requests.get(link, headers=headers)
        soup1 = BeautifulSoup(r1.content, "lxml")

        x = x + 1

        yeni_fiyat = soup1.find("span", attrs={"itemprop": "price"}).text.strip().replace("\n", "")
        #print("Yeni Fiyatı: " + yeni_fiyat)

        orjinal_fiyat = soup1.find("del", attrs={"id": "originalPrice"}).text
        #print("Orjınal Fiyatı: " + orjinal_fiyat)

        ürün_adı = soup1.find("h1", attrs={"itemprop": "name"}).text.strip()
        #print("Ürünün Adı: " + ürün_adı)

        marka = soup1.find("span", attrs={"class": "brand-name"}).text.strip()
        #print("Markası: " + marka)

        soup_img = BeautifulSoup(r1.content, 'html.parser')
        picture_elems = soup_img.find_all('picture')
        resim_listesi = []
        resim_no = 1

        for idx, picture_elem in enumerate(picture_elems):

            if (idx == 0):  # listedeki ilk elemanı ayrıca al çünkü diğerleri owl-lazy class ına sahip
                source_elem = picture_elem.find('source', class_="product-image")
                imgurl = source_elem['srcset'].replace("/format:webp 1x", "")
                #print(str(resim_no) + ".Resim " + imgurl)
                resim_no = resim_no + 1
                resim_listesi.append(imgurl)
                continue;

            if (picture_elem.find('source', class_="owl-lazy")):  # owl-lazy class ına sahip olan diğerlerini de al
                source_elem = picture_elem.find('source', class_="product-image")
                imgurl = source_elem['data-srcset'].replace("/format:webp 1x", "").replace("/format:webp 2x", "")

                #print(str(resim_no) + ".Resim " + imgurl)
                resim_listesi.append(imgurl)

            resim_no = resim_no + 1

        #print("")
        teknik_ayrıntılar = soup1.find_all("table", attrs={"class": "data-list tech-spec"})
        ürün_özelikleri = []

        for teknik in teknik_ayrıntılar:
            detaylar = teknik.find_all("tr")
            for i in detaylar:
                etiket = i.find("th").text
                deger = i.find("td").text

                #print(etiket, "---", deger)
                üö = etiket, "---", deger
                ürün_özelikleri.append(üö)

        liste.append([ürün_adı, marka, link, yeni_fiyat, orjinal_fiyat, resim_listesi,ürün_özelikleri])


    a = a + 1

df = pd.DataFrame(liste)
df.columns = ["Ürün Adı", "Marka", "Link", "Yeni Fiyat", "Orjinal Fiyat", "Fotos","Ürün Özellikleri"]

df.to_excel(exel_tablo_adi + ".xlsx")

input("\n" + exel_tablo_adi + " isimli exel BAŞARIYLA KAYDEDİLDİ :)")

"""
Bu Script Emre Yaşar  tarafından yazılmıştır.
Yeni bir script ve iş görüşmeleri için instagram: real.shut.down.exe üzerinden ulaşabilirsiniz.
"""
