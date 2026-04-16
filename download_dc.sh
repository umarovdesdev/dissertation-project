#!/bin/bash
# Download dissertation council files from IITU website

BASE="E:/dissertation_council"
BAKIROVA="$BASE/Образцы документов/авторы/Бакирова Г.С."

mkdir -p "$BAKIROVA"

echo "=== Downloading Bakirova G.S. files ==="

curl -kL "https://iitu.edu.kz/documents/4359/Defense_Announcement.pdf" -o "$BAKIROVA/Defense_Announcement.pdf" && echo "1/9 done"
curl -kL "https://iitu.edu.kz/documents/4360/Abstract_in_Kazakh.pdf" -o "$BAKIROVA/Abstract_in_Kazakh.pdf" && echo "2/9 done"
curl -kL "https://iitu.edu.kz/documents/4361/Abstract_in_Russian.pdf" -o "$BAKIROVA/Abstract_in_Russian.pdf" && echo "3/9 done"
curl -kL "https://iitu.edu.kz/documents/4362/Abstract_in_English.pdf" -o "$BAKIROVA/Abstract_in_English.pdf" && echo "4/9 done"
curl -kL "https://iitu.edu.kz/documents/4363/Dissertation.pdf" -o "$BAKIROVA/Dissertation.pdf" && echo "5/9 done"
curl -kL "https://iitu.edu.kz/documents/4364/List_of_scientific_papers.pdf" -o "$BAKIROVA/List_of_scientific_papers.pdf" && echo "6/9 done"
curl -kL "https://iitu.edu.kz/documents/4365/Review_of_the_scientific_consultant.pdf" -o "$BAKIROVA/Review_of_the_scientific_consultant.pdf" && echo "7/9 done"
curl -kL "https://iitu.edu.kz/documents/4368/%D0%9E%D1%82%D0%B7%D1%8B%D0%B2_%D0%B7%D0%B0%D1%80%D1%83%D0%B1%D0%B5%D0%B6%D0%BD%D0%BE%D0%B3%D0%BE_%D0%BA%D0%BE%D0%BD%D1%81%D1%83%D0%BB%D1%8C%D1%82%D0%B0%D0%BD%D1%82%D0%B0_%D0%BD%D0%BE%D0%B2%D1%8B%D0%B9.pdf" -o "$BAKIROVA/Отзыв_зарубежного_консультанта_новый.pdf" && echo "8/9 done"
curl -kL "https://iitu.edu.kz/documents/4367/Conclusion_of_the_Ethnic_Commission.pdf" -o "$BAKIROVA/Conclusion_of_the_Ethnic_Commission.pdf" && echo "9/9 done"

echo ""
echo "=== Verifying downloads ==="
ls -la "$BAKIROVA/"
echo ""
echo "=== Summary ==="
ls -la "$BASE/"
ls -la "$BASE/Нормативные документы/"
