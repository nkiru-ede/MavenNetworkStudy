# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 15:23:23 2025

@author: edenk
"""

import requests
import csv
import os
import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



# File paths
BASE_DIR = "directory path"
VERSIONS_CSV = os.path.join(BASE_DIR, "versions.csv")
DEPENDENCIES_CSV = os.path.join(BASE_DIR, "dependencies.csv")
PROCESSED_PACKAGES_FILE = os.path.join(BASE_DIR, "processed_packages.txt")
PROCESSED_VERSIONS_FILE = os.path.join(BASE_DIR, "processed_versions.txt")
PROCESSED_DEPENDENCIES_FILE = os.path.join(BASE_DIR, "processed_dependencies.txt")

# Initialize CSVs
def initialize_csv(file_path, headers):
    if not os.path.exists(file_path):
        with open(file_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            print(f"CSV initialized: {file_path}")

# Load processed items
def load_processed(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            return set(line.strip() for line in file.readlines())
    return set()

# Save a processed item
def save_processed(file_path, item):
    with open(file_path, "a", encoding="utf-8") as file:
        file.write(f"{item}\n")
        print(f"Processed item saved: {item}")

# Save data to CSV immediately
def save_to_csv(file_path, rows):
    with open(file_path, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(rows)
        print(f"Data saved to CSV: {file_path}")

# Initialize the Selenium driver
def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode (no GUI)
    driver = webdriver.Chrome(options=options)
    return driver

# Scrape all npm packages dynamically
def get_all_packages():
    processed_packages = load_processed(PROCESSED_PACKAGES_FILE)
    driver = init_driver()
    page = 1

    while True:
        url = f"https://packages.ecosyste.ms/registries/repo1.maven.org/packages?page={page}&per_page=100"
        driver.get(url)

        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/packages/')]")))
            package_elements = driver.find_elements(By.XPATH, "//a[contains(@href, '/packages/')]")

            if not package_elements:
                break  # Stop if no more packages found

            for element in package_elements:
                package_name = element.text.strip()
                if package_name and package_name not in processed_packages:
                    print(f"Package found: {package_name}")
                    
                    # Process the package immediately
                    process_package(package_name, processed_packages)

            print(f"Page {page} scraped")
            page += 1

        except Exception as e:
            print(f"Error scraping page {page}: {e}")
            traceback.print_exc()
            break

    driver.quit()

# Process each package immediately
def process_package(package_name, processed_packages):
    # Scrape versions for the current package
    artifacts = scrape_versions(package_name)
    save_processed(PROCESSED_PACKAGES_FILE, package_name)

    # # Scrape dependencies for each version (artifact) of the current package
    # for artifact in artifacts:
    #     scrape_dependencies(artifact)

    # print(f"Finished processing package: {package_name}\n")

# Scrape versions using API
def scrape_versions(package_name):
    processed_versions = load_processed(PROCESSED_VERSIONS_FILE)

    if package_name in processed_versions:
        print(f"Skipping already processed package: {package_name}")
        return []

    url = f"https://packages.ecosyste.ms/api/v1/registries/repo1.maven.org/packages/{package_name}/versions"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for errors
        data = response.json()

        # Debugging: print the response data
        print(f"Response data for {package_name}: {data}")

        # Check if the response is a list of versions (adjust the logic)
        if isinstance(data, list):
            rows = []
            for version_info in data:
                version = version_info['number']
                release_date = version_info['published_at']
                artifact_version = f"{package_name}:{version}"
                rows.append((artifact_version, release_date))

                print(f"Version found: {artifact_version}, Release date: {release_date}")

                # Save to CSV immediately
                save_to_csv(VERSIONS_CSV, [(artifact_version, release_date)])

            return [row[0] for row in rows]
        else:
            print(f"Unexpected response format for {package_name}: {data}")
            return []
    
    except requests.exceptions.RequestException as e:
        print(f"Error scraping versions for {package_name}: {e}")
        return []
        
        
# # Scrape dependencies using API
# def scrape_dependencies(package_name):
#     processed_dependencies = load_processed(PROCESSED_DEPENDENCIES_FILE)

#     if package_name in processed_dependencies:
#         print(f"Skipping already processed package: {package_name}")
#         return []

#     url = f"https://packages.ecosyste.ms/api/v1/registries/repo1.maven.org/packages/{package_name}/versions"
    
#     try:
#         response = requests.get(url)
#         response.raise_for_status()  # Check for errors
#         data = response.json()

#         # Debugging: print the response data
#         print(f"Response data for {package_name}: {data}")

#         # Check if the response is a list of dependencies (adjust the logic)
#         if isinstance(data, list):
#             rows = []
#             for dependency_info in data:
#                 dependency = dependency_info['package_name']
#                 version = dependency_info['requirements']
#                 artifact_dependency = f"{dependency}:{version}"
#                 rows.append((artifact_dependency, version))

#                 print(f"Dependency found: {artifact_dependency}, Version: {version}")

#                 # Save to CSV immediately
#                 save_to_csv(DEPENDENCIES_CSV, [(artifact_dependency, version)])

#             return [row[0] for row in rows]
#         else:
#             print(f"Unexpected response format for {package_name}: {data}")
#             return []
    
#     except requests.exceptions.RequestException as e:
#         print(f"Error scraping dependencies for {package_name}: {e}")
#         return []


# Main function        
def scrape_all():
    # Initialize CSV files with headers if they don't exist
    initialize_csv(VERSIONS_CSV, ["artifact", "release"])
    initialize_csv(DEPENDENCIES_CSV, ["source", "target"])

    # Get and process packages one by one
    get_all_packages()

if __name__ == "__main__":
    scrape_all()
