# Sztuczna Inteligencja w Robotyce - Projekt
# Koncepcja:
Propabilistyka między dwoma zdjęciami obliczane jesst na podstawie 3 czynników, Każdy czynnik posiada swoją wagę w zależności od stopnia możliwych zmian i trafności. <br />
-Wielkość BoundingBox (Waga 0.4 - Brak dużych zmian o ile cel nie zbliża się lub nie oddala od kamery) <br />
-Odległość między BoundingBoxem na jednym i drugim zdjęciu (Waga 0.1 - Możliwe duże oddalenia między celami na dwóch różnych zdjęciach) <br />
-Średnia kolorów w centrum BoundingBoxa (Waga 0.5 - Oświetlenie może wpływać na jakość, jednak najmniej podatny na zmiany czynnik) <br />

# Wnioskowanie:
Proste wnioskowanie sprawdzające procent znalezienia znanych wcześniej osób na poprzednim zdjęciu. Wpływa na granicę propabilistyki od której osoba może zostać uznana za występującą wcześniej na planie. 

