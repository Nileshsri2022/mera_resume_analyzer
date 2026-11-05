import numpy as np
import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
import warnings
warnings.filterwarnings('ignore')

from .linkedin_client import LinkedInClient


class LinkedInScraper:
    """Streamlit UI layer for scraping job listings from LinkedIn.

    Rendering/UI concerns live here; all Selenium/fetch logic is delegated to
    LinkedInClient (jobs/linkedin_client.py).
    """

    @staticmethod
    def webdriver_setup():
        """Set up and configure the Chrome webdriver"""
        return LinkedInClient.webdriver_setup()

    @staticmethod
    def get_user_input(show_title=True):
        """Get user input for job search parameters"""
        add_vertical_space(1)

        # Apply custom styling for the form
        if show_title:
            st.markdown("""
                <style>
                .linkedin-form {
                    background: rgba(10, 102, 194, 0.05);
                    border-radius: 10px;
                    padding: 20px;
                    border-left: 4px solid #0A66C2;
                    margin-bottom: 20px;
                }
                .linkedin-title {
                    color: #0A66C2;
                    font-weight: bold;
                }
                .linkedin-subtitle {
                    color: #666;
                    font-size: 0.9rem;
                    margin-bottom: 15px;
                }
                </style>
            """, unsafe_allow_html=True)

            st.markdown('<div class="linkedin-form">', unsafe_allow_html=True)
            st.markdown('<h3 class="linkedin-title"><i class="fab fa-linkedin"></i> LinkedIn Job Scraper</h3>', unsafe_allow_html=True)
            st.markdown('<p class="linkedin-subtitle">Find real-time job listings directly from LinkedIn</p>', unsafe_allow_html=True)

        with st.form(key='linkedin_scrape'):
            col1, col2, col3 = st.columns([0.5, 0.3, 0.2], gap='medium')

            with col1:
                job_title_input = st.text_input(
                    label='Job Title',
                    placeholder='e.g. Data Scientist, Software Engineer',
                    help="Enter job titles separated by commas"
                )
                job_title_input = job_title_input.split(',')

            with col2:
                job_location = st.text_input(
                    label='Job Location',
                    value='India',
                    placeholder='e.g. Bangalore, Mumbai, Remote',
                    help="Enter a location or 'India' for nationwide search"
                )

            with col3:
                job_count = st.number_input(
                    label='Number of Jobs',
                    min_value=1,
                    max_value=10,
                    value=3,
                    step=1,
                    help="Number of job listings to scrape (max 10)"
                )

            # Submit Button
            add_vertical_space(1)
            submit = st.form_submit_button(
                label='Search LinkedIn Jobs',
                type='primary',
                use_container_width=True
            )
            add_vertical_space(1)

        if show_title:
            st.markdown('</div>', unsafe_allow_html=True)

        return job_title_input, job_location, job_count, submit

    @staticmethod
    def build_url(job_title, job_location):
        """Build LinkedIn search URL from job title and location"""
        return LinkedInClient.build_url(job_title, job_location)

    @staticmethod
    def open_link(driver, link):
        """Open LinkedIn link and wait for page to load"""
        success, msg = LinkedInClient.open_link(driver, link)
        if not success:
            st.warning(msg)
        return success

    @staticmethod
    def link_open_scrolldown(driver, link, job_count):
        """Open LinkedIn link and scroll down to load more jobs"""
        success, msg = LinkedInClient.link_open_scrolldown(driver, link, job_count)
        if not success:
            st.warning(msg)
        return success

    @staticmethod
    def job_title_filter(scrap_job_title, user_job_title_input):
        """Filter job titles based on user input"""
        # Skip filtering if job title input is empty or contains only empty strings
        if not user_job_title_input or all(not title.strip() for title in user_job_title_input):
            return scrap_job_title

        # User job titles converted to lowercase
        user_input = [title.lower().strip() for title in user_job_title_input if title.strip()]

        # If no valid user input after cleaning, return the original title
        if not user_input:
            return scrap_job_title

        # Scraped job title converted to lowercase
        scrap_title = scrap_job_title.lower().strip()

        # Check if any user job title matches the scraped job title
        for user_title in user_input:
            # Check if all words in user title are in scraped title
            if all(word in scrap_title for word in user_title.split()):
                return scrap_job_title

        # No match found
        return np.nan

    @staticmethod
    def scrap_company_data(driver, job_title_input, job_location):
        """Scrape company data from LinkedIn job listings"""
        df, status = LinkedInClient.scrap_company_data(driver, job_title_input, job_location)

        if status == 'empty':
            st.warning("No job listings found on LinkedIn. Try different search terms.")
        elif isinstance(status, tuple) and status[0] == 'error':
            st.error(f"Error scraping company data: {status[1]}")
            st.info("Try refreshing the page or using different search terms.")

        return df

    @staticmethod
    def scrap_job_description(driver, df, job_count):
        """Scrape job descriptions for each job listing"""
        if df.empty:
            return df

        # Progress bar for scraping job descriptions
        progress_bar = st.progress(0)
        status_text = st.empty()

        def _update_progress(i, total):
            progress = int((i + 1) / total * 100)
            progress_bar.progress(progress)
            status_text.text(f"Scraping job {i+1} of {total}...")

        def _warn(message):
            st.warning(message)

        try:
            return LinkedInClient.scrap_job_description(
                driver,
                df,
                job_count,
                on_progress=_update_progress,
                on_warning=_warn,
            )
        finally:
            # Clear progress indicators
            progress_bar.empty()
            status_text.empty()

    @staticmethod
    def process_job_description(text):
        """Process and structure job description text"""
        return LinkedInClient.process_job_description(text)

    @staticmethod
    def display_data_userinterface(df_final):
        """Display scraped job data in the user interface"""
        if df_final.empty:
            st.warning("No matching jobs found. Try different search terms or location.")
            return

        # Apply custom styling for job cards
        st.markdown("""
            <style>
            .job-card {
                background: rgba(255, 255, 255, 0.05);
                border-radius: 10px;
                padding: 1.5rem;
                margin-bottom: 1rem;
                border-left: 4px solid #0A66C2;
                transition: transform 0.2s;
            }
            .job-card:hover {
                background: rgba(255, 255, 255, 0.08);
            }
            .job-title {
                color: #0A66C2;
                font-size: 1.3rem;
                margin-bottom: 0.5rem;
            }
            .company-name {
                font-weight: bold;
                font-size: 1.1rem;
            }
            .job-location {
                color: #888;
                margin-bottom: 1rem;
            }
            .job-url-button {
                display: inline-block;
                background: #0A66C2;
                color: white;
                padding: 0.5rem 1rem;
                border-radius: 5px;
                text-decoration: none;
                margin-top: 1rem;
                font-weight: bold;
            }
            .job-url-button:hover {
                background: #084d8e;
            }
            .job-count {
                background: rgba(10, 102, 194, 0.1);
                color: #0A66C2;
                padding: 0.5rem 1rem;
                border-radius: 5px;
                margin-bottom: 1rem;
                font-weight: bold;
            }
            .job-section {
                margin-top: 1rem;
                padding-top: 0.5rem;
                border-top: 1px solid rgba(255, 255, 255, 0.1);
            }
            .job-section-title {
                font-weight: bold;
                color: #0A66C2;
                margin-bottom: 0.5rem;
            }
            </style>
        """, unsafe_allow_html=True)

        # Display job count
        st.markdown(f'<div class="job-count">🎯 Found {len(df_final)} matching jobs on LinkedIn</div>', unsafe_allow_html=True)

        # Display each job
        for i in range(len(df_final)):
            company_name = df_final.iloc[i, 0]
            job_title = df_final.iloc[i, 1]
            location = df_final.iloc[i, 2]
            url = df_final.iloc[i, 3]
            description = df_final.iloc[i, 4]

            # Create job card
            st.markdown(f"""
                <div class="job-card">
                    <div class="job-title">{job_title}</div>
                    <div class="company-name">{company_name}</div>
                    <div class="job-location">📍 {location}</div>
                </div>
            """, unsafe_allow_html=True)

            # Job description in expander with better formatting
            with st.expander("View Job Description"):
                st.markdown(description)
                st.markdown(f"<a href='{url}' target='_blank' class='job-url-button'>Apply on LinkedIn</a>", unsafe_allow_html=True)

            st.markdown("<hr>", unsafe_allow_html=True)

    @staticmethod
    def main(show_title=True):
        """Main function to run the LinkedIn job scraper"""
        # Initialize driver to None
        driver = None

        try:
            # Get user input
            job_title_input, job_location, job_count, submit = LinkedInScraper.get_user_input(show_title)

            if submit:
                if job_title_input != [''] and job_location:
                    try:
                        # Set up Chrome webdriver
                        with st.spinner('Setting up Chrome webdriver...'):
                            driver = LinkedInScraper.webdriver_setup()

                            if not driver:
                                st.error("Failed to initialize Chrome webdriver. Please make sure Chrome is installed.")
                                return

                        # Build URL and open LinkedIn
                        with st.spinner('Loading LinkedIn jobs page...'):
                            link = LinkedInScraper.build_url(job_title_input, job_location)
                            st.info(f"Searching for: {', '.join([t for t in job_title_input if t.strip()])} in {job_location}")
                            success = LinkedInScraper.link_open_scrolldown(driver, link, job_count)

                            if not success:
                                st.error("Failed to load LinkedIn jobs page. Please try again.")
                                return

                        # Scrape job data
                        with st.spinner('Scraping job listings...'):
                            df = LinkedInScraper.scrap_company_data(driver, job_title_input, job_location)

                            if df.empty:
                                st.warning("No jobs found matching your criteria. Try different search terms.")
                                return

                        # Scrape job descriptions
                        with st.spinner('Fetching job descriptions...'):
                            df_final = LinkedInScraper.scrap_job_description(driver, df, job_count)

                            if df_final.empty:
                                st.warning("Could not retrieve job descriptions. Try different search terms.")
                                return

                        # Display results
                        LinkedInScraper.display_data_userinterface(df_final)

                    except Exception as e:
                        st.error(f"An error occurred: {str(e)}")
                        st.info("Try refreshing the page or using different search terms.")

                elif job_title_input == ['']:
                    st.warning("Please enter a job title to search.")

                elif not job_location:
                    st.warning("Please enter a job location to search.")

        except Exception as e:
            st.error(f"An unexpected error occurred: {str(e)}")

        finally:
            # Close the webdriver
            if driver:
                driver.quit()

def render_linkedin_scraper():
    """Render the LinkedIn job scraper interface"""
    # Don't show the title again, as it's already shown in the job_search.py file
    LinkedInScraper.main(show_title=False)
