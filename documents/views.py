from django.shortcuts import render, redirect, get_object_or_404
from .models import Document, Processing, ExtractedData, Risk
from .hubspot_integration import send_document_to_hubspot


def login_view(request):
    return render(request, 'login.html')


def dashboard(request):
    documents = Document.objects.all().order_by('-uploaded_at')

    return render(request, 'dashboard.html', {
        'documents': documents
    })


def upload_document(request):
    if request.method == 'POST':
        file = request.FILES.get('file')

        if file:
            # создаем документ
            document = Document.objects.create(
                file=file,
                file_name=file.name,
                status='processing'
            )

            # создаем процесс обработки
            processing = Processing.objects.create(
                document=document,
                status='processing'
            )

            # 🔥 FAKE AI (временно)
            fake_data = {
                "address": "Москва, ул. Ленина 1",
                "cadastral_number": "77:01:0004012:3456",
                "area": "120 м²",
                "owner": "Иван Иванов",
                "type": "Жилой",
                "ownership_type": "Физическое лицо",
                "price": "3 500 000 руб"
            }

            # сохраняем результат анализа
            ExtractedData.objects.create(
                document=document,
                data=fake_data,
                raw_text="Пример распознанного текста...",
                confidence_score=0.92
            )

            # создаем риски
            Risk.objects.create(
                document=document,
                type="legal",
                description="Отсутствует подтверждение собственности",
                severity="high"
            )

            Risk.objects.create(
                document=document,
                type="cadastral",
                description="Неполные кадастровые данные",
                severity="medium"
            )

            # обновляем статус
            document.status = "done"
            document.save()

            processing.status = "done"
            processing.save()
            
            send_document_to_hubspot(document)

            return redirect(f'/document/{document.id}/')

    return render(request, 'upload.html')


def document_detail(request, doc_id):
    document = get_object_or_404(Document, id=doc_id)

    # получаем извлеченные данные
    extracted = getattr(document, 'extracted_data_record', None)

    # получаем риски
    risks = document.risks.all()

    return render(request, 'document_detail.html', {
        'doc': document,
        'data': extracted.data if extracted else {},
        'risks': risks
    })