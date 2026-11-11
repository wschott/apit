from apit.utils.io import backup_file


def test_backup_file(make_tmp_file):
    file = make_tmp_file("original.m4a")
    assert not file.with_name("original.bak.m4a").exists()

    backup_file(file)

    assert file.with_name("original.bak.m4a").exists()
