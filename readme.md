## Uruchomienie
python ./bio.py <words_file> <matrix_file>

words_file - plik z 2 dowolnymi sekwencjami odzielonymi znakiem nowej linii <br/>
matrix_file - macierz podobienstwa dla alfabetu zawartego w sekwencjach - musi być kwadratowa i zawierać wszystkie litery z sekwencji

## Examples
python ./bio.py words1.txt matrix1.txt || ACTA:TGTT - zadanie NW z kol1 <br/>
python ./bio.py words3.txt matrix3.txt || writers:vintner - NW ze slajdów (podobienstwo zamiast odeglosci edycyjnej) <br/>
python ./bio.py words4.txt matrix4.txt || TGAATTT:AACTTAC - Smith ze slajdów <br/>
python ./bio.py words5.txt matrix5.txt || TCAT:CCGC - zadanie NW z kol2 <br/>