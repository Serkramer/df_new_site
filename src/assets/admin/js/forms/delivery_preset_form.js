document.addEventListener("DOMContentLoaded", function() {
    // Получаем ссылки на поля 'delivery_type' и 'post_office_ref'
    const deliveryTypeField = document.getElementById('id_delivery_type');
    const postOfficeField = document.getElementById('id_post_office_ref');
    const deliverTypeSelector = document.getElementById('id_delivery_type_selector')

    // Функция для скрытия или показа поля post_office_ref
    function togglePostOfficeField() {
        const selectedDeliveryType = deliveryTypeField.value;

        // Показываем или скрываем поле post_office_ref в зависимости от значения delivery_type
        if (selectedDeliveryType === '3') {  // Замените 'desired_delivery_type' на значение типа, при котором поле должно быть показано
            postOfficeField.closest('.form-row').style.display = 'block'; // Показываем поле
            deliverTypeSelector.closest('.form-row').style.display = 'block'; // Показываем поле
        } else {
            postOfficeField.closest('.form-row').style.display = 'none'; // Скрываем поле
            deliverTypeSelector.closest('.form-row').style.display = 'none'; // Скрываем поле
        }
    }

    // Добавляем обработчик события изменения значения в поле 'delivery_type'
    deliveryTypeField.addEventListener('change', togglePostOfficeField);

    // Начальная проверка, чтобы сразу установить правильную видимость при загрузке страницы
    togglePostOfficeField();
});
