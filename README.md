# POIR.01.01.01-00-0972/20 - System automatycznego audytu ekspozycji wykorzystujący technologię rozpoznawania obrazu do detekcji i analizy produktów

## Informacje o projekcie

Repozytorium zawiera paczkę kodu źródłowego wytworzoną w ramach projektu **POIR.01.01.01-00-0972/20** pt. **„System automatycznego audytu ekspozycji wykorzystujący technologię rozpoznawania obrazu do detekcji i analizy produktów”**.

Projekt dotyczył opracowania systemu wspierającego automatyczny audyt regałów sklepowych przez:
- akwizycję materiału obrazowego z wykorzystaniem dedykowanego urządzenia,
- automatyczną detekcję produktów i etykiet cenowych,
- analizę zgodności ekspozycji z planogramem,
- odczyt informacji z etykiet oraz generowanie raportów dla procesów audytowych.

Zgodnie z dokumentacją końcową projekt obejmował zarówno komponenty algorytmiczne, jak i warstwę sprzętową, aplikacyjną oraz integracyjną. Efektem prac było rozwiązanie działające jako wielokomponentowy system: od pozyskania obrazu, przez przetwarzanie AI/OCR, po prezentację oraz raportowanie wyników.

## Charakter paczki źródłowej

Paczkę należy traktować jako **repozytorium wielomodułowe (multi-service / monorepo)**, w którym poszczególne katalogi odpowiadają za odrębne elementy architektury systemu. W kodzie widoczne są głównie następujące warstwy:

- **akwizycja obrazu** z kamer i urządzeń brzegowych,
- **serwisy AI** do analizy zdjęć regałów i generowania raportów planogramowych,
- **OCR i przetwarzanie etykiet cenowych**, 
- **backend domenowy** do zarządzania sklepami, planogramami, raportami i wynikami analiz,
- **backend administracyjny** do zarządzania katalogiem SKU, treningami i danymi referencyjnymi,
- **frontend webowy** do przeglądania raportów i obsługi procesu audytu,
- **biblioteki pomocnicze** do augmentacji danych i narzędzi computer vision.

## Struktura katalogów

### `planogram-camera-service/`
Mikroserwis w Pythonie/Flask odpowiedzialny za **pozyskiwanie pojedynczych klatek z kamer IP** i ich udostępnianie w postaci PNG przez API HTTP.

Zakres techniczny:
- obsługa kamer różnych producentów, w szczególności **Dahua** oraz **Hikvision**, 
- połączenia z użyciem **HTTP Digest Auth**, **HTTP Basic Auth** oraz **RTSP**,
- enkodowanie przechwyconych klatek do formatu PNG,
- wystawienie endpointu `/image/<cam_ip>/<cam_type>`,
- skrypty diagnostyczne do sprawdzania dostępności kamer i urządzeń sieciowych.

Rola w systemie:
- warstwa integracyjna między urządzeniem/kamerą a dalszym pipeline'em analizy obrazu,
- ujednolicone wejście obrazowe dla dalszych usług AI.

### `planogram-ai-service/`
Mikroserwis AI w Pythonie/Flask udostępniający **API analizy obrazów regałów i generowania raportów planogramowych**.

Zakres techniczny:
- endpointy walidujące poprawność zdjęć do analizy,
- endpoint do **anonimizacji wizerunków** (`remove-faces-from-photo`),
- endpoint `generate-planogram-report` zwracający strukturę detekcji zawierającą m.in.:
  - współrzędne bboxów,
  - pozycję produktu na półce,
  - indeks SKU,
  - metrykę trafności,
- implementacja usług uruchamianych w środowisku kontenerowym,
- zależności związane z **PyTorch**, **OpenCV**, **TensorFlow/Keras** oraz dodatkowymi bibliotekami do inferencji.

Rola w systemie:
- centralny komponent inferencyjny dla audytu ekspozycji,
- ekstrakcja wyników potrzebnych do porównania zdjęcia z planogramem i budowy raportu.

### `ocr/`
Moduł OCR odpowiedzialny za **odczyt tekstu z etykiet cenowych i przygotowanie pipeline'u treningowego dla rozpoznawania znaków**.

Zakres techniczny:
- generowanie oraz augmentacja danych OCR,
- skrypty budowy datasetów i przygotowania danych treningowych,
- moduły treningowe (`train.py`, `test.py`, `build_dataset.py`),
- komponenty detekcji obszarów tekstowych i analizy boksów,
- skanowanie, parsowanie i przetwarzanie obrazów etykiet,
- integracja z bibliotekami do OCR i dekodowania danych pomocniczych (m.in. barcode).

Rola w systemie:
- rozpoznawanie treści etykiet cenowych,
- przygotowanie wejścia do logiki wiążącej etykiety z produktami na półce.

### `z-analyzer/`
Backend analityczny oparty o **Symfony / PHP**, realizujący logikę domenową związaną z **audytem sklepów, planogramami, zdjęciami i raportami analizy**.

Zakres techniczny:
- encje domenowe takie jak m.in. `Shop`, `Planogram`, `PlanogramElement`, `Sku`, `Photo`, `ReportPhotoAnalysis`, `Camera`,
- kontrolery API obsługujące audyty, sklepy i proces raportowy,
- repozytoria i usługi odpowiedzialne za import danych, mapowanie SKU, kalkulację accuracy oraz integrację z usługami zewnętrznymi,
- mechanizmy autoryzacji oparte o OAuth/FOS,
- migracje bazy danych oraz warstwa persistence.

