const btn = document.getElementById('flashcard-btn')
const container = document.getElementById('flashcard-container')
let currentCard = 0;
const flashcardContainer = document.getElementById('flashcard-container');
const prevButton = document.getElementById('prev');
const nextButton = document.getElementById('next');

async function loadFlashcards() {
    const response = await fetch('/generate-flashcards');
    const flashcards = await response.json();
    
    displayFlashcard();

    function displayFlashcard() {
        flashcardContainer.querySelector('.front').textContent = flashcards[currentCard].front;
        flashcardContainer.querySelector('.back').textContent = flashcards[currentCard].back;
    }

    flashcardContainer.addEventListener('click', () => {
        flashcardContainer.querySelector('.flashcard-content').classList.toggle('flip');
    });

    prevButton.addEventListener('click', () => {
        if (currentCard > 0) {
            currentCard--;
            displayFlashcard();
            flashcardContainer.querySelector('.flashcard-content').classList.remove('flip');
        }
    });

    nextButton.addEventListener('click', () => {
        if (currentCard < flashcards.length - 1) {
            currentCard++;
            displayFlashcard();
            flashcardContainer.querySelector('.flashcard-content').classList.remove('flip');
        }
    });
}

btn.addEventListener('click', async () => {
    const response = await fetch('/generate-flashcards')
    const response_json = await response.json()

    for (let obj of response_json) {
    }
})