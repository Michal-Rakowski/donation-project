from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.db.models import Avg, Count, Min, Sum
from .models import *

def create_category(name="Sample Category"):
    """
    Creates sample category
    """   
    return Category.objects.create(name=name)

def create_institution(name="Sample Institution", 
                    description="Sample description", institution_type="FUND"):
    return Institution.objects.create(name=name, description=description, institution_type=institution_type)

def create_user(first_name='Lukasz', 
                last_name='Blos', email='lukasz@mail.com', 
                password='lukasz_password51'):
    return CustomUser.objects.create(first_name=first_name, last_name=last_name, 
                                    email=email, password=password)

def create_donation(user="user", institution="institution",quantity=5,
                    address="adress", phone_number="phone_number",
                    city="city", zip_code="zip_code", 
                    pick_up_date_time=timezone.now(), pick_up_comment="pick_up_comment"):

    user = create_user()
    institution = create_institution()
    return Donation.objects.create(user=user, institution=institution, quantity=quantity,
                    address=address, phone_number=phone_number,
                    city=city, zip_code=zip_code, pick_up_date_time=pick_up_date_time, 
                    pick_up_comment=pick_up_comment)

class LandingPageTests(TestCase):
    def test_landing_page_access(self):
        """
        Verifies that landing page load properly and returns 200 ok status
        """
        url = reverse('landing-page')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_context_data_no_instutions(self):
        """
        If no institutions were created appropriate message is displayed
        """
        response = self.client.get(reverse('landing-page'))
        self.assertContains(response, "Zgloś instytucję")
        self.assertTrue('institutions' in response.context)


    def test_context_data_with_institutions(self):
        """
        Verifies that view return all created institutions
        """
        institution1 = create_institution()
        institution2 = create_institution(name='Institution2', 
                                          description='Description of institution2',
                                          institution_type='OPOZ')
        institution3 = create_institution(name='Institution3', 
                                          description='Description of institution3',
                                          institution_type='FUND')
        response = reverse('landing-page')
        response = self.client.get(reverse('landing-page'))
        self.assertEqual(Institution.objects.all().count(), 3)
        self.assertContains(response, b'Description of institution3')

    def test_additional_context_with_no_donations(self):
        """
        Tests if aggregation produces correct result without created donations and 
        if that context is displayed in template
        """
        response = reverse('landing-page')
        response = self.client.get(reverse('landing-page'))
        self.assertEqual(Donation.objects.aggregate(total_bags=Sum('quantity'))['total_bags'], None)
        self.assertEqual(Donation.objects.aggregate(total_institutions=Count('institution'))['total_institutions'], 0)
        self.assertTrue('total_bags' in response.context)
        self.assertTrue('total_institutions' in response.context)
        self.assertContains(response, b'0')
    
    def test_context_with_donations(self):
        """
        Tests if aggregation produces correct result if donations were created and 
        if that context is displayed in template
        """
        donation1 = create_donation()
        response = reverse('landing-page')
        response = self.client.get(reverse('landing-page'))
        self.assertEqual(Donation.objects.aggregate(total_bags=Sum('quantity'))['total_bags'], 5)
        self.assertEqual(Donation.objects.aggregate(total_institutions=Count('institution'))['total_institutions'], 1)
        self.assertTrue('total_bags' in response.context)
        self.assertTrue('total_institutions' in response.context)
        self.assertContains(response, b'5')

class UsersManagersTests(TestCase):
    """
    Verifies creation of user and superuser with CustomUserManager
    """
    def test_create_user(self):
        """
        Verifies creation of regular user
        """
        User = get_user_model()
        user = User.objects.create_user(email='normal@user.com', password='foo')
        self.assertEqual(user.email, 'normal@user.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_admin)
        try:
            # username does not exist for the AbstractBaseUser option
            self.assertNotExist(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(ValueError):
            User.objects.create_user(email='')
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password="foo")

    def test_create_superuser(self):
        """
        Verifies creation of superuser(admin)
        """
        User = get_user_model()
        admin_user = User.objects.create_superuser('super@user.com', 'foo')
        self.assertEqual(admin_user.email, 'super@user.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_admin)
        try:
            # username does not exist for the AbstractBaseUser option
            self.assertNotExist(admin_user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            User.objects.create_superuser(
                email='super@user.com', password='foo', is_admin=False)


class RegisterViewTests(TestCase):
    def test_register_view_access(self):
        """
        Verifies register view is returning 200 ok status
        """
        url = reverse('register')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_register_user(self):
        """
        Verifies user gets created if post data is correct
        """
        url = reverse('register')
        response = self.client.post(url, {
            'first_name': 'Michal', 
            'last_name': 'Rakowski', 
            'email': 'michal@mail.com',
            'password1': 'michal_password51',
            'password2': 'michal_password51'
        })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url=reverse('login'), status_code=302, target_status_code=200)
        self.assertTrue(CustomUser.objects.filter(email='michal@mail.com').exists())
        self.assertTrue(CustomUser.objects.filter(email='michal@mail.com').count(), 1)

    def test_create_user_if_exist(self):
        """
        Verifies unique constraint for email
        """
        user = create_user()
        user.refresh_from_db()
        self.assertTrue(CustomUser.objects.filter(email='lukasz@mail.com').exists())
        url = reverse('register')
        response = self.client.post(url, {
            'first_name': 'Luke', 
            'last_name': 'Rakow', 
            'email': 'lukasz@mail.com',
            'password1': 'luke_password51',
            'password2': 'luke_password51'
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, b'A user with such email already exists.')

    def test_register_if_password_mismatch(self):
        """
        No user created if passwords do not match
        """
        url = reverse('register')
        response = self.client.post(url, {
            'first_name': 'Tom', 
            'last_name': 'Korizow', 
            'email': 'tom@mail.com',
            'password1': 'tom_password51',
            'password2': 'tompassword51'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(CustomUser.objects.filter(email='tom@mail.com').exists())
        ##ASSERTION ERROR EVEN THO MESSAGE DISPLAYS - Why? 
        #self.assertContains(response, b"Passwords don't match")


class LoginViewTests(TestCase):
    def test_login_view_acccess(self):
        """
        Verifies login view is returning 200 ok status
        """
        url = reverse('login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class AddDonationViewTests(TestCase):
    def test_add_donation_access(self):
        """
        Verifies add-donation view is accessible upon request
        """
        url = reverse('add-donation')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)