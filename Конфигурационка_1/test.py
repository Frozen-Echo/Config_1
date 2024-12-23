import unittest
import os
import shutil
import tempfile
from commands import process_command

class TestShellEmulatorWindows(unittest.TestCase):
    def setUp(self):
        # Создаём временную директорию для тестов
        self.temp_dir = tempfile.mkdtemp()
        self.username = "kweezy"
        self.current_dir = "/"
        self.vfs_path = self.temp_dir

        # Создаём тестовую файловую структуру
        os.makedirs(os.path.join(self.vfs_path, "testfs"), exist_ok=True)
        with open(os.path.join(self.vfs_path, "test.txt"), "w") as f:
            f.write("Sample text")

    def tearDown(self):
        # Удаляем временные файлы после каждого теста
        shutil.rmtree(self.temp_dir)

    def test_ls_root(self):
        output, change_dir = process_command("ls", self.current_dir, self.vfs_path, self.username)
        expected = "\n".join(sorted(["testfs", "test.txt"]))
        self.assertEqual(output, expected)
        self.assertFalse(change_dir)

    def test_ls_directory(self):
        output, change_dir = process_command("ls", "/testfs", self.vfs_path, self.username)
        expected = ""  # testfs пустой
        self.assertEqual(output, expected)
        self.assertFalse(change_dir)

    def test_cd_valid_directory(self):
        output, change_dir = process_command("cd testfs", self.current_dir, self.vfs_path, self.username)
        self.assertEqual(output, os.path.normpath("/testfs"))
        self.assertTrue(change_dir)

    def test_cd_invalid_directory(self):
        output, change_dir = process_command("cd nonexistent", self.current_dir, self.vfs_path, self.username)
        self.assertEqual(output, "cd: nonexistent: No such directory")
        self.assertFalse(change_dir)

    # date
    def test_date_no_args(self):
        output, change_dir = process_command("date", self.current_dir, self.vfs_path, self.username)
        self.assertNotEqual("", output)
        self.assertFalse(change_dir)

    def test_date_format_length(self):
        output, _ = process_command("date", self.current_dir, self.vfs_path, self.username)
        self.assertTrue(len(output) > 5)

    # touch
    def test_touch_create_file(self):
        file_name = "newfile.txt"
        output, change_dir = process_command(f"touch {file_name}", self.current_dir, self.vfs_path, self.username)
        self.assertTrue(os.path.exists(os.path.join(self.vfs_path, file_name)))
        self.assertFalse(change_dir)

    def test_touch_usage(self):
        output, change_dir = process_command("touch", self.current_dir, self.vfs_path, self.username)
        self.assertEqual("Usage: touch <filename>", output)
        self.assertFalse(change_dir)

    # rev
    def test_rev_existing_file(self):
        output, change_dir = process_command("rev test.txt", self.current_dir, self.vfs_path, self.username)
        self.assertIn("txet elpmaS", output)
        self.assertFalse(change_dir)

    def test_rev_non_existent(self):
        output, change_dir = process_command("rev nofile.txt", self.current_dir, self.vfs_path, self.username)
        self.assertEqual("rev: cannot open 'nofile.txt': No such file", output)
        self.assertFalse(change_dir)

    def test_rev_usage(self):
        output, change_dir = process_command("rev", self.current_dir, self.vfs_path, self.username)
        self.assertEqual("Usage: rev <filename>", output)
        self.assertFalse(change_dir)

if __name__ == '__main__':
    unittest.main()
