
class MapDatabaseRouter:
    """
    Маршрутизатор для перенаправления всех запросов к моделям вашего приложения
    в базу данных 'map'.
    """
    def db_for_read(self, model, **hints):
        """
        Возвращает 'map' для всех чтений моделей вашего приложения.
        """
        if model._meta.app_label == 'map':
            return 'map'
        return None

    def db_for_write(self, model, **hints):
        """
        Возвращает 'custom' для всех записей моделей вашего приложения.
        """
        if model._meta.app_label == 'map':
            return 'map'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Разрешает отношения между объектами разных баз данных, если оба объекта
        относятся к вашему приложению.
        """
        if obj1._meta.app_label == 'map' and obj2._meta.app_label == 'map':
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Разрешает миграции для моделей вашего приложения только в базе данных 'map'.
        """
        if app_label == 'map':
            return db == 'map'
        return None
