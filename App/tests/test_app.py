import logging, unittest

from App.models import User, Student, Staff

LOGGER = logging.getLogger(__name__)

# '''
#    Unit Tests
# '''

class UserUnitTests(unittest.TestCase):

    def test_check_password(self):
        Testuser = User("David Goggins", "goggs@gmail.com", "goggs123", "student")
        self.assertTrue(Testuser.check_password("goggs123"))

    def test_set_password(self):
        password = "passtest"
        new_password = "passtest"
        Testuser = User("bob", "bob@email.com", password, "user")
        Testuser.set_password(new_password)
        self.assertTrue(Testuser.check_password(new_password))

    def test_check_password_fails_with_wrong_password(self):
        Testuser = User("David Goggins", "goggs@gmail.com", "goggs123", "student")
        self.assertFalse(Testuser.check_password("wrongpassword"))

    def test_password_is_hashed(self):
        password = "plaintext123"
        Testuser = User("alice", "alice@email.com", password, "user")
        # Password should be hashed, not equal to plaintext
        self.assertNotEqual(Testuser.password, password)

class StaffUnitTests(unittest.TestCase):
    
    def test_init_staff(self):
        newstaff = Staff("Jacob Lester", "jacob55@gmail.com", "Jakey55")
        self.assertEqual(newstaff.name, "Jacob Lester")
        self.assertEqual(newstaff.email, "jacob55@gmail.com")
        self.assertTrue(newstaff.check_password("Jakey55"))

    def test_staff_role(self):
        newstaff = Staff("Test Staff", "staff@example.com", "password")
        self.assertEqual(newstaff.role, "staff")

    def test_staff_initialization_with_various_inputs(self):
        staff1 = Staff("John Doe", "john@example.com", "pass123")
        self.assertEqual(staff1.name, "John Doe")
        self.assertEqual(staff1.email, "john@example.com")
        
        staff2 = Staff("Jane Smith", "jane@example.com", "securepass456")
        self.assertEqual(staff2.name, "Jane Smith")
        self.assertEqual(staff2.email, "jane@example.com")

class StudentUnitTests(unittest.TestCase):

    def test_init_student(self):
        newStudent = Student("David Moore", "david77@outlook.com", "iloveschool67")
        self.assertEqual(newStudent.name, "David Moore")
        self.assertEqual(newStudent.email, "david77@outlook.com")
        self.assertTrue(newStudent.check_password("iloveschool67"))

    def test_student_role(self):
        newStudent = Student("Test Student", "student@example.com", "password")
        self.assertEqual(newStudent.role, "student")

    def test_student_default_hours_accumulated(self):
        newStudent = Student("Hours Test", "hours@example.com", "pass")
        # Default should be None or 0, verify it's falsy
        self.assertIn(newStudent.hoursAccumulated, [None, 0])

    def test_student_default_accolades(self):
        newStudent = Student("Accolades Test", "accolades@example.com", "pass")
        # Default should be None or empty list
        self.assertIn(newStudent.accolades, [None, list, []])

    def test_student_initialization_with_various_inputs(self):
        student1 = Student("Alice Johnson", "alice@example.com", "password123")
        self.assertEqual(student1.name, "Alice Johnson")
        self.assertEqual(student1.email, "alice@example.com")
        
        student2 = Student("Bob Wilson", "bob@example.com", "secure789")
        self.assertEqual(student2.name, "Bob Wilson")
        self.assertEqual(student2.email, "bob@example.com")


# '''
#     Integration Tests
# '''
# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class
# @pytest.fixture(autouse=True, scope="module")
# def empty_db():
#     app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
#     create_db()
#     yield app.test_client()
#     db.drop_all()

# class StaffIntegrationTests(unittest.TestCase):

#     def test_create_staff(self):
#         staff = register_staff("marcus", "marcus@example.com", "pass123")
#         assert staff.username == "marcus"
#         # ensure staff persisted
#         fetched = Staff.query.get(staff.staff_id)
#         assert fetched is not None

#     def test_request_fetch(self):
#         # create a student and a pending request
#         student = Student.create_student("tariq", "tariq@example.com", "studpass")
#         req = Request(student_id=student.student_id, hours=3.5, status='pending')
#         db.session.add(req)
#         db.session.commit()

