import pytest
import logging
from dash.testing.application_runners import import_app
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Set up logging for debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Fixture to set up ChromeDriver path
@pytest.fixture(scope="session")
def chrome_driver():
    try:
        driver_path = ChromeDriverManager().install()
        logger.info(f"ChromeDriver path: {driver_path}")
        return driver_path
    except Exception as e:
        logger.error(f"Failed to install ChromeDriver: {e}")
        raise

# Override dash_duo to use Chrome with managed driver
@pytest.fixture
def dash_duo(dash_duo, chrome_driver):
    try:
        options = Options()
        options.add_argument("--headless=new")  # New headless mode for Chrome
        options.add_argument("--disable-gpu")  # Required for headless on Windows
        options.add_argument("--no-sandbox")  # Avoid sandbox issues
        options.add_argument("--disable-dev-shm-usage")  # Avoid memory issues
        service = Service(executable_path=chrome_driver)
        dash_duo.driver = webdriver.Chrome(service=service, options=options)
        logger.info("ChromeDriver initialized successfully")
        yield dash_duo
        dash_duo.driver.quit()
    except Exception as e:
        logger.error(f"Failed to initialize ChromeDriver: {e}")
        raise

# Fixture to import the Dash app
@pytest.fixture
def dash_app():
    return import_app("app")  # Assumes app.py in project root

# Test 1: Header is present and has the correct text
def test_header_present(dash_duo, dash_app):
    dash_duo.start_server(dash_app)
    header = dash_duo.wait_for_element("h1", timeout=10)
    assert header is not None, "Header element not found"
    assert header.text == "🌸 Pink Morsel Sales Dashboard", "Header text does not match"

# Test 2: Visualization (graph) is present
def test_visualization_present(dash_duo, dash_app):
    dash_duo.start_server(dash_app)
    graph = dash_duo.wait_for_element("#sales-graph", timeout=10)
    assert graph is not None, "Visualization element not found"

# Test 3: Region picker is present
def test_region_picker_present(dash_duo, dash_app):
    dash_duo.start_server(dash_app)
    region_picker = dash_duo.wait_for_element("#region-selector", timeout=10)
    assert region_picker is not None, "Region picker element not found"