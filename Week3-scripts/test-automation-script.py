import unittest
import os
import shutil
import tempfile
 
from log_analyzer import analyze_log
from file_organizer import organize_folder, CATEGORY_MAP
 
 
class TestLogAnalyzer(unittest.TestCase):
    def setUp(self):
        # Create a temporary log file so tests don't depend on any
        # real file existing on disk — this makes the test repeatable
        # on any machine.
        self.temp_log = tempfile.NamedTemporaryFile(
            mode="w", suffix=".log", delete=False
        )
        self.temp_log.write(
            "2026-09-14 ERROR Failed login from 10.0.0.5\n"
            "2026-09-14 WARNING Disk space low\n"
            "2026-09-15 ERROR Failed login from 10.0.0.5\n"
        )
        self.temp_log.close()
 
    def tearDown(self):
        os.remove(self.temp_log.name)
 
    def test_finds_correct_number_of_ips(self):
        results = analyze_log(self.temp_log.name)
        self.assertEqual(len(results["unique_ips"]), 1)
        self.assertIn("10.0.0.5", results["unique_ips"])
 
    def test_counts_error_severity_correctly(self):
        results = analyze_log(self.temp_log.name)
        self.assertEqual(results["severity_counts"]["ERROR"], 2)
        self.assertEqual(results["severity_counts"]["WARNING"], 1)
 
    def test_missing_file_raises_error(self):
        with self.assertRaises(FileNotFoundError):
            analyze_log("this_file_does_not_exist.log")
 
 
class TestFileOrganizer(unittest.TestCase):
    def setUp(self):
        # Create a throwaway temp directory so the test never touches
        # your real files.
        self.temp_dir = tempfile.mkdtemp()
        open(os.path.join(self.temp_dir, "notes.txt"), "w").close()
        open(os.path.join(self.temp_dir, "photo.jpg"), "w").close()
 
    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)
 
    def test_dry_run_does_not_move_files(self):
        organize_folder(self.temp_dir, dry_run=True)
        # Files should still be in the root folder, untouched
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, "notes.txt")))
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, "photo.jpg")))
 
    def test_real_run_moves_files_into_category_folders(self):
        organize_folder(self.temp_dir, dry_run=False)
        self.assertTrue(
            os.path.exists(os.path.join(self.temp_dir, "Documents", "notes.txt"))
        )
        self.assertTrue(
            os.path.exists(os.path.join(self.temp_dir, "Images", "photo.jpg"))
        )
 
    def test_category_map_has_expected_types(self):
        self.assertEqual(CATEGORY_MAP[".py"], "Scripts")
        self.assertEqual(CATEGORY_MAP[".pdf"], "Documents")
 
 
if __name__ == "__main__":
    unittest.main()
 