import logging, unittest, pytest, os


from App.main import create_app
from App.database import db, create_db
from App.models import User, Student, Staff, ActivityHistory, Request
from App.models.commands import *

from App.controllers.user import *
from App.controllers.staff import *
from App.controllers.student import *
from App.controllers.activity_history import *
from App.controllers.request import *

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
        new_password = "passtest2"
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
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.drop_all()

class TestUserIntegrationTests:

    def test_create_and_retrieve_user_by_id(self):
        new_user = create_user("Bob", "bobpass", "bobpass@gmail.com", "user")
        retrieved_user = get_user_by_id(new_user.id)
        assert retrieved_user.name == new_user.name

    def test_create_and_retrieve_user_by_name(self):
        new_user = create_user("Rob", "robpass", "realrob@gmail.com", "user")
        retrieved_user = get_user_by_name("Rob")
        assert retrieved_user.id == new_user.id

    def test_get_all_users(self):
        users_count_before = len(get_all_users())
        create_user("Jalice", "jalicepass", "notallice@gmail.com", "user")
        all_users_after = get_all_users()
        users_count_after = len(all_users_after)

        assert users_count_before == 2
        assert users_count_before + 1 == users_count_after

        assert any(user.name == "Jalice" for user in all_users_after)

    def test_update_user(self):
        new_user = create_user("Sam", "jetstream", "brazilman@gmail.com", "user")
        update_result = update_user(new_user.id, username="Samuel", email="notbrazilman@gmail.com", password="yuhpass")
        updated_user = get_user_by_id(new_user.id)

        assert update_result is True
        assert updated_user.name == "Samuel"
        assert updated_user.email == "notbrazilman@gmail.com"
        assert updated_user.check_password("yuhpass")


class TestStaffIntegrationTests:
    
    def test_create_and_retrieve_staff_by_id(self):
        new_staff = create_staff("Dimtriscu", "evilresident@yahoo.com", "evil")
        retrieved_staff = get_staff_by_id(new_staff.id)
        assert retrieved_staff.name is new_staff.name

    def test_get_all_staff(self):
        staff_count_before = len(get_all_staff())
        create_staff("Ben", "bendover@yahoo.com", "benover")
        all_staff = get_all_staff()
        staff_count_after = len(all_staff)

        assert staff_count_before == 1
        assert staff_count_before + 1 == staff_count_after
        assert any(staff.name == "Ben" for staff in all_staff)

    def test_update_staff(self):
        new_staff = create_staff("Senator Armstrong", "nanomachines@yahoo.com", "nanomachinesson")
        update_result = update_user(new_staff.id, username="Armstrong", email="nano@yahoo.com", password="excellus")
        updated_staff = get_staff_by_id(new_staff.id)

        assert update_result is True
        assert updated_staff.name == "Armstrong"
        assert updated_staff.email == "nano@yahoo.com"
        assert updated_staff.check_password("excellus")

class TestStudentIntegrationTests:
    
    def test_create_and_retrieve_student_by_id(self):
        new_student = create_student("John Chainsaw", "johnchainsaw@yahoo.com", "dennis")
        retrieved_student = get_student_by_id(new_student.id)
        assert retrieved_student.name is new_student.name

    def test_get_all_students(self):
        student_count_before = len(get_all_students())
        create_student("Chris", "boulderlover@yahoo.com", "boulder")
        all_students = get_all_students()
        student_count_after = len(all_students)

        assert student_count_before == 1
        assert student_count_before + 1 == student_count_after
        assert any(student.name == "Chris" for student in all_students)

    def test_update_student(self):
        new_student = create_student("Miller", "fiddle@yahoo.com", "motherbase")
        update_result = update_user(new_student.id, username="Filler", email="fiddles@yahoo.com", password="diamond")
        updated_student = get_student_by_id(new_student.id)

        assert update_result is True
        assert updated_student.name == "Filler"
        assert updated_student.email == "fiddles@yahoo.com"
        assert updated_student.check_password("diamond")

