// static/js/scripts.js

let deleteHandlerAdded = false;

function initDeleteHandlers() {
    if (deleteHandlerAdded) return;

    const deleteButtons = document.querySelectorAll('.delete-btn');

    deleteButtons.forEach(button => {
        // Спочатку видалимо всі старі обробники
        button.replaceWith(button.cloneNode(true));
    });

    // Додамо нові обробники до "свіжих" кнопок
    document.querySelectorAll('.delete-btn').forEach(button => {
        button.addEventListener('click', function(event) {
            const confirmation = confirm('Ви впевнені, що хочете видалити цей пост? Цю дію неможливо скасувати.');

            if (!confirmation) {
                event.preventDefault();
            }
        });
    });

    deleteHandlerAdded = true;
}

document.addEventListener('DOMContentLoaded', initDeleteHandlers);