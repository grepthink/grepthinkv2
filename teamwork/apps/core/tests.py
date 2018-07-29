from django.core.urlresolvers import resolve
from django.test import TestCase

from django.contrib.auth.models import User

from teamwork.apps.core.views import *
from teamwork.apps.core.models import EmailAddressAuthBackend, po_match

from teamwork.apps.profiles.models import Profile, Skills
from teamwork.apps.courses.models import Course, Enrollment
from teamwork.apps.projects.models import Project, Interest

# class MatchPageTest(TestCase):
#     def test_root_url_resolves_to_match_page_view(self):
#         found = resolve('/')
#         self.assertEqual(found.func, index)


class AuthenticateWithEmailTest(TestCase):
    """
    Creates a user and asserts return values are correct from authenticate method
    """
    def setUp(self):
        self.user1 = User.objects.create_user('user_test1', 'test1@test.com', 'groupthink')

    def tearDown(self):
        del self.user1

    def testAuthenticateSuccess(self):
        """
        Attempt to authenticate user w/ correct email address and pw and assert user object is returned
        """
        user = EmailAddressAuthBackend.authenticate(self, username='test1@test.com', password='groupthink')
        self.assertTrue(type(user) is User)

    def testAuthenticateFail(self):
        """
        Attempt to authenticate user w/ incorrect password and assert user object is None
        """
        user = EmailAddressAuthBackend.authenticate(self, username='test1@test.com', password='incorrect')
        self.assertIsNone(user)

class FindProjectMatchesTest(TestCase):

    def setUp(self):
        # create users
        self.user1 = User.objects.create_user('user1', 'user1@test.com', 'testing')
        self.user2 = User.objects.create_user('user2', 'user2@test.com', 'testing')
        self.user3 = User.objects.create_user('user3', 'user3@test.com', 'testing')

        # create course
        self.course = Course.objects.create(name='TestCourse',slug='Test1', creator=self.user1)

        # create enrollment objects
        self.enrollment1 = Enrollment.objects.create(user=self.user1, course=self.course, role='professor')
        self.enrollment2 = Enrollment.objects.create(user=self.user2, course=self.course, role='student')
        self.enrollment3 = Enrollment.objects.create(user=self.user3, course=self.course, role='student')

        # user1 create project
        self.project = Project.objects.create(creator=self.user1,
                                              scrum_master=self.user1,
                                              ta=self.user1,
                                              slug='TestCourse1')

        # add project to course
        self.course.projects.add(self.project)

        # create skills that the project will desire
        self.skill1 = Skills.objects.create(skill='SkillOne')
        self.skill2 = Skills.objects.create(skill='SkillTwo')

        # add skill1 to profile2 known skills
        self.user2.profile.known_skills.add(self.skill1)

        # add skill2 to profile3 known skills
        self.user3.profile.known_skills.add(self.skill2)

        # user2 and 3 show interest in created project
        self.interest1 = Interest.objects.create(user=self.user2, interest=5, interest_reason='five')
        self.interest2 = Interest.objects.create(user=self.user3, interest=4, interest_reason='four')

        self.project.interest.add(self.interest1)
        self.project.interest.add(self.interest2)

    def tearDown(self):
        """
        TODO: Is this necessary?
        """
        # delete users
        del self.user1
        del self.user2
        del self.user3

        # delete project
        del self.project

        # delete course
        del self.course

        # delete interest
        del self.interest1
        del self.interest2

    def testMatchWithoutScheduleBonus(self):
        matchesList = po_match(self.project)

        # Assert User2 is the first
        self.assertTrue(matchesList[0][0] == self.user2)

        # Assert User3 is the second
        self.assertTrue(matchesList[1][0] == self.user3)

        # Assert User2's score is greater than User3's
        self.assertTrue(matchesList[0][1][0] > matchesList[1][1][0])

    def testMatchWithScheduleBonus(self):
        # TODO
        # set schedules of users

        # perform match
        # matchesList = po_match(self.project)

        # assert return value
