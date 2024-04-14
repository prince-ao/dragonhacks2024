document.addEventListener('DOMContentLoaded', function() {
    const btn = document.getElementById('flashcard-btn');
    const flashcardContainer = document.getElementById('flashcard-container');
    const prevButton = document.getElementById('prev');
    const nextButton = document.getElementById('next');
    const front = document.getElementById('front');
    const back = document.getElementById('back');

    let currentCard = 0;
    let flashcards = [];

    async function loadFlashcards() {
        const summary = document.getElementById('summary').textContent;

        const response = await fetch('/generate-flashcards', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ summary: summary })
        });

        flashcards = await response.json();
        displayFlashcard();
    }

    function displayFlashcard() {
        if (flashcards.length > 0) {
            back.textContent = flashcards[currentCard]['front'];
            flashcardContainer.classList.remove('hidden');
        }
    }

    flashcardContainer.addEventListener('click', () => {
        flashcardContainer.querySelector('.flip-card-inner').classList.toggle('flip');
    });

    prevButton.addEventListener('click', () => {
        if (currentCard > 0) {
            currentCard--;
            displayFlashcard();
            flashcardContainer.querySelector('.flip-card-inner').classList.remove('flip');
        }
    });

    nextButton.addEventListener('click', () => {
        if (currentCard < flashcards.length - 1) {
            currentCard++;
            displayFlashcard();
            flashcardContainer.querySelector('.flip-card-inner').classList.remove('flip');
        }
    });

    btn.addEventListener('click', async () => {
        await loadFlashcards();

        back.addEventListener('click', async () => {
            if (back.textContent === flashcards[currentCard]['back']) {
                back.textContent = flashcards[currentCard]['front']
            } else {
                back.textContent = flashcards[currentCard]['back']
            }
        });
    });
});