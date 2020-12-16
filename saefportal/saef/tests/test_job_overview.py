import pytz
from datetime import datetime, timedelta
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from mock import Mock
from saef.models import JobSessionMetaData

from utils.test_utils import load_test_db

def mockTimezoneNow():
    date_now_mock = datetime(2020, 8, 12, 15, 37, 26, 179787, tzinfo=pytz.utc)
    timezone.now = Mock(return_value=date_now_mock)
    return date_now_mock
class JobOverviewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        load_test_db("saef", "test_dataset_overview")
        
    def setUp(self):
        self.client.login(email='t@test.com', password='test')
        self.date_now_mock = mockTimezoneNow()
        
    def get_response(self, parameters):
        response = self.client.get(reverse('job_session') + parameters)
        self.assertEqual(response.status_code, 200)
        return response
    
    def check_status_type_in_dataset_sessions(self, response, status):
        for job in response.context['job_sessions_metadata']:
            self.assertEqual(job.status_type, status)
            
    def check_timestamp_in_dataset_session(self, response, past_time):
        for job in response.context['job_sessions_metadata']:
            self.assertGreaterEqual(job.job_session.create_timestamp, past_time)  
    
    def test_view_get(self):
        response = self.client.get(reverse('job_session'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'job_overview/job_overview.html')
        
        expected = JobSessionMetaData.objects.filter().count()
        self.assertEqual(len(response.context['job_sessions_metadata']), expected)

    def test_filter_status_all(self):
        response = self.get_response('?status_option=All+status')
        self.assertEqual(len(response.context['job_sessions_metadata']), 3)
        
    def test_filter_status_succeeded(self):
        response = self.get_response('?status_option=Succeeded')
        self.assertEqual(len(response.context['job_sessions_metadata']), 1)
        self.check_status_type_in_dataset_sessions(response, 'SUCCEEDED')
        
    def test_filter_status_succeeded_with_issue(self):
        response = self.get_response('?status_option=Succeeded+with+issue')
        self.assertEqual(len(response.context['job_sessions_metadata']), 1)
        self.check_status_type_in_dataset_sessions(response, 'SUCCEEDED_ISSUE')

    def test_filter_status_failed(self):
        response = self.get_response('?status_option=Failed')
        self.assertEqual(len(response.context['job_sessions_metadata']), 1)
        self.check_status_type_in_dataset_sessions(response, 'FAILED')

    def test_filter_date_all(self):
        response = self.get_response('?date_option=All')
        self.assertEqual(len(response.context['job_sessions_metadata']), 3)
        
    def test_filter_date_last_7_days(self):
        response = self.get_response('?date_option=7+days')
        past_7 = self.date_now_mock + timedelta(days=-7)
        
        self.assertEqual(len(response.context['job_sessions_metadata']), 2)
        self.check_timestamp_in_dataset_session(response, past_7)
            
    def test_filter_date_last_31_days(self):
        response = self.get_response('?date_option=1+month')
        past_31 = self.date_now_mock + timedelta(days=-31)
        
        self.assertEqual(len(response.context['job_sessions_metadata']), 3)
        self.check_timestamp_in_dataset_session(response, past_31)
            
    def test_filter_multiple_arguments_daterange31_statustype(self):
        response = self.get_response('?date_option=1+month&status_option=Succeeded')
        self.assertEqual(len(response.context['job_sessions_metadata']), 1)
            
    def test_filter_orderby(self):
        response = self.get_response('?order_by=name')
        
        def session_name(session):
            return f'{session.job_session.job.name}_{session.pk}'
        
        self.assertEqual(session_name(response.context['job_sessions_metadata'][0]), 'LoadDimCustomer_1')
        self.assertEqual(session_name(response.context['job_sessions_metadata'][1]), 'LoadDimCustomer_2')
        self.assertEqual(session_name(response.context['job_sessions_metadata'][2]), 'LoadDimCustomer_3')
        
        response = self.get_response('?order_by=-name')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(session_name(response.context['job_sessions_metadata'][0]), 'LoadDimCustomer_3')
        self.assertEqual(session_name(response.context['job_sessions_metadata'][1]), 'LoadDimCustomer_2')
        self.assertEqual(session_name(response.context['job_sessions_metadata'][2]), 'LoadDimCustomer_1')
        
    def test_filter_application_all(self):
        response = self.get_response('?application_option=All+applications')
        self.assertEqual(len(response.context['job_sessions_metadata']), 3)
        
    def test_filter_application_selected_exist(self):
        selected_application = 'AdventureWorks'
        response = self.get_response(f'?application_option={selected_application}')
        self.assertEqual(len(response.context['job_sessions_metadata']), 3)
        
    def test_filter_application_selected_does_not_exist(self):
        selected_application = 'Northwind'
        response = self.get_response(f'?application_option={selected_application}')
        self.assertEqual(len(response.context['job_sessions_metadata']), 0)