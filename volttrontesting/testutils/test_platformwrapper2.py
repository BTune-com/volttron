import gevent
import pytest
import time
import warnings
import os

from volttron.platform import get_examples
from volttrontesting.fixtures.volttron_platform_fixtures import get_rand_port
from volttrontesting.utils.platformwrapper import PlatformWrapper
from volttron.platform.vip.agent import Agent, PubSub, Core

@pytest.mark.wrapper
def test_can_cleanup_installed_listener():
    try:
        import psutil
    except:
        warnings.warn('No psutil module present for this test')
        return
    wrapper = PlatformWrapper()

    address="tcp://127.0.0.1:{}".format(get_rand_port())
    wrapper.startup_platform(address)

    assert wrapper is not None
    assert wrapper.is_running()

    auuid = wrapper.install_agent(agent_dir=get_examples("ListenerAgent"),
                                  vip_identity="listener",
                                  start=False)
    assert auuid is not None
    started = wrapper.start_agent(auuid)
    assert isinstance(started, int)
    assert psutil.pid_exists(started)

    wrapper.shutdown_platform()
    # give operating system enough time to update pids.
    gevent.sleep(0.1)
    assert not psutil.pid_exists(started)


@pytest.mark.wrapper
def test_pid_file():
    try:
        import psutil
    except:
        warnings.warn('No psutil module present for this test')
        return
    wrapper = PlatformWrapper()

    address="tcp://127.0.0.1:{}".format(get_rand_port())
    wrapper.startup_platform(address)

    assert wrapper is not None
    assert wrapper.is_running()
    pid_file = os.path.join(wrapper.volttron_home, "VOLTTRON_PID")
    assert os.path.exists(pid_file)
    with open(pid_file, 'r') as pf:
        assert psutil.pid_exists(int(pf.read().strip()))

    wrapper.shutdown_platform()
    # give operating system enough time to update pids.
    gevent.sleep(0.1)
    assert not os.path.exists(pid_file)

    # Check overwrite of pid file. In case last shutdown was not clean
    with open(pid_file, 'w') as pf:
        pf.write('abcd')

    wrapper = PlatformWrapper()

    address = "tcp://127.0.0.1:{}".format(get_rand_port())
    wrapper.startup_platform(address)

    assert wrapper is not None
    assert wrapper.is_running()
    pid_file = os.path.join(wrapper.volttron_home, "VOLTTRON_PID")
    assert os.path.exists(pid_file)
    with open(pid_file, 'r') as pf:
        assert psutil.pid_exists(int(pf.read().strip()))



