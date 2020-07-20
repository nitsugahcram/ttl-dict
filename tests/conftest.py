"""Fixtures and global testing configuration."""
import os
import py
import pytest

from uuid import uuid4
from unittest.mock import patch
from dependency_injector import providers
from precogs import main
from precogs import stc
from precogs.db.dal import Dal, etcd
from precogs.toolbox.configuration import Configuration
from precogs.toolbox.logger import get_logger, set_logger
from precogs.core import CoreBasic, TracesMetrics
from precogs.core_flask import CoreFlask
from precogs.core_app import CoreApp
from precogs.core_model import CoreModels
from precogs.databus.loop import ReaderLoop
# from precogs.traces.scheduler.intercept import DispatcherInterceptor
from precogs.traces.scheduler.intercept_vectorize import VectorDispatcher
from precogs.traces.scheduler.intercept_speedup import AgglutiantorDispatcher
from precogs import tests
from .common import Hooks, LoggerHooks, ProducerMockCounter

DATA_PATH = "{tests}/data".format(tests=os.path.dirname(tests.__file__))
CONFIG_PATH = "{data}/etc/metamorph".format(data=DATA_PATH)
TRACE_REG_OK = os.path.join(DATA_PATH, "traceEvent_test_reg_data.log")
TRACE_LOG_PERFOMANCE = os.path.join(DATA_PATH, "traceEvent_10000_traces.log")
TRACE_INSTALLER_OK = os.path.join(DATA_PATH,
                                  "traceEvent_test_installer_data.log")

TRACE_LOG_PERFOMANCE_PKL = os.path.join(DATA_PATH,
                                        "traceEvent_10000_traces.pkl")


@pytest.fixture
def tmpconfig(tmpdir):
    """Create a temporal copy of the whole configuration."""
    base_config = py.path.local(CONFIG_PATH)
    base_config.copy(tmpdir)
    yield tmpdir
    # restory the configuration files
    base_config = py.path.local(CONFIG_PATH)
    base_config.copy(tmpdir)


@pytest.fixture
def init(tmpdir, tmpconfig):  # noqa ; pylint: disable=redefined-outer-name
    """Initialize fixture, patch the configuration and set up the logger.

    First calls `Configuration.getInstance(CONFIG_PATH)` to create the
    configuration singleton with an artifitial configuration path.
    Then all the following configuration (logger, etc) follow this
    fake configuration for testing.
    """

    # Patching the Application container
    patcher_etcd_client = patch("etcd.Client", autospec=True)
    mock_etcd_client = patcher_etcd_client.start()
    _overide_namespace = str(uuid4())

    configuration_path = tmpconfig
    CoreBasic.config.override(
        providers.Callable(Configuration.getInstance, str(configuration_path)))

    CoreBasic.logger = providers.Callable(get_logger, "classifier.application")

    CoreBasic.logger_api = providers.Callable(get_logger, "classifier.api")

    CoreBasic.Dal.override(
        providers.Factory(Dal, CoreBasic.logger, CoreBasic.config, 1,
                          _overide_namespace, "http",
                          "service.test.ETCD_NODE_{n}", mock_etcd_client))

    CoreApp.VectorizeDispacher.override(
        providers.Callable(VectorDispatcher, CoreBasic.config))

    CoreApp.AgglutinatorDispacher.override(
        providers.Callable(AgglutiantorDispatcher, CoreBasic.config,
                           CoreBasic.logger, CoreBasic.TracesToMetrics))

    main.METRICS = CoreFlask.InternalMetricsReporter()

    reader_log_file = tmpdir.join("classifier-appreader.json")
    api_log_file = tmpdir.join("classifier-api.json")

    cfg = CoreBasic.config()
    cfg["service"]["logger"]['stdout'] = False
    cfg["service"]["logger"]["application"]["file"] = str(reader_log_file)
    cfg["service"]["logger"]["api"]["file"] = str(api_log_file)
    set_logger("classifier.application", cfg, str(reader_log_file))
    set_logger("classifier.api", cfg, str(api_log_file))

    dal_obj = CoreBasic.Dal()
    main.DAL = dal_obj
    Dal.RETRY_WAIT = 0
    main.STC_HOST_URI = "http://localhost:9222"

    yield {
        "application_log_file": reader_log_file,
        "api_log_file": api_log_file,
        "configuration_path": configuration_path,
        "dal": dal_obj,
        "flask_dal": main.DAL,
        "dal_override": _overide_namespace
    }
    dal_obj.reset()
    patcher_etcd_client.stop()
    cfg.releaseInstance()


@pytest.fixture
def flaskinit(init):  # noqa; pylint: disable=redefined-outer-name
    """Initialize the flask application for testing purpose."""

    main.FLASK.config['TESTING'] = True
    main.FLASK.config['WTF_CSRF_ENABLED'] = False
    main.FLASK.config['DEBUG'] = False
    app = main.FLASK.test_client()
    assert main.FLASK.debug is False
    return (init, app)


@pytest.fixture
def traces_log():
    """Initialize the File Log."""
    file_descriptor_reg = open(TRACE_REG_OK, encoding='UTF-8')
    file_descriptor_installer = open(TRACE_INSTALLER_OK, encoding='UTF-8')
    file_descriptor_perfromance = open(TRACE_LOG_PERFOMANCE, encoding='UTF-8')
    yield {
        'handler_reg': file_descriptor_reg,
        'handler_installer': file_descriptor_installer,
        'performance_traces': file_descriptor_perfromance
    }
    file_descriptor_installer.close()
    file_descriptor_reg.close()
    file_descriptor_perfromance.close()


@pytest.fixture
def traces_pkl():
    """Initialize the File Log."""
    from precogs.toolbox.utils.basic_serialization import load_from_pickle
    trace_list = load_from_pickle(TRACE_LOG_PERFOMANCE_PKL)
    yield {'traces_list': trace_list}


@pytest.fixture
def tree_log():
    """Initialize the File Log."""
    TRACE_PC1_OK = os.path.join(DATA_PATH, "traceEvent_tree.log")
    TRACE_TREE_SHAPE_OK = os.path.join(DATA_PATH, "traceEvent_shape.log")
    file_descriptor_tree = open(TRACE_PC1_OK, encoding='UTF-8')
    file_descriptor_shape = open(TRACE_TREE_SHAPE_OK, encoding='UTF-8')
    yield {
        'handler_tree': file_descriptor_tree,
        'handler_shape': file_descriptor_shape,
    }
    file_descriptor_tree.close()
    file_descriptor_shape.close()


@pytest.fixture
def hooks_init(init):
    CoreBasic.MetricMock = providers.Singleton(LoggerHooks)

    CoreModels.Hooks.override(providers.Callable(Hooks, CoreBasic.MetricMock))

    return init


@pytest.fixture
def hooks_publisher(init):
    CoreBasic.Publisher.override(
        providers.Singleton(ProducerMockCounter, CoreBasic.config))

    return init