#         requests = fetch_all_requests()
#         # should include request with student name 'tariq'
#         assert any(r['student_name'] == 'tariq' and r['hours'] == 3.5 for r in requests)

#     def test_hours_approval(self):
#         # prepare staff, student and request
#         staff = register_staff("carmichael", "carm@example.com", "staffpass")
#         student = Student.create_student("niara", "niara@example.com", "studpass")
#         req = Request(student_id=student.student_id, hours=2.0, status='pending')
#         db.session.add(req)
#         db.session.commit()

#         result = process_request_approval(staff.staff_id, req.id)
#         # verify logged hours created and request status updated
#         logged = result.get('logged_hours')
#         assert logged is not None
#         assert logged.hours == 2.0
#         assert result['request'].status == 'approved'

#     def test_hours_denial(self):
#         # prepare staff, student and request
#         staff = register_staff("maritza", "maritza@example.com", "staffpass")
#         student = Student.create_student("jabari", "jabari@example.com", "studpass")
#         req = Request(student_id=student.student_id, hours=1.0, status='pending')
#         db.session.add(req)
#         db.session.commit()

#         result = process_request_denial(staff.staff_id, req.id)
#         assert result['denial_successful'] is True
#         assert result['request'].status == 'denied'


# class StudentIntegrationTests(unittest.TestCase):

#     def test_create_student(self):
#         student = register_student("junior", "junior@example.com", "studpass")
#         assert student.username == "junior"
#         fetched = Student.query.get(student.student_id)
#         assert fetched is not None

#     def test_request_hours_confirmation(self):
#         student = Student.create_student("amara", "amara@example.com", "pass")
#         req = create_hours_request(student.student_id, 4.0)
#         assert req is not None
#         assert req.hours == 4.0
#         assert req.status == 'pending'

#     def test_fetch_requests(self):
#         student = Student.create_student("kareem", "kareem@example.com", "pass")
#         # create two requests
#         r1 = create_hours_request(student.student_id, 1.0)
#         r2 = create_hours_request(student.student_id, 2.5)
#         reqs = fetch_requests(student.student_id)
#         assert len(reqs) >= 2
#         hours = [r.hours for r in reqs]
#         assert 1.0 in hours and 2.5 in hours

#     def test_get_approved_hours_and_accolades(self):
#         student = Student.create_student("nisha", "nisha@example.com", "pass")
#         # Manually add logged approved hours
#         lh1 = LoggedHours(student_id=student.student_id, staff_id=None, hours=6.0, status='approved')
#         lh2 = LoggedHours(student_id=student.student_id, staff_id=None, hours=5.0, status='approved')
#         db.session.add_all([lh1, lh2])
#         db.session.commit()

#         name, total = get_approved_hours(student.student_id)
#         assert name == student.username
#         assert total == 11.0

#         accolades = fetch_accolades(student.student_id)
#         # 11 hours should give at least the 10 hours accolade
#         assert '10 Hours Milestone' in accolades

#     def test_generate_leaderboard(self):
#         # create three students with varying approved hours
#         a = Student.create_student("zara", "zara@example.com", "p")
#         b = Student.create_student("omar", "omar@example.com", "p")
#         c = Student.create_student("leon", "leon@example.com", "p")
#         db.session.add_all([
#             LoggedHours(student_id=a.student_id, staff_id=None, hours=10.0, status='approved'),
#             LoggedHours(student_id=b.student_id, staff_id=None, hours=5.0, status='approved'),
#             LoggedHours(student_id=c.student_id, staff_id=None, hours=1.0, status='approved')
#         ])
#         db.session.commit()

#         leaderboard = generate_leaderboard()
#         # leaderboard should be ordered desc by hours for the students we created
#         names = [item['name'] for item in leaderboard]
#         # ensure our students are present
#         assert 'zara' in names and 'omar' in names and 'leon' in names
#         # assert relative ordering: zara (10) > omar (5) > leon (1)
#         assert names.index('zara') < names.index('omar') < names.index('leon')
