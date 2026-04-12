# EstateScan AI

Веб-приложение для анализа документов недвижимости с использованием AI.

## 🚀 Функционал
- Загрузка документов (PDF, JPG, PNG)
- Автоматический анализ документа (MVP)
- Извлечение ключевых данных:
  - адрес
  - площадь
  - владелец
  - кадастровый номер
- Отображение рисков
- Dashboard с документами

## 🛠️ Технологии
- Python / Django
- SQLite
- TailwindCSS

## 📦 Запуск проекта

```bash
git clone https://github.com/fongan228/RealEstate.git
cd RealEstate

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

python manage.py migrate
python manage.py runserver