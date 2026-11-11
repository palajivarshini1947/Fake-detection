from django.db import models

class Contact(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    subject=models.CharField(max_length=100)
    message=models.TextField()
    class Meta:
        db_table='Contact'

class Admin(models.Model):
    email=models.EmailField()
    password=models.CharField(max_length=100)
    class Meta:
        db_table='Admin'

class Notification(models.Model):
    title=models.CharField(max_length=100)
    message=models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table='Notification'


class CustomerRegi(models.Model):
    email=models.EmailField()
    password=models.CharField(max_length=100)
    name=models.TextField()
    mobile=models.BigIntegerField()
    address=models.TextField()
    pincode=models.BigIntegerField()
    status = models.CharField(max_length=20, default='Pending')
    class Meta:
        db_table='customer_regi'

class JobProvider(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    password=models.CharField(max_length=100)
    phone=models.BigIntegerField()
    status=models.CharField(max_length=20, default='Pending')
    class Meta:
        db_table='JobProvider'



class JobPosting(models.Model):
    # Link the job to the provider who posted it
    provider = models.ForeignKey(JobProvider, on_delete=models.CASCADE)

    # Core Job Fields
    title = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    salary_range = models.CharField(max_length=100, blank=True, null=True)

    # Text Fields (using TextField for longer paragraphs)
    description = models.TextField()
    requirements = models.TextField(blank=True, null=True)
    benefits = models.TextField(blank=True, null=True)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'JobPosting'

    def __str__(self):
        return self.title


class JobApplication(models.Model):
    job = models.ForeignKey('JobPosting', on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey('CustomerRegi', on_delete=models.CASCADE, related_name='applications')

    # Allows the user to upload a resume (PDF, DOCX)
    resume = models.FileField(upload_to='resumes/')
    cover_letter = models.TextField(blank=True, null=True)

    # Application Status: Pending, Accepted, Rejected
    status = models.CharField(max_length=20, default='Pending')
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'JobApplication'

    def __str__(self):
        return f"{self.applicant.name} applied for {self.job.title}"