from django.db import models


#Choice Constants
class FeeStatus(models.TextChoices):
    PAID = 'Paid', 'Paid'
    PENDING = 'Pending', 'Pending'
    OVERDUE = 'Overdue', 'Overdue'


class ExamType(models.TextChoices):
    INTERNAL = 'Internal', 'Internal'
    EXTERNAL = 'External', 'External'
    FINAL = 'Final', 'Final'


class BacklogStatus(models.TextChoices):
    PENDING = 'Pending', 'Pending'
    CLEARED = 'Cleared', 'Cleared'


class AttendanceStatus(models.TextChoices):
    PRESENT = 'Present', 'Present'
    ABSENT = 'Absent', 'Absent'
    LEAVE = 'Leave', 'Leave'


class AlertStatus(models.TextChoices):
    SENT = 'Sent', 'Sent'
    READ = 'Read', 'Read'


#Main Models
class Branches(models.Model):
    branch_id = models.AutoField(primary_key=True)
    branch_name = models.TextField()
    HOD = models.ForeignKey('Faculties', on_delete=models.SET_NULL, null=True, related_name='hod_of_branches')
    created_at = models.DateTimeField()
    modified_at = models.DateTimeField()
    modified_by = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.branch_name


class Batches(models.Model):
    batch_id = models.AutoField(primary_key=True)
    batch_name = models.TextField()
    start_year = models.IntegerField()
    end_year = models.IntegerField()
    created_at = models.DateTimeField()
    modified_at = models.DateTimeField()
    modified_by = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.batch_name


class Faculties(models.Model):
    faculty_id = models.AutoField(primary_key=True)
    first_name = models.TextField()
    last_name = models.TextField()
    email = models.TextField()
    phone_number = models.TextField()
    department = models.ForeignKey(Branches, on_delete=models.SET_NULL, null=True, related_name='faculties')
    designation = models.TextField()
    date_of_joining = models.DateField()
    address = models.TextField()
    created_at = models.DateTimeField()
    modified_at = models.DateTimeField()
    modified_by = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Students(models.Model):
    student_id = models.AutoField(primary_key=True)  # usn or unique roll no.
    first_name = models.TextField()
    last_name = models.TextField()
    email = models.TextField()
    phone_number = models.TextField()
    date_of_birth = models.DateField()
    address = models.TextField()
    branch = models.ForeignKey(Branches, on_delete=models.SET_NULL, null=True, related_name='students')
    batch = models.ForeignKey(Batches, on_delete=models.SET_NULL, null=True, related_name='students')
    father_name = models.TextField()
    father_phno = models.TextField()
    parents_gaurdian_mail = models.TextField()
    mother_name = models.TextField()
    mother_phno = models.TextField()
    guardian_name = models.TextField()
    gaurdian_phno = models.TextField()
    created_at = models.DateTimeField()
    modified_at = models.DateTimeField()
    modified_by = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Subjects(models.Model):
    subject_id = models.AutoField(primary_key=True)
    subject_name = models.TextField()
    branch = models.ForeignKey(Branches, on_delete=models.CASCADE, related_name='subjects')
    created_at = models.DateTimeField()
    modified_at = models.DateTimeField()
    modified_by = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.subject_name


class Fees(models.Model):
    fee_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Students, on_delete=models.CASCADE, related_name='fees')
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    payment_date = models.DateField()
    status = models.CharField(max_length=10, choices=FeeStatus.choices)
    created_at = models.DateTimeField()
    modified_at = models.DateTimeField()
    modified_by = models.TextField()
    is_active = models.BooleanField(default=True)


class Marks(models.Model):
    mark_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Students, on_delete=models.CASCADE, related_name='marks')
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE, related_name='marks')
    exam_type = models.CharField(max_length=20, choices=ExamType.choices)
    score = models.IntegerField()
    grade = models.TextField()
    created_at = models.DateTimeField()
    modified_at = models.DateTimeField()
    modified_by = models.TextField()
    is_active = models.BooleanField(default=True)


class Backlogs(models.Model):
    backlog_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Students, on_delete=models.CASCADE, related_name='backlogs')
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE, related_name='backlogs')
    exam_type = models.CharField(max_length=20, choices=ExamType.choices)
    status = models.CharField(max_length=10, choices=BacklogStatus.choices)
    attempt_number = models.IntegerField()
    created_at = models.DateTimeField()
    modified_at = models.DateTimeField()
    modified_by = models.TextField()
    is_active = models.BooleanField(default=True)


class Classes(models.Model):
    class_id = models.AutoField(primary_key=True)
    class_name = models.TextField()
    class_teacher = models.ForeignKey(Faculties, on_delete=models.SET_NULL, null=True, related_name='teaching_classes')
    batch = models.ForeignKey(Batches, on_delete=models.SET_NULL, null=True, related_name='classes')
    students = models.ForeignKey(Students, on_delete=models.SET_NULL, null=True, related_name='enrolled_classes')
    created_at = models.DateTimeField()
    modified_at = models.DateTimeField()
    modified_by = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.class_name


class Class_sub(models.Model):
    class_sub_id = models.AutoField(primary_key=True)
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE, related_name='class_subjects')
    class_id = models.ForeignKey(Classes, on_delete=models.CASCADE, related_name='subjects')
    faculty = models.ForeignKey(Faculties, on_delete=models.SET_NULL, null=True, related_name='subject_classes')
    created_at = models.DateTimeField()
    modified_at = models.DateTimeField()
    modified_by = models.TextField()
    is_active = models.BooleanField(default=True)


class Attendance(models.Model):
    attendance_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Students, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField()
    status = models.CharField(max_length=10, choices=AttendanceStatus.choices)
    class_sub = models.ForeignKey(Class_sub, on_delete=models.CASCADE, related_name='attendance_records')
    created_at = models.DateTimeField()
    modified_at = models.DateTimeField()
    modified_by = models.TextField()
    is_active = models.BooleanField(default=True)


class ParentAlerts(models.Model):
    alert_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Students, on_delete=models.CASCADE, related_name='alerts')
    message = models.TextField()
    timestamp = models.DateTimeField()
    status = models.CharField(max_length=10, choices=AlertStatus.choices)

    # Links to most relevant context
    fee = models.ForeignKey(Fees, on_delete=models.SET_NULL, null=True, related_name='alerts')
    mark = models.ForeignKey(Marks, on_delete=models.SET_NULL, null=True, related_name='alerts')
    attendance = models.ForeignKey(Attendance, on_delete=models.SET_NULL, null=True, related_name='alerts')
    backlog = models.ForeignKey(Backlogs, on_delete=models.SET_NULL, null=True, related_name='alerts')

    created_at = models.DateTimeField()
    modified_at = models.DateTimeField()
    modified_by = models.TextField()
    is_active = models.BooleanField(default=True)
