class StoreDatabaseRouter:
    """
    Маршрутизатор для перенаправления всех запросов к моделям вашего приложения
    в базу данных 'store'.
    """
    def db_for_read(self, model, **hints):
        """
        Возвращает 'store' для всех чтений моделей вашего приложения.
        """
        if model._meta.app_label == 'store':
            return 'store'
        return None

    def db_for_write(self, model, **hints):
        """
        Возвращает 'store' для всех записей моделей вашего приложения.
        """
        if model._meta.app_label == 'store':
            return 'store'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Разрешает отношения между объектами разных баз данных, если оба объекта
        относятся к вашему приложению.
        """
        if obj1._meta.app_label == 'store' and obj2._meta.app_label == 'store':
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Разрешает миграции для моделей вашего приложения только в базе данных 'store'.
        """
        if app_label == 'store':
            return db == 'store'
        return None
