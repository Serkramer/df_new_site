# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class StoreManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().using('store')


class Articles(models.Model):
    id = models.BigAutoField(primary_key=True)
    barcode = models.ForeignKey('Barcodes', models.DO_NOTHING, blank=True, null=True)
    cell = models.ForeignKey('Cells', models.DO_NOTHING, blank=True, null=True)
    company_owner_of_material = models.ForeignKey('CompanyOwnerOfMaterialEntity', models.DO_NOTHING, blank=True,
                                                  null=True)

    class Meta:
        managed = False
        db_table = 'articles'
        verbose_name = 'Артикль'
        verbose_name_plural = 'Артиклі'

    def __str__(self):
        return f"{self.barcode.code} | {self.barcode.type}"


class Barcodes(models.Model):
    id = models.BigAutoField(primary_key=True)
    type = models.CharField(max_length=10, blank=True, null=True)
    code = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'barcodes'

    def __str__(self):
        return f"{self.code} - {self.type}"


class CellBranches(models.Model):
    id = models.BigAutoField(primary_key=True)
    settlement_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Населенний пункт")
    is_own = models.BooleanField(blank=True, null=True, verbose_name='Наш / не наш')  # This field type is a guess.
    short_name = models.CharField(max_length=10, blank=True, null=True, verbose_name="Скорочена назва")

    class Meta:
        managed = False
        db_table = 'cell_branches'
        verbose_name = 'Філія'
        verbose_name_plural = 'Філії'

    def __str__(self):
        return self.settlement_name