Rola w systemie:
- backend operacyjny spinający dane sklepów, zdjęć, planogramów oraz wyników AI,
- warstwa odpowiedzialna za utrzymywanie i udostępnianie wyników analizy do frontendów i procesów audytowych.

### `z-dashboard/`
Frontend webowy oparty o **Angular**, przeznaczony do **prezentacji raportów audytowych i nawigacji po strukturze sklep -> typ raportu -> wynik analizy**.

Zakres techniczny:
- routing modułowy dla logowania, list sklepów, raportów i ekranów wyników,
- komponenty prezentujące dane sklepu, listy raportów, szczegóły wyniku oraz dane audytowe,
- warstwa UI oparta m.in. o **Angular 8**, **Nebular** i **Bootstrap**,
- przygotowanie do komunikacji z backendem analitycznym.

Rola w systemie:
- wizualizacja rezultatów przetwarzania,
- interfejs użytkownika dla audytora lub operatora analizującego wyniki systemu.

### `sku-manager/`
Backend administracyjny oparty o **Symfony / PHP**, służący do **zarządzania słownikami produktowymi, klasami produktów, grupami produktów, treningami i obrazami referencyjnymi**.

Zakres techniczny:
- encje domenowe takie jak `Product`, `ProductGroup`, `ProductClass`, `Brand`, `Image`, `Training`, `Category`,
- REST API do operacji CRUD na danych referencyjnych,
- walidacja biznesowa i obsługa zdarzeń domenowych,
- komponenty bezpieczeństwa oparte o JWT,
- testy jednostkowe dla warstwy managerów i walidatorów.

Rola w systemie:
- utrzymywanie katalogu referencyjnego SKU i metadanych potrzebnych do trenowania lub parametryzacji modeli,
- zaplecze administracyjne dla warstwy AI i procesów konfiguracji systemu.

### `shelf-retail/`
Moduł badawczo-rozwojowy w Pythonie związany z **detekcją obiektów na półkach sklepowych**.

Zakres techniczny:
- implementacje i konfiguracje modeli detekcyjnych bazujących na ekosystemie **MMDetection / PyTorch**,
- lokalne narzędzia do testów detektorów, pracy z kamerami oraz importu planogramów,
- struktura wskazująca na wykorzystanie eksperymentalnych modeli do analizy półek i danych retailowych,
- zależności obejmujące m.in. `mmcv`, `pycocotools`, `torch`, `torchvision`, `tensorflow-gpu`, `keras`.

Rola w systemie:
- warstwa eksperymentalna i modelowa dla detekcji produktów/elementów ekspozycji,
- zaplecze R&D wspierające rozwój algorytmów używanych później przez serwis AI.

### `vision-tools/`
Wspólna biblioteka narzędzi computer vision i ML wspierająca **trening, ewaluację, deploy oraz przetwarzanie danych obrazowych**.

Zakres techniczny:
- narzędzia treningowe dla Keras/TensorFlow,
- moduły do obsługi konfiguracji, monitoringu zasobów, preprocessingu i metryk,
- pomocnicze komponenty dla OCR (`aocr`), deployu procesów oraz pracy z datasetami,
- zestaw helperów do pracy z obrazami, bboxami, EXIF, LMDB i plikami.

Rola w systemie:
- warstwa współdzielona między eksperymentami i usługami produkcyjnymi,
- repozytorium utility code dla zespołu rozwijającego algorytmy wizyjne.

### `aug/`
Biblioteka augmentacji obrazów wykorzystywana do **syntetycznego zwiększania różnorodności danych treningowych**.

Zakres techniczny:
- pipeline'y operacji augmentacyjnych,
- transformacje geometryczne, fotometryczne, perspektywiczne, blur, blending, distortions,
- przykłady użycia oraz materiały demonstracyjne.

Rola w systemie:
- poprawa generalizacji modeli trenowanych na ograniczonych zbiorach danych,
- wsparcie scenariuszy few-shot oraz przygotowania danych dla modeli CV/OCR.

## Uwagi architektoniczne

Na podstawie struktury paczki kodu można stwierdzić, że rozwiązanie zostało zbudowane jako **system rozproszony**, w którym:
- komponenty Pythonowe realizują akwizycję obrazu, inferencję AI, OCR i eksperymenty modelowe,
- komponenty PHP/Symfony realizują logikę biznesową, zarządzanie danymi domenowymi i ekspozycję API,
- komponent Angular realizuje warstwę prezentacji wyników,
- część katalogów pełni funkcję stricte **produkcyjną**, a część stanowi **zaplecze badawczo-treningowe** powstałe podczas prac B+R.

## Zgodność z zakresem projektu

Struktura repozytorium jest spójna z celami projektu badawczo-rozwojowego, tj. z opracowaniem:
- metod pozyskiwania materiału obrazowego regałów,
- metod detekcji produktów i etykiet,
- metod rozpoznawania informacji z etykiet cenowych,
- mechanizmu analizy zgodności ekspozycji z planogramem,
- zaplecza raportowego i aplikacyjnego dla użytkowników końcowych.

## Status repozytorium

Niniejsza paczka stanowi archiwum kodu źródłowego wytworzonego w toku realizacji projektu B+R. Ze względu na jej projektowy charakter poszczególne moduły mogą reprezentować różny poziom dojrzałości: od bibliotek eksperymentalnych i narzędzi treningowych po usługi aplikacyjne gotowe do integracji środowiskowej.
