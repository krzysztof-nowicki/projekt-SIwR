# Sztuczna Inteligencja w Robotyce - Projekt
# Koncepcja:
Propabilistyka między dwoma zdjęciami obliczane jest na podstawie 3 czynników, Każdy czynnik posiada swoją wagę w zależności od stopnia możliwych zmian i trafności. <br />
-Wielkość BoundingBox <br /> (Waga 0.4 - Brak dużych zmian o ile cel nie zbliża się lub nie oddala od kamery) <br />
-Odległość między BoundingBoxem na jednym i drugim zdjęciu <br /> (Waga 0.1 - Możliwe duże oddalenia między celami na dwóch różnych zdjęciach) <br />
-Średnia kolorów w centrum BoundingBoxa  <br /> (Waga 0.5 - Oświetlenie może wpływać na jakość, jednak najmniej podatny na zmiany czynnik) <br />
Do przypisania indeksu z poprzedniego zdjęcia wykorzystany został graf czynników