class Cells(models.Model):
    id = models.BigAutoField(primary_key=True)
    code = models.CharField(unique=True, max_length=25, blank=True, null=True)
    store_type = models.CharField(max_length=255, blank=True, null=True)
    barcode = models.ForeignKey(Barcodes, models.DO_NOTHING, blank=True, null=True)
    cell_branch = models.ForeignKey(CellBranches, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cells'


class CompanyOwnerOfMaterialEntity(models.Model):
    id = models.BigIntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'company_owner_of_material_entity'


class CompletedWorks(models.Model):
    id = models.BigAutoField(primary_key=True)
    assemblies_height = models.IntegerField(blank=True, null=True)
    assemblies_width = models.IntegerField(blank=True, null=True)
    is_burn_out = models.BooleanField(blank=True, null=True)  # This field type is a guess.
    forms_count = models.IntegerField(blank=True, null=True)
    materials_height = models.IntegerField(blank=True, null=True)
    materials_type = models.CharField(max_length=255, blank=True, null=True)
    materials_width = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    technology = models.CharField(max_length=255, blank=True, null=True)
    material = models.ForeignKey('Materials', models.DO_NOTHING, blank=True, null=True)
    work_shift_sheet = models.ForeignKey('WorkShiftSheets', models.DO_NOTHING, blank=True, null=True)
    article = models.ForeignKey(Articles, models.DO_NOTHING, blank=True, null=True)
    job = models.ForeignKey('Jobs', models.DO_NOTHING, blank=True, null=True)
    with_remainder = models.BooleanField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'completed_works'


class DefectMaterialSlices(models.Model):
    id = models.BigAutoField(primary_key=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    photo_file_name = models.CharField(max_length=255, blank=True, null=True)
    width = models.IntegerField(blank=True, null=True)
    defect = models.ForeignKey('Defects', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'defect_material_slices'


class DefectStatuses(models.Model):
    id = models.BigAutoField(primary_key=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'defect_statuses'


class Defects(models.Model):
    id = models.BigAutoField(primary_key=True)
    confirm = models.BooleanField(blank=True, null=True)  # This field type is a guess.
    date = models.DateTimeField(blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    defect_status = models.ForeignKey(DefectStatuses, models.DO_NOTHING, blank=True, null=True)
    material = models.ForeignKey('Materials', models.DO_NOTHING, blank=True, null=True)
    work_shift = models.ForeignKey('WorkShifts', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'defects'


class Inventories(models.Model):
    id = models.BigAutoField(primary_key=True)
    save_report_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'inventories'


class InventoryMaterialSlices(models.Model):
    status = models.CharField(max_length=255, blank=True, null=True)
    inventory = models.OneToOneField(Inventories, models.DO_NOTHING, primary_key=True)
    material_slice = models.ForeignKey('MaterialSlices', models.DO_NOTHING)
    is_confirm = models.BooleanField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'inventory_material_slices'
        unique_together = (('inventory', 'material_slice'),)


class JobSourceDefectProofs(models.Model):
    id = models.BigAutoField(primary_key=True)
    image = models.TextField(blank=True, null=True)
    job_source_defect = models.ForeignKey('JobSourceDefects', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'job_source_defect_proofs'


class JobSourceDefects(models.Model):
    id = models.BigAutoField(primary_key=True)
    creator_login = models.CharField(max_length=100, blank=True, null=True)
    date_create = models.DateTimeField(blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    guilty_employee_id = models.BigIntegerField(blank=True, null=True)
    defect_status = models.ForeignKey(DefectStatuses, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'job_source_defects'


class JobSources(models.Model):
    id = models.BigAutoField(primary_key=True)
    angle = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    color = models.CharField(max_length=255, blank=True, null=True)
    dot_shape = models.CharField(max_length=255, blank=True, null=True)
    source_height = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    len_file = models.CharField(max_length=255, blank=True, null=True)
    line_count = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    offset_height = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    offset_with = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    source_with = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    job = models.ForeignKey('Jobs', models.DO_NOTHING, blank=True, null=True)
    job_source_defect = models.ForeignKey(JobSourceDefects, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'job_sources'


class Jobs(models.Model):
    id = models.BigAutoField(primary_key=True)
    date = models.DateTimeField(blank=True, null=True)
    mat_info = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    x_size = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    y_size = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    name_1 = models.CharField(max_length=255, blank=True, null=True)
    name_2 = models.CharField(max_length=255, blank=True, null=True)
    name_3 = models.CharField(max_length=255, blank=True, null=True)
    name_4 = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'jobs'


class Loans(models.Model):
    id = models.BigAutoField(primary_key=True)
    count = models.IntegerField(blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    in_transit = models.BooleanField(blank=True, null=True)  # This field type is a guess.
    is_repayment = models.BooleanField(blank=True, null=True)  # This field type is a guess.
    status = models.CharField(max_length=15, blank=True, null=True)
    from_cell_branch = models.ForeignKey(CellBranches, models.DO_NOTHING, blank=True, null=True,
                                         related_name='loans_from')
    material_sheet = models.ForeignKey('MaterialSheets', models.DO_NOTHING, blank=True, null=True,
                                       related_name='loans_to')
    to_cell_branch = models.ForeignKey(CellBranches, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'loans'


class LogWorkShifts(models.Model):
    id = models.BigAutoField(primary_key=True)
    login = models.CharField(max_length=255, blank=True, null=True)
    time_enter = models.DateTimeField(blank=True, null=True)
    action = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'log_work_shifts'


class LogWorkerActions(models.Model):
    id = models.BigAutoField(primary_key=True)
    time_action = models.DateTimeField(blank=True, null=True)
    worker_action = models.CharField(max_length=255, blank=True, null=True)
    article = models.ForeignKey(Articles, models.DO_NOTHING, blank=True, null=True)
    cell_branch = models.ForeignKey(CellBranches, models.DO_NOTHING, blank=True, null=True)
    login = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'log_worker_actions'


class MaterialBoxes(models.Model):
    id = models.BigAutoField(primary_key=True)
    count_in_box = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    barcode = models.ForeignKey(Barcodes, models.DO_NOTHING, blank=True, null=True)
    material_sheet = models.ForeignKey('MaterialSheets', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'material_boxes'


class MaterialHardness(models.Model):
    id = models.BigAutoField(primary_key=True)
    hardness = models.IntegerField(blank=True, null=True)
    material_hardness_type = models.ForeignKey('MaterialHardnessTypes', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'material_hardness'

    def __str__(self):
        return f"{self.hardness} {self.material_hardness_type}"


class MaterialHardnessTypes(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=15)

    class Meta:
        managed = False
        db_table = 'material_hardness_types'

    def __str__(self):
        return self.name


class MaterialManufacturers(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'material_manufacturers'

    def __str__(self):
        return self.name


class MaterialPlateTypes(models.Model):
    id = models.BigAutoField(primary_key=True)
    grade = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'material_plate_types'

    def __str__(self):
        return self.grade


class MaterialProcessTypes(models.Model):
    id = models.BigAutoField(primary_key=True)
    type = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'material_process_types'

    def __str__(self):
        return self.type


class MaterialSheetStores(models.Model):
    id = models.BigAutoField(primary_key=True)
    count = models.IntegerField(blank=True, null=True)
    cell_branch = models.ForeignKey(CellBranches, models.DO_NOTHING, blank=True, null=True)
    material_sheet = models.ForeignKey('MaterialSheets', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'material_sheet_stores'


class MaterialSheets(models.Model):
    id = models.BigAutoField(primary_key=True)
    height = models.IntegerField(blank=True, null=True, verbose_name='Висота')
    width = models.IntegerField(blank=True, null=True, verbose_name='Ширина')
    barcode = models.ForeignKey(Barcodes, models.DO_NOTHING, blank=True, null=True, verbose_name='Баркод')
    material = models.ForeignKey('Materials', models.DO_NOTHING, blank=True, null=True, verbose_name='Матеріал')
    article = models.ForeignKey(Articles, models.DO_NOTHING, blank=True, null=True, verbose_name='Артикул')

    class Meta:
        managed = False
        db_table = 'material_sheets'
        verbose_name = 'Лист материала'
        verbose_name_plural = 'Листи материала'


class MaterialSlices(models.Model):
    id = models.BigAutoField(primary_key=True)
    height = models.IntegerField()
    width = models.IntegerField()
    article = models.ForeignKey(Articles, models.DO_NOTHING, blank=True, null=True)
    material = models.ForeignKey('Materials', models.DO_NOTHING, blank=True, null=True)
    id_defective = models.BooleanField(blank=True, null=True)  # This field type is a guess.
    defective_description = models.CharField(max_length=255, blank=True, null=True)
    work_shift = models.ForeignKey('WorkShifts', models.DO_NOTHING, blank=True, null=True)
    creator = models.CharField(max_length=255, blank=True, null=True)
    is_remaining = models.BooleanField(blank=True, null=True)  # This field type is a guess.
    date_create = models.DateTimeField(blank=True, null=True)
    date_write_off = models.DateTimeField(blank=True, null=True)
    work_shift_sheet = models.ForeignKey('WorkShiftSheets', models.DO_NOTHING, blank=True, null=True)
    write_off_status = models.CharField(max_length=255, blank=True, null=True)
    cell_branch = models.ForeignKey(CellBranches, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'material_slices'
        verbose_name = 'Кусок материала'
        verbose_name_plural = 'Куски материала'

    def __str__(self):
        return f'{self.material}, {self.height}x{self.width}'


class MaterialSolvents(models.Model):
    id = models.BigAutoField(primary_key=True)
    solvent = models.CharField(max_length=10, blank=True, null=True, verbose_name='Розчинник')

    class Meta:
        managed = False
        db_table = 'material_solvents'

    def __str__(self):
        return self.solvent


class MaterialUnderlayments(models.Model):
    id = models.BigAutoField(primary_key=True)
    thickness = models.DecimalField(max_digits=5, decimal_places=4, blank=True, null=True, verbose_name='Товщіна')
    underlayment_material = models.CharField(max_length=255, blank=True, null=True, verbose_name='Матеріал підложки')

    class Meta:
        managed = False
        db_table = 'material_underlayments'

    def __str__(self):
        return f"{self.underlayment_material} {self.thickness}"


class Materials(models.Model):
    id = models.BigAutoField(primary_key=True)
    base_thickness_max = models.DecimalField(max_digits=5, decimal_places=3, blank=True, null=True,
                                             verbose_name='Макс. цоколь')
    base_thickness_min = models.DecimalField(max_digits=5, decimal_places=3, blank=True, null=True,
                                             verbose_name='Мін. цоколь')
    thickness = models.DecimalField(max_digits=5, decimal_places=3, blank=True, null=True, verbose_name='Товщина')
    name = models.CharField(max_length=45, blank=True, null=True, verbose_name='Назва')
    material_hardness = models.ForeignKey(MaterialHardness, models.DO_NOTHING, blank=True, null=True,
                                          verbose_name='Твердість')
    material_manufacturer = models.ForeignKey(MaterialManufacturers, models.DO_NOTHING, blank=True, null=True,
                                              verbose_name='Виробник')
    material_plate_type = models.ForeignKey(MaterialPlateTypes, models.DO_NOTHING, blank=True, null=True,
                                            verbose_name='Тип матеріалу')
    material_process_type = models.ForeignKey(MaterialProcessTypes, models.DO_NOTHING, blank=True, null=True,
                                              verbose_name='Тип виробництва')
    material_solvent = models.ForeignKey(MaterialSolvents, models.DO_NOTHING, blank=True, null=True,
                                         verbose_name='Розчинник')
    is_polymeric = models.BooleanField(blank=True, null=True, verbose_name='Є полімером')  # This field type is a guess.
    low_base_thickness_max = models.DecimalField(max_digits=5, decimal_places=3, blank=True, null=True,
                                                 verbose_name='Занижений макс. цоколь')
    low_base_thickness_min = models.DecimalField(max_digits=5, decimal_places=3, blank=True, null=True,
                                                 verbose_name='Занижений мін. цоколь')
    material_underlayment = models.ForeignKey(MaterialUnderlayments, models.DO_NOTHING, blank=True, null=True,
                                              verbose_name='Підложка')

    class Meta:
        managed = False
        db_table = 'materials'
        verbose_name = 'Матеріал'
        verbose_name_plural = 'Матеріали'

    def __str__(self):
        return self.name


class Operators(models.Model):
    id = models.BigAutoField(primary_key=True)
    first_name = models.CharField(max_length=45, blank=True, null=True)
    last_name = models.CharField(max_length=45, blank=True, null=True)
    login = models.CharField(unique=True, max_length=100, blank=True, null=True)
    middle_name = models.CharField(max_length=45, blank=True, null=True)
    cell_branch = models.ForeignKey(CellBranches, models.DO_NOTHING, blank=True, null=True)
    active = models.BooleanField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'operators'


class OrdersBoundWithJobs(models.Model):
    order_id = models.BigIntegerField()
    job = models.OneToOneField(Jobs, models.DO_NOTHING, primary_key=True)

    class Meta:
        managed = False
        db_table = 'orders_bound_with_jobs'
        unique_together = (('job', 'order_id'),)


class PaperColors(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'paper_colors'


class PaperRolls(models.Model):
    id = models.BigAutoField(primary_key=True)
    count = models.IntegerField(blank=True, null=True)
    filename_printer_profile = models.CharField(max_length=50, blank=True, null=True)
    last_update_printer_profile = models.DateField(blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    width = models.IntegerField(blank=True, null=True)
    paper_color = models.ForeignKey(PaperColors, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'paper_rolls'


class Returns(models.Model):
    id = models.BigAutoField(primary_key=True)
    count = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    repayment_date = models.DateTimeField(blank=True, null=True)
    loan = models.ForeignKey(Loans, models.DO_NOTHING, blank=True, null=True)
    material_sheet = models.ForeignKey(MaterialSheets, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'returns'


class RouteGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    date_create = models.DateTimeField(blank=True, null=True)
    date_receive = models.DateTimeField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    in_transit = models.BooleanField(blank=True, null=True)  # This field type is a guess.
    barcode = models.ForeignKey(Barcodes, models.DO_NOTHING, blank=True, null=True)
    from_cell_branch = models.ForeignKey(CellBranches, models.DO_NOTHING, blank=True, null=True,
                                         related_name='routegroups_from')
    to_cell_branch = models.ForeignKey(CellBranches, models.DO_NOTHING, blank=True, null=True,
                                       related_name='routegroups_to')

    class Meta:
        managed = False
        db_table = 'route_groups'


class Routes(models.Model):
    id = models.BigAutoField(primary_key=True)
    received = models.IntegerField(blank=True, null=True)
    sent = models.IntegerField(blank=True, null=True)
    route_group = models.ForeignKey(RouteGroups, models.DO_NOTHING, blank=True, null=True)
    material_sheet = models.ForeignKey(MaterialSheets, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'routes'


class SimpleProducts(models.Model):
    id = models.BigAutoField(primary_key=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    article = models.ForeignKey(Articles, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'simple_products'


class WorkShiftSheets(models.Model):
    id = models.BigAutoField(primary_key=True)
    is_done = models.BooleanField(blank=True, null=True)  # This field type is a guess.
    work_shift = models.ForeignKey('WorkShifts', models.DO_NOTHING, blank=True, null=True)
    creator_login = models.CharField(max_length=100, blank=True, null=True)
    date_create = models.DateTimeField(blank=True, null=True)
    date_last_append = models.DateTimeField(blank=True, null=True)
    cell_branch = models.ForeignKey(CellBranches, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'work_shift_sheets'


class WorkShifts(models.Model):
    id = models.BigAutoField(primary_key=True)
    end_work_shift = models.DateTimeField(blank=True, null=True)
    start_work_shift = models.DateTimeField(blank=True, null=True)
    cell_branch = models.ForeignKey(CellBranches, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'work_shifts'


class WorkersOnAWorkShifts(models.Model):
    work_shift = models.OneToOneField(WorkShifts, models.DO_NOTHING, primary_key=True)
    operator = models.ForeignKey(Operators, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'workers_on_a_work_shifts'
        unique_together = (('work_shift', 'operator'),)

