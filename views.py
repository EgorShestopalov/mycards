from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Word
import random

def home(request):
    if request.method == 'POST':
        word = request.POST.get('word', '').strip()
        translation = request.POST.get('translation', '').strip()
        
        # Валидация
        if len(word) < 2:
            messages.error(request, 'Слово должно содержать минимум 2 символа')
        elif len(translation) < 2:
            messages.error(request, 'Перевод должен содержать минимум 2 символа')
        elif Word.objects.filter(word__iexact=word).exists():
            messages.error(request, f'Слово "{word}" уже существует')
        else:
            Word.objects.create(word=word, translation=translation)
            messages.success(request, f'Слово "{word}" добавлено!')
        
        return redirect('/')
    
    words = Word.objects.all().order_by('word')  # Сортировка по алфавиту
    return render(request, 'home.html', {'words': words})

def delete_word(request, id):
    word = get_object_or_404(Word, id=id)
    word.delete()
    messages.success(request, f'Слово "{word.word}" удалено')
    return redirect('/')

def quiz(request):
    if not Word.objects.exists():
        messages.error(request, 'Нет слов для квиза! Добавьте хотя бы одно слово.')
        return redirect('/')
    
    if request.method == 'POST':
        word = get_object_or_404(Word, id=request.POST['id'])
        user_answer = request.POST.get('answer', '').strip().lower()
        
        if user_answer == word.translation.lower():
            result = f"✅ Правильно! {word.word} — это {word.translation}"
        else:
            result = f"❌ Неправильно! {word.word} — это {word.translation}"
        
        # Выбираем следующее слово
        remaining_words = list(Word.objects.exclude(id=word.id))
        next_word = random.choice(remaining_words) if remaining_words else None
        
        return render(request, 'quiz.html', {'result': result, 'word': next_word})
    
    return render(request, 'quiz.html', {'word': random.choice(Word.objects.all())})