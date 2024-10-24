document.addEventListener('DOMContentLoaded', function() {
    // Получаем элементы полей
    const priceTypeField = document.getElementById('id_price_type');
    const thicknessField = document.querySelector('.form-row.field-thickness');
    const materialsField = document.querySelector('.form-row.field-materials');

    // Функция для отображения/скрытия полей
    function toggleFields() {
        if (priceTypeField.value === 'PRICE_MATERIAL') {
            thicknessField.style.display = '';
            materialsField.style.display = '';
        } else {
            thicknessField.style.display = 'none';
            materialsField.style.display = 'none';
        }
    }

    // Вызываем функцию при загрузке страницы
    toggleFields();

    // Добавляем обработчик события изменения
    priceTypeField.addEventListener('change', toggleFields);
});
