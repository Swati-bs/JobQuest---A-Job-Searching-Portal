# JobQuest - Full-Stack Job Portal

**JobQuest** is a comprehensive full-stack job portal designed to streamline the job search and application process for users. Built using modern technologies, it combines secure user registration, personalized job recommendations, and real-time application tracking, all while providing an interactive and seamless experience for both candidates and recruiters.

## Key Features & Technologies

- **Secure User Registration**  
  Users can register using **OTP-based email verification** or **Google Sign-In**, ensuring both security and convenience. This feature ensures the safe onboarding of users and the prevention of spam accounts.

- **Advanced Job Search & Filters**  
  Job seekers can browse job listings using an intuitive **search bar** and **filters** (Location, Job Type, Salary Range, Experience Level), allowing them to narrow down their job search based on personal preferences and industry needs.

- **Job Recommendations**  
The system recommends personalized job listings by **matching the skills** listed in a user’s resume with the required skills in job postings, ensuring relevant and targeted opportunities.

- **Real-Time Application Tracking**  
  Applications are tracked in real-time, allowing users to monitor the progress of their applications with status updates such as *Applied*, *Shortlisted*, *Interviewing*, and *Selected*.

- **Profile Management & OpenCV Integration**  
  Users can **upload, update, and manage their profiles**, including **resume uploads** and **LinkedIn links**. A unique feature allows users to **capture their profile picture in real-time using OpenCV** and upload it directly, providing a polished look to their profile.

- **Account Management**  
  Users have the ability to **deactivate their account temporarily**, giving them flexibility while keeping their data secure and intact.

- **Job Alerts**  
  Personalized **job alerts** notify users about relevant opportunities based on their profile and job preferences, ensuring they never miss an opportunity.

- **Feedback Mechanism**  
  A built-in **feedback system** allows users to report bugs, suggest features, or provide feedback directly from the portal, enhancing user engagement and continuous improvement.

## Technologies Used

- **Frontend:** HTML5, CSS3, JavaScript, React.js
- **Backend:** Django, Python
- **Database:** SQLite
- **API & Authentication:** OAuth2 for Google Sign-In
- **Real-Time Features:** OpenCV for real-time profile image capture
- **Others:** Bootstrap, Git for version control

## How It Works

1. **Sign-Up:** Users can either register via OTP email verification or **Google Sign-In**.
2. **Profile Setup:** Users complete their profiles with personal details, work experience, resume uploads, and a professional profile picture (using OpenCV).
3. **Job Search:** Users can search for jobs and filter them based on location, job type, experience level, and salary range. Recommended jobs appear based on their profile.
4. **Application Tracking:** Users can track their application progress (from applied to selected) and receive status updates in real time.
5. **Job Alerts & Notifications:** Users receive customized job alerts based on their preferences.
