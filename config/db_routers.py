class CustomRouter:
    def db_for_read(self, model, **hints):
        """Определяет базу данных для чтения данных модели."""
        if model._meta.app_label == 'custom':
            return 'custom'
        if model._meta.app_label == 'store':
            return 'store'
        return 'default'

    def db_for_write(self, model, **hints):
        """Определяет базу данных для записи данных модели."""
        if model._meta.app_label == 'custom':
            return 'custom'
        if model._meta.app_label == 'store':
            return 'store'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """Разрешает отношения между объектами."""
        db_set = {'custom', 'store', 'default'}
        if obj1._state.db in db_set and obj2._state.db in db_set:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Разрешает миграции только для нужных баз данных."""
        if app_label == 'custom':
            return db == 'custom'
        if app_label == 'store':
            return db == 'store'
        return db == 'default'
