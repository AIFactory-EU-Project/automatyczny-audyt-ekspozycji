#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import os
import unittest
from io import BytesIO
from unittest import mock

from ai_service.api.common.exceptions import LowResolutionImage
from ai_service.api.common.helpers import create_app
from ai_service.api.settings import TestConfig, ProdConfig


def raise_validation_error(**kwargs):
    raise LowResolutionImage()


def raise_500_error(**kwargs):
    raise 5/0


class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestConfig).test_client()
        img1 = open(os.path.abspath(os.path.dirname(__file__))
                    + '/images/valid.jpg', 'rb')
        self.test_image = BytesIO(img1.read())
        img1.close()
        img2 = open(os.path.abspath(os.path.dirname(__file__))
                    + '/images/invalid.png', 'rb')
        self.test_invalid_image = BytesIO(img2.read())
        img2.close()

    def test_verify_grill_photo_valid_for_analysis(self):
        request = self.app.post('/verify-grill-photo-valid-for-analysis'
                                , content_type='multipart/form-data',
                                data={'image': (self.test_image, 'img1.jpg')})
        self.assertEqual(request.status_code, 200)
        body = json.loads(str(request.data, 'utf8'))
        self.assertEqual(body, {})

    def test_verify_shelf_photo_valid_for_analysis(self):
        request = self.app.post('/verify-shelf-photo-valid-for-analysis'
                                , content_type='multipart/form-data',
                                data={'image': (self.test_image, 'img1.jpg')})
        self.assertEqual(request.status_code, 200)
        body = json.loads(str(request.data, 'utf8'))
        self.assertEqual(body, {})

    def test_remove_faces_from_photo(self):
        request = self.app.post("/remove-faces-from-photo", content_type='multipart/form-data',
                                data={'image': (self.test_image, 'img1.jpg')})
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.content_type, 'image/jpeg')
        self.assertGreater(len(request.data), 0)

    def test_generate_grill_report(self):
        request = self.app.post('/generate-grill-report'
                                , content_type='multipart/form-data',
                                data={'image': (self.test_image, 'img1.jpg')})
        self.assertEqual(request.status_code, 200)
        body = json.loads(str(request.data, 'utf8'))
        self.assertEqual(body, {'count': 0})

    def test_generate_planogram_report(self):
        request = self.app.post('/generate-planogram-report'
                                , content_type='multipart/form-data',
                                data={'image': (self.test_image, 'img1.jpg'), 'planogram_id': 123})
        self.assertEqual(request.status_code, 200)
        self.assertIn('planogramReport', str(request.data, 'utf8'))

    def test_generate_planogram_report_400(self):
        request = self.app.post('/generate-planogram-report'
                                , content_type='multipart/form-data',
                                data={'image': (self.test_image, 'img1.jpg')})
        self.assertEqual(request.status_code, 400)

    @mock.patch('api.models.PlanogramReport.add_detected_object', side_effect=raise_validation_error)
    def test_generate_planogram_report_custom_400(self, mock):
        request = self.app.post('/generate-planogram-report'
                                , content_type='multipart/form-data',
                                data={'image': (self.test_image, 'img1.jpg'), 'planogram_id': 123})
        self.assertEqual(request.status_code, 400)
        self.assertIn('low resolution image', str(request.data, 'utf8'))

    @mock.patch('api.models.PlanogramReport.add_detected_object', side_effect=raise_500_error)
    def test_generate_planogram_report_500(self, mock):
        self.app = create_app(ProdConfig).test_client()
        request = self.app.post('/generate-planogram-report'
                                , content_type='multipart/form-data',
                                data={'image': (self.test_image, 'img1.jpg'), 'planogram_id': 123})
        self.assertEqual(request.status_code, 500)

    def test_health_check(self):
        request = self.app.get("/health-check")
        self.assertEqual(request.status_code, 200)

    def test_broken_picture(self):
        request = self.app.post('/verify-grill-photo-valid-for-analysis'
                                , content_type='multipart/form-data',
                                data={'image': (self.test_invalid_image, 'img1.jpg')})
        body = json.loads(str(request.data, 'utf8'))
        self.assertEqual(body.get('image', [0])[0], 'Invalid value.')
        self.assertEqual(request.status_code, 400)

