# Bio

## Uruchomienie
./bio.py <words_file> <matrix_file>

words_file - plik z 2 dowolnymi sekwencjami odzielonymi znakiem nowej linii
matrix_file - macierz podobienstwa dla alfabetu zawartego w sekwencjach - musi być kwadratowa i zawierać wszystkie litery z sekwencji

## Examples
./bio.py words1.txt matrix1.txt ACTA:TGTT - zadanie NW z kol1
./bio.py words3.txt matrix3.txt writers:vinter - NW ze slajdów (podobienstwo zamiast odeglosci edycyjnej)
./bio.py words4.txt matrix4.txt TGAATTT:AACTTAC - Smith ze slajdów
./bio.py words5.txt matrix5.txt TCAT:CCGC - zadanie NW z kol2