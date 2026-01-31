"""
Tests unitaires pour les modèles de l'application medical.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import date, timedelta

# Récupère le modèle User personnalisé
User = get_user_model()

class BaseTest(TestCase):
    """Classe de base pour les tests avec des données communes"""
    
    @classmethod
    def setUpTestData(cls):
        """Configuration initiale pour tous les tests"""
        # Création d'un utilisateur administrateur
        cls.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123',
            first_name='Admin',
            last_name='System',
            role='admin'
        )
        
        # Création d'un utilisateur médecin
        cls.doctor_user = User.objects.create_user(
            username='docteur.dupont',
            password='docteur123',
            first_name='Jean',
            last_name='Dupont',
            email='jean.dupont@example.com',
            role='doctor',
            is_staff=True
        )


class UserModelTest(BaseTest):
    """Tests pour le modèle User"""
    
    def test_create_user(self):
        """Teste la création d'un utilisateur standard"""
        user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            first_name='Test',
            last_name='User',
            email='test@example.com',
            role='nurse'
        )
        
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.get_full_name(), 'Test User')
        self.assertEqual(user.role, 'nurse')
        self.assertTrue(user.check_password('testpass123'))
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)
    
    def test_create_superuser(self):
        """Teste la création d'un superutilisateur"""
        admin = User.objects.create_superuser(
            username='superadmin',
            password='adminpass',
            email='super@example.com',
            first_name='Super',
            last_name='Admin',
            role='admin'
        )
        
        self.assertTrue(admin.is_superuser)
        self.assertTrue(admin.is_staff)
        self.assertEqual(admin.role, 'admin')


# Test pour le modèle Patient
class PatientModelTest(BaseTest):
    """Tests pour le modèle Patient"""
    
    def test_create_patient(self):
        """Teste la création d'un patient avec des données valides"""
        from patients.models import Patient
        
        patient_data = {
            'first_name': 'Sophie',
            'last_name': 'Martin',
            'patient_id': 'PAT12345',
            'gender': 'F',
            'phone': '0612345678',
            'email': 'sophie.martin@example.com',
            'address': '123 Rue de la Santé',
            'city': 'Paris',
            'blood_type': 'A+',
            'status': 'active',
            'created_by': self.doctor_user
        }
        
        patient = Patient.objects.create(**patient_data)
        
        # Vérifications
        self.assertEqual(patient.first_name, 'Sophie')
        self.assertEqual(patient.last_name, 'Martin')
        self.assertEqual(patient.gender, 'F')
        self.assertEqual(patient.created_by, self.doctor_user)
        self.assertIsNotNone(patient.registration_date)
    
    def test_patient_str_representation(self):
        """Teste la représentation en chaîne du patient"""
        from patients.models import Patient
        
        patient = Patient(
            first_name='Jean',
            last_name='Dupont',
            patient_id='PAT67890',
            gender='M',
            phone='0612345678',
            email='jean.dupont@example.com',
            address='456 Avenue des Lilas',
            city='Lyon',
            blood_type='O+',
            status='active',
            created_by=self.doctor_user
        )
        
        self.assertEqual(str(patient), 'Dupont Jean (PAT67890)')
    
    def test_patient_age_calculation(self):
        """Teste le calcul de l'âge du patient"""
        from patients.models import Patient
        
        # Créer une date de naissance pour avoir 25 ans
        birth_date = date.today().replace(year=date.today().year - 25)
        
        patient = Patient(
            first_name='Test',
            last_name='Age',
            date_of_birth=birth_date,
            patient_id='PAT99999',
            gender='M',
            phone='0612345678',
            email='test.age@example.com',
            address='789 Boulevard des Roses',
            city='Marseille',
            blood_type='B-',
            status='active',
            created_by=self.doctor_user
        )
        
        self.assertEqual(patient.calculate_age(), 25)
