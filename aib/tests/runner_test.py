import pytest
from unittest.mock import MagicMock, patch

from aib.main import parse_args
from aib.runner import Runner


class AnyListContaining(str):
    def __eq__(self, other):
        return self in other


@pytest.mark.parametrize("args", [
    ([]),
    (["--container"]),
    # Test with sudo (build option)
    (["build", "--sudo", "a", "b"]),
    (["--container", "build", "--sudo", "a", "b"]),
])
@patch("aib.runner.subprocess")
def test_run_args(subprocess_mock, args):
    subprocess_run = MagicMock()
    subprocess_mock.run = subprocess_run
    runner = Runner(parse_args(args))

    cmd = ["touch", "example"]
    runner.run(cmd)
    subprocess_run.assert_called_once_with(cmd, check=True)

@pytest.mark.parametrize("args", [
    ([]),
    (["--container"]),
    # Test with sudo (build option)
    (["build", "--sudo", "a", "b"]),
    (["--container", "build", "--sudo", "a", "b"]),
])
@patch("aib.runner.subprocess")
@patch("aib.runner.shutil")
def test_run_args_container(shutil_mock, subprocess_mock, args):
    subprocess_run = MagicMock()
    shutil_which = MagicMock(retrun_value="podman")
    subprocess_mock.run = subprocess_run
    shutil_mock.which = shutil_which
    args = parse_args(args)
    runner = Runner(args)

    cmd = ["touch", "example_container"]
    runner.run(cmd, use_container=True)
    expected = AnyListContaining("podman") if args.container else cmd
    subprocess_run.assert_called_once_with(expected, check=True)

@pytest.mark.parametrize("args", [
    ([]),
    (["--container"]),
    # Test with sudo (build option)
    (["build", "--sudo", "a", "b"]),
    (["--container", "build", "--sudo", "a", "b"]),
])
@patch("aib.runner.subprocess")
@patch("aib.runner.shutil")
def test_run_args_container_non_root(shutil_mock, subprocess_mock, args):
    subprocess_run = MagicMock()
    shutil_which = MagicMock(retrun_value="podman")
    subprocess_mock.run = subprocess_run
    shutil_mock.which = shutil_which
    args = parse_args(args)
    runner = Runner(args)

    cmd = ["touch", "example_user"]
    runner.run(cmd, use_container=True, use_non_root_user_in_container=True)
    expected = AnyListContaining("--user") if args.container else cmd
    subprocess_run.assert_called_once_with(expected, check=True)

@pytest.mark.parametrize("args", [
    ([]),
    (["--container"]),
    # Test with sudo (build option)
    (["build", "--sudo", "a", "b"]),
    (["--container", "build", "--sudo", "a", "b"]),
])
@patch("aib.runner.subprocess")
@patch("aib.runner.shutil")
def test_run_args_sudo(shutil_mock, subprocess_mock, args):
    subprocess_run = MagicMock()
    shutil_which = MagicMock(retrun_value="podman")
    subprocess_mock.run = subprocess_run
    shutil_mock.which = shutil_which
    args = parse_args(args)
    runner = Runner(args)

    cmd = ["touch", "example_sudo"]
    runner.run(cmd, use_sudo=True)
    expected = AnyListContaining("sudo") if vars(args).get("sudo", False) else cmd
    subprocess_run.assert_called_once_with(expected, check=True)

@pytest.mark.parametrize("container_autoupdate,use_non_root,volumes", [
    (False, False, []),
    (False, False, ["vol1"]),
    (False, False, ["vol1", "vol2"]),
    (True, False, []),
    (True, False, ["vol1"]),
    (True, False, ["vol1", "vol2"]),
    (False, True, []),
    (False, True, ["vol1"]),
    (False, True, ["vol1", "vol2"]),
    (True, True, []),
    (True, True, ["vol1"]),
    (True, True, ["vol1", "vol2"]),
])
def test_collect_podman_args(container_autoupdate, use_non_root, volumes):
    args = ["--container"]
    if container_autoupdate:
        args += ["--container-autoupdate"]
    runner = Runner(parse_args(args))
    for v in volumes:
        runner.add_volume(v)
    podman_args = runner._collect_podman_args(use_non_root_user_in_container=use_non_root)

    index = 4
    assert podman_args[:3] == ["--rm", "--privileged", "--workdir"]
    # Check volumes are added
    for v in volumes:
        assert podman_args[index] == "-v"
        assert v in podman_args[index+1] and ":" in podman_args[index+1]
        index += 2
    # Check container autoupdate
    if container_autoupdate:
        assert podman_args[index] == "--pull=newer"
        index += 1
    # Check use non root options
    if use_non_root:
        assert podman_args[index] == "--user"
    else:
        assert podman_args[index:index+2] == ["--security-opt", "label=type:unconfined_t"]