class TestRequestIntegrationTests:

    #Positive Testing
    def test_create_request(self):
        student = get_user_by_name("Chris")
        new_request = create_request(student.id, 4, "Assessed The Residents", "The residents are evil")
        retrieved_request = get_request_by_id(new_request.id)

        assert retrieved_request.id == new_request.id
        assert new_request in get_requests_by_student(student.id)

    def test_delete_request(self):
        student = get_user_by_name("Chris")
        new_request = create_request(student.id, 2, "Helped with Boulder", "Punched a boulder")

        delete_request(new_request.id)

        retrieved_request = get_request_by_id(new_request.id)
        assert retrieved_request is None

    def test_approve_request(self):
        staff = get_user_by_name("Ben")
        student = get_user_by_name("Chris")
        new_request = create_request(student.id, 3, "Disposed of Evil Residents", "The residents were evil")

        approve_request(staff.id, new_request.id)

        updated_request = get_request_by_id(new_request.id)
        assert updated_request.status == "approved"

    def test_deny_request(self):
        staff = get_user_by_name("Ben")
        student = get_user_by_name("Chris")
        new_request = create_request(student.id, 5, "Saved Ethan", "Disposed of Ethan's wife")

        process_request_denial(staff.id, new_request.id)

        updated_request = get_request_by_id(new_request.id)
        assert updated_request.status == "denied"

    def test_get_all_requests(self):
        requests_count_before = len(get_all_requests())
        student = create_student("Leon", "raccoon@gmail.com", "ada")

        new_request = create_request(student.id, 1, "Did a Backflip", "Did it to save Ashley")
        all_requests = get_all_requests()
        requests_count_after = len(all_requests)

        assert requests_count_after == 4
        assert requests_count_before + 1 == requests_count_after
        assert any(request.id == new_request.id for request in all_requests)
        
    #Negative Testing
    def test_create_request_with_invalid_student(self):
        invalid_student_id = 9999  # Assuming this ID does not exist

        with pytest.raises(ValueError) as excinfo:
            create_request(invalid_student_id, 100, "Saved The Tojo Clan", "I'm not gonna sugarcoat it, r1 + triangle")
        
        assert f"Student with id {invalid_student_id} not found." in str(excinfo.value)

    def test_approve_request_with_invalid_staff(self):
        student = get_user_by_name("John Chainsaw")
        new_request = create_request(student.id, 3, "Killed The Job Devil", "The Job Devil was scary")
        invalid_staff_id = 9999  # Assuming this ID does not exist

        with pytest.raises(ValueError) as excinfo:
            approve_request(invalid_staff_id, new_request.id)
        
        assert f"Staff with id {invalid_staff_id} not found." in str(excinfo.value)

    def test_deny_request_with_invalid_staff(self):
        student = get_user_by_name("John Chainsaw")
        new_request = create_request(student.id, 6, "Jujutsued My Kaisen", "idk")
        invalid_staff_id = 9999  # Assuming this ID does not exist

        with pytest.raises(ValueError) as excinfo:
            process_request_denial(invalid_staff_id, new_request.id)
        
        assert f"Staff with id {invalid_staff_id} not found." in str(excinfo.value)

    def test_approve_request_with_invalid_request(self):
        staff = get_user_by_name("Ben")
        invalid_request_id = 9999  # Assuming this ID does not exist

        with pytest.raises(ValueError) as excinfo:
            approve_request(staff.id, invalid_request_id)
        
        assert f"Request with id {invalid_request_id} not found." in str(excinfo.value)
    
class TestActivityHistoryIntegrationTests:

    #Postive Testing
    def test_log_hours_and_retrieve_history(self):
        staff = get_user_by_name("Ben")
        student = create_student("James", "silent@gmail.com", "thehillsaresilent")
        log_entry = log_hours(staff.id, student.id, 5, "Ignored Wife", "Found pyramid head instead")

        history = get_activity_history_by_student(student.id)
        assert log_entry in history
        assert log_entry.hours == 5
        assert log_entry.title == "Ignored Wife"
        assert log_entry.action == "logged"

    def test_get_student_history_by_action(self):
        staff = get_user_by_name("Ben")
        student = get_user_by_name("Chris")
        log_entry1 = log_hours(staff.id, student.id, 2, "Recycling", "Recycled materials")
        log_entry2 = log_hours(staff.id, student.id, 3, "Tutoring", "Gave ethan a g#n")
        filtered_history = filter_student_history_by_action(student.id, "logged")
        assert log_entry1 in filtered_history
        assert log_entry2 in filtered_history

    def test_get_student_history_by_request(self):
        staff = get_user_by_name("Ben")
        student = get_user_by_name("Chris")

        new_approved_request = create_request(student.id, 4, "Park Cleanup", "Cleaned up the park")
        approve_request(staff.id, new_approved_request.id)

        new_denied_request = create_request(student.id, 6, "Late Night Noise", "Told the residents not to be evil")
        process_request_denial(staff.id, new_denied_request.id)

        approved_history = filter_student_history_by_action(student.id, "approved")
        denied_history = filter_student_history_by_action(student.id, "denied")

        assert any(entry.request_id == new_approved_request.id for entry in approved_history)
        assert any(entry.request_id == new_denied_request.id for entry in denied_history)

    def test_student_accolades_after_logging_hours(self):
        staff = create_staff("Ultima", "myfantasy@gmail.com", "ultimaweapon")
        student = create_student("Clive", "clive@gmail.com", "rosaria")

        log_hours(staff.id, student.id, 15, "Achieved My Final Fantasy", "The finalest of fantasies")
        accolades = get_student_accolades(student.id)

        assert "10 Hours Milestone" in accolades
        assert "25 Hours Milestone" not in accolades

    def test_student_next_milestone(self):
        student = get_user_by_name("Clive")
        
        assert get_next_milestone(student.id) == 25
    
    def test_get_accolades_history_object(self):
        student = get_user_by_name("Clive")
        accolades_history = filter_student_history_by_action(student.id, "accolade")

        assert any(entry.title == "10 Hours Milestone" for entry in accolades_history)

    #Negative Testing
    def test_log_hours_with_invalid_staff(self):
        student = get_user_by_name("Chris")
        invalid_staff_id = 9999  # Assuming this ID does not exist

        with pytest.raises(ValueError) as excinfo:
            log_hours(invalid_staff_id, student.id, 3, "Crossdressed Cloud", "He looked better than Tifa")
        
        assert f"Staff with id {invalid_staff_id} not found." in str(excinfo.value)

    def test_log_hours_with_invalid_student(self):
        staff = get_user_by_name("Ben")
        invalid_student_id = 9999  # Assuming this ID does not exist

        with pytest.raises(ValueError) as excinfo:
            log_hours(staff.id, invalid_student_id, 3, "Ate Paimon", "我的天呢")
        
        assert f"Student with id {invalid_student_id} not found." in str(excinfo.value)

    def test_get_activity_history_with_invalid_student(self):
        invalid_student_id = 9999  # Assuming this ID does not exist

        with pytest.raises(ValueError) as excinfo:
            get_activity_history_by_student(invalid_student_id)
        
        assert f"Student with id {invalid_student_id} not found." in str(excinfo.value)