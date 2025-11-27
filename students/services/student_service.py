class StudentService:
    @staticmethod
    def toggle_active(student_id):
        from students.models import Student

        try:
            student = Student.objects.get(id=student_id)
            student.user.is_active = not student.user.is_active
            student.user.save()
            return True
        except Student.DoesNotExist:
            return False