from django.test import TestCase
from django.urls import reverse
from common.models import Documentation
import os
from django.conf import settings

class TooltipTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Path of the directory where the tooltip markdown files are stored
        tooltips_path = os.path.join(settings.BASE_DIR, '../docs')
        # Tooltip file path
        tooltip_file = os.path.join(tooltips_path, 'example.md')
        
        # Populate the tooltip markdown file with some content
        with open(tooltip_file, 'w') as file:
            file.write("# Example Tooltip\nThis is an example tooltip content.")

        # Create a Tooltip instance pointing to the newly created markdown file
        Documentation.objects.create(
            identifier='example',
            description='Example Tooltip',
            markdown_file=tooltip_file
        )

    def test_tooltip_retrieval(self):
        # Get the URL for the tooltip retrieval view
        url = reverse('docs', kwargs={'identifier': 'example'})
        response = self.client.get(url)

        # Check that the response is 200 OK
        self.assertEqual(response.status_code, 200)

        # Check that the Markdown content was converted to HTML
        expected_html = "<h1>Example Tooltip</h1>\n<p>This is an example tooltip content.</p>\n"
        self.assertHTMLEqual(response.content.decode('utf-8'), expected_html)

    def test_tooltip_not_found(self):
        # Test retrieval of a non-existent tooltip
        url = reverse('docs', kwargs={'identifier': 'nonexistent'})
        response = self.client.get(url)

        # Check that the response is 404 Not Found
        self.assertEqual(response.status_code, 404)

class DocumentationFileTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a temporary directory and add some Markdown files
        cls.docs_path = os.path.join(settings.BASE_DIR, '../docs')
        cls.files = ['test1.md', 'test2.md', 'not_a_md_file.txt']
        for file in cls.files:
            print(os.path.join(cls.docs_path, file))
            with open(os.path.join(cls.docs_path, file), 'w') as f:
                f.write(f"Content for {file}")
                
    @classmethod
    def tearDownClass(cls):
        # Clean up by removing the directory after tests run
        for file in cls.files:
            os.remove(os.path.join(cls.docs_path, file))
        super().tearDownClass()
    
    def test_list_markdown_files(self):
        response = self.client.get(reverse('list_docs'))
        self.assertEqual(response.status_code, 200)
        
        expected_files = ['test1.md', 'test2.md']
        response_files = response.json()
        
        # Check that each expected file is in the response
        for file_name in expected_files:
            self.assertIn(file_name, response_files